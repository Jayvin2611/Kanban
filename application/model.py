from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
db=SQLAlchemy()


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String,nullable=False, unique=True)
    password = db.Column(db.String,nullable=False)
    first_name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    lists= db.relationship('List', backref='user')
    chat = db.relationship('Chat', backref='user')
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)



class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String,nullable=False)
    cards = db.relationship('Card', backref='list',lazy='subquery',cascade="all,delete")

class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey(List.id,ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String,nullable=False)
    content = db.Column(db.String)
    deadline = db.Column(db.DateTime,nullable=False)
    completed = db.Column(db.Boolean,nullable=False)
    created_on = db.Column(db.DateTime,nullable=False)

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.String,nullable=False, unique=True)

    