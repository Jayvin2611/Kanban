from flask_restful import Resource, Api,fields, marshal_with,reqparse
from flask_security import current_user,auth_required,SQLAlchemySessionUserDatastore,hash_password
from flask_cors import cross_origin
from application.model import *
from flask import current_app as app,make_response
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .validations import *
from .caching import *


user_datastore = SQLAlchemySessionUserDatastore(db.session, User,Role)


error_messages = {
    'USER01': "First Name Can't Be empty",
    'USER02': "Email id Already Exist Try Another Email id.",
    'USER03': "User Doesn't Have any Traker.",
    'USER04': 'Enter Valid Email id.',
    'USER05': 'Opps unable to sent OTP to your email id please try again later',
    'PASSWORD01': 'Wrong Password.',
    'PASSWORD02': "Password Can't Be empty",
    'PASSWORD03': 'Password Must be 8 character long',
    'PASSWORD04': "Old Password and New Password can't be same",
    'LIST01': "List Doesn't Exist.",
    'LIST02': "List Name Can't Be empty",
    'LIST03': 'List With Same Name Already Exist.',
    'LIST04': "List Id can't be empty",
    'LIST05': "List Doesnt Have any Card",
    'LIST06': "List Id Can't Be empty",
    'CARD01': "Card Doesn't Exist.",
    'CARD02': "Card Doesn't Belong to This List",
    'CARD03': "Card Already Exits.",
    'CARD04': "Card Id is not give in url",
    'LINK01': "Google space link can't be empty",
    'LINK02': "Google space link is not valid"
}



user_parser = reqparse.RequestParser()
user_parser.add_argument('id')
user_parser.add_argument('email')
user_parser.add_argument('password')
user_parser.add_argument('first_name')
user_parser.add_argument('last_name')

list_parser = reqparse.RequestParser()
list_parser.add_argument('id')
list_parser.add_argument('name')

card_parser = reqparse.RequestParser()
card_parser.add_argument('id')
card_parser.add_argument('list_id')
card_parser.add_argument('title')
card_parser.add_argument('content')
card_parser.add_argument('deadline')
card_parser.add_argument('completed')

link_parser = reqparse.RequestParser()
link_parser.add_argument('link')

dragdrop_parser = reqparse.RequestParser()
dragdrop_parser.add_argument('card_id')
dragdrop_parser.add_argument('list_id')



user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'token':fields.String(attribute=lambda x: x.get_auth_token())
}

card_fields = {
    'id': fields.Integer,
    'list_id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'deadline': fields.String(attribute=lambda x : x.deadline.strftime('%Y-%m-%dT%H:%M')),
    'completed': fields.Boolean
}

list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'cards': fields.Nested(card_fields)
}

class Link(Resource):
    @auth_required('token')
    def post(self):
        args = link_parser.parse_args()
        link=args.get('link')
        if link is None:
            raise BusinessValidationError(400,error_code='LINK01',error_msg=error_messages['LINK01'])
        if 'chat.googleapis.com/v1' not in link:
            raise BusinessValidationError(400,error_code='LINK02',error_msg=error_messages['LINK02'])
        user_id=current_user.id
        chat=Chat.query.filter_by(user_id=user_id).first()
        if chat is None:
            chat=Chat(user_id=user_id,url=link)
            db.session.add(chat)
            db.session.commit()
            raise BusinessValidationSuccessful()
        chat.url=link
        db.session.commit()
        raise BusinessValidationSuccessful()


class Export(Resource):
    @auth_required('token')
    def get(self,id=None):
        if id is None:
            raise BusinessValidationError(400,error_code='LIST06',error_msg=error_messages['LIST06'])
        list=None
        [l:=x for x in current_user.lists if x.id == id]
        if l is None:
            raise BusinessValidationError(400,error_code='LIST01',error_msg=error_messages['LIST01'])
        csv = 'id,title,content,deadline,completed,created_on\n'
        if l.cards is not None:
            for card in l.cards:
                title=card.title.replace(',',' ')
                content=card.content.replace(',','')
                deadline=card.deadline.strftime("%d/%m/%Y %I:%M %p")
                created_on=card.created_on.strftime("%d/%m/%Y %I:%M %p")
                csv+=f'{str(card.id)},{title},{content},{deadline},{str(card.completed)},{created_on}\n'
            csv_byte=csv.encode()
            response=make_response(csv_byte)
            return response
        raise BusinessValidationError(400,error_code='LIST05',error_msg=error_messages['LIST05'])

class ChartDataApi(Resource):
    @auth_required('token')
    def get(self):
        first_of_this_month=datetime.now().replace(day=1,hour=0, minute=0, second=0, microsecond=0)
        cards=Card.query.filter(Card.created_on>=first_of_this_month).all()
        c=[x for x in cards if x.list.user.id==current_user.id]
        d=dict()
        d['total']=len(c)
        d['completed']=0
        d['pending']=0
        d['overdue']=0
        for card in c:
            if card.completed:
                d['completed']+=1
            else:
                d['pending']+=1
            if card.deadline<datetime.now():
                d['overdue']+=1
        d['series']=[d['completed'],d['pending']]
        return d,200

class DragDrop(Resource):
    @auth_required('token')
    def put(self):
        args = dragdrop_parser.parse_args()
        card_id=args.get('card_id')
        list_id=args.get('list_id')
        card=Card.query.filter_by(id=card_id).first()
        list=List.query.filter_by(id=list_id).first()
        if card is not None and list is not None:
            if card.list.user.id==current_user.id and list.user.id==current_user.id:
                previous_list = card.list
                previous_list.cards.remove(card)
                card.list_id=list.id
                list.cards.append(card)
                db.session.commit()
                raise BusinessValidationSuccessful()



class UserApi(Resource):
    @auth_required('token')
    @marshal_with(user_fields)
    def get(self):
        return current_user
    
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        email=args.get('email')
        password=args.get('password')
        first_name=args.get('first_name')
        last_name=args.get('last_name')
        if email is None:
            raise BusinessValidationError(400,error_code='USER04',error_msg=error_messages['USER04'])
        if '@' not in email:
            raise BusinessValidationError(400,error_code='USER04',error_msg=error_messages['USER04'])
        if password is None or password=='':
            raise BusinessValidationError(400,error_code='PASSWORD02',error_msg=error_messages['PASSWORD02'])
        if len(password)<8:
            raise BusinessValidationError(400,error_code='PASSWORD03',error_msg=error_messages['PASSWORD03'])
        if first_name is None or first_name=='':
            raise BusinessValidationError(400,error_code='USER01',error_msg=error_messages['USER01'])
        try:
            user=user_datastore.create_user(email=email,password=hash_password(password),
            first_name=first_name,last_name=last_name)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            db.session.rollback()
            if 'UNIQUE' in error:
                raise BusinessValidationError(400,error_code='USER02',error_msg=error_messages['USER02'])
            print(error)
            raise BusinessValidationError(400,error_code='Error',error_msg='Unkown Error')
    
    @auth_required('token')
    @marshal_with(user_fields)
    def put(self):
        args = user_parser.parse_args()
        first_name=args.get('first_name')
        last_name=args.get('last_name')
        if first_name is None or first_name=='':
            raise BusinessValidationError(400,error_code='PASSWORD02',error_msg=error_messages['PASSWORD02'])
        current_user.first_name=first_name
        current_user.last_name=last_name
        db.session.commit()
        return current_user
    
class ListApi(Resource):
    @auth_required('token')
    @marshal_with(list_fields)
    def get(self,id=None):
        if id is None:
            # lists = get_lists(current_user.id)                #caching
            lists= current_user.lists
            return lists
        else:
            id=id
            l=None
            [l:=x for x in current_user.lists if x.id == id]
            if l is None:
                raise BusinessValidationError(400,error_code='LIST01',error_msg=error_messages['LIST01'])
            return l
    
    @auth_required('token')
    @marshal_with(list_fields)
    def post(self):
        args = list_parser.parse_args()
        name=args.get('name')
        if name is None or name=='':
            raise BusinessValidationError(400,error_code='LIST02',error_msg=error_messages['LIST02'])
        l=None
        [l:=x for x in current_user.lists if x.name == name]
        if l is None:
            l=List(name=name,user_id=current_user.id)
            db.session.add(l)
            current_user.lists.append(l)
            db.session.commit()
            return l
        raise BusinessValidationError(400,error_code='LIST03',error_msg=error_messages['LIST03'])
    
    @auth_required('token')
    @marshal_with(list_fields)
    def put(self):
        args = list_parser.parse_args()
        id=int(args.get('id'))
        name=args.get('name')
        if name is None or name=='':
            raise BusinessValidationError(400,error_code='LIST02',error_msg=error_messages['LIST02'])
        l=None
        [l:=x for x in current_user.lists if x.name == name]
        if l is not None:
            raise BusinessValidationError(400,error_code='LIST03',error_msg=error_messages['LIST03'])
        l=None
        [l:=x for x in current_user.lists if x.id == id]
        if l is not None:
            l.name=name
            db.session.commit()
            return l
        raise BusinessValidationError(400,error_code='LIST04',error_msg=error_messages['LIST04'])
    
    @auth_required('token')
    def delete(self):
        args = list_parser.parse_args()
        id=int(args.get('id'))
        l=None
        [l:=x for x in current_user.lists if x.id == id]
        if l is not None:
            db.session.delete(l)
            db.session.commit()
            raise BusinessValidationSuccessful()
        raise BusinessValidationError(400,error_code='LIST04',error_msg=error_messages['LIST04'])

class CardApi(Resource):
    @auth_required('token')
    @marshal_with(card_fields)
    def get(self,id=None):
        if id is None:
            raise BusinessValidationError(400,error_code='CARD04',error_msg=error_messages['CARD04'])
        card=Card.query.filter_by(id=id).first()
        if card is None:
            raise BusinessValidationError(400,error_code='CARD01',error_msg=error_messages['CARD01'])
        if card.list not in current_user.lists:
            raise BusinessValidationError(400,error_code='CARD02',error_msg=error_messages['CARD02'])
        return card
    
    @auth_required('token')
    @marshal_with(card_fields)
    def post(self):
        args=card_parser.parse_args()
        list_id=int(args.get('list_id'))
        title=args.get('title')
        content=args.get('content')
        deadline=datetime.strptime(args.get('deadline'),'%Y-%m-%dT%H:%M')
        completed=True if args.get('completed')=='True' else False
        l=None
        [l:=x for x in current_user.lists if x.id == list_id]
        if l is None:
            raise BusinessValidationError(400,error_code='LIST04',error_msg=error_messages['LIST04'])
        card=None
        [card:=x for x in l.cards if x.title==title]
        if card is not None:
            raise BusinessValidationError(400,error_code='CARD03',error_msg=error_messages['CARD03'])
        card=Card(list_id=list_id,title=title,content=content,deadline=deadline,completed=completed,created_on = datetime.now())
        db.session.add(card)
        l.cards.append(card)
        db.session.commit()
        return card
    
    @auth_required('token')
    @marshal_with(card_fields)
    def put(self):
        args=card_parser.parse_args()
        id=int(args.get('id'))
        list_id=int(args.get('list_id'))
        title=args.get('title')
        content=args.get('content')
        completed=True if args.get('completed')=='True' else False
        l=None
        [l:=x for x in current_user.lists if x.id == list_id]
        if l is None:
            raise BusinessValidationError(400,error_code='LIST04',error_msg=error_messages['LIST04'])
        card=Card.query.filter_by(id=id).first()
        if card is None:
            raise BusinessValidationError(400,error_code='CARD01',error_msg=error_messages['CARD01'])
        if card.list.id != l.id:
            raise BusinessValidationError(400,error_code='CARD02',error_msg=error_messages['CARD02'])
        card.title=title
        card.content=content
        card.completed=completed
        db.session.commit()
        return card
    
    @auth_required('token')
    def delete(self):
        args=card_parser.parse_args()
        id=int(args.get('id'))
        list_id=int(args.get('list_id'))
        l=None
        [l:=x for x in current_user.lists if x.id == list_id]
        if l is None:
            raise BusinessValidationError(400,error_code='LIST04',error_msg=error_messages['LIST04'])
        card=Card.query.filter_by(id=id).first()
        if card is None:
            raise BusinessValidationError(400,error_code='CARD01',error_msg=error_messages['CARD01'])
        if card.list.id != l.id:
            raise BusinessValidationError(400,error_code='CARD02',error_msg=error_messages['CARD02'])
        db.session.delete(card)
        db.session.commit()
        raise BusinessValidationSuccessful()