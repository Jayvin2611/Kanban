from application.workers import celery
from celery.schedules import crontab
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .model import *
from .pdf_generate import *
from .reminder import *

class Month_report_data():
    def __init__(self,user):
        self.user = user
        self.total = 0
        self.completed = 0
        self.pending = 0
        self.overdue = 0

class Daily_reminder_data():
    def __init__(self,user):
        self.user = user
        self.cards = []
        self.url = None

@celery.task()
def monthly_report():
    first_of_this_month=datetime.now().replace(day=1,hour=0, minute=0, second=0, microsecond=0)
    first_of_last_month=first_of_this_month-relativedelta(months=1)
    # cards=Card.query.filter((Card.created_on>=first_of_last_month) & (Card.created_on<first_of_this_month)).all()
    cards=Card.query.all()
    user_dict = dict()
    if cards is not None:
        for card in cards:
            user = card.list.user
            if user.id not in user_dict:
                user_dict[user.id]=Month_report_data(user=user)
            data = user_dict[user.id]
            data.total +=1
            if card.completed:
                data.completed+=1
            else:
                data.pending+=1
            if card.deadline<datetime.now():
                data.overdue+=1
        for data in user_dict.values():
            report_func(data)


@celery.task()
def daily_reminder():
    today=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow=today+relativedelta(days=1)
    # cards=Card.query.filter((Card.deadline>=today) & (Card.deadline<tomorrow)).all()
    cards=Card.query.all()
    user_dict = dict()
    if cards is not None:
        for card in cards:
            user = card.list.user
            if user.id not in user_dict:
                user_dict[user.id]=Daily_reminder_data(user=user)
                chat=Chat.query.filter_by(user_id=user.id).first()
                if chat is not None:
                    user_dict[user.id].url=chat.url
            data=user_dict[user.id]
            data.cards.append(card)
        for data in user_dict.values():
            if data.url is not None:
                send_reminder(data)
            

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(10.0, monthly_report.s(), name='Report mail') # here time is in utc not ist   
    sender.add_periodic_task(10.0,daily_reminder.s(),name='Reminder msg') # here time is in utc not ist
    # crontab(minute=0,hour=0,day_of_month=1)
    # crontab(minute=30,hour=18)