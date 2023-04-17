import requests
from jinja2 import Template
from datetime import datetime

template="""Hello {{ data.user.first_name }}
This is a reminder message to remind you that you have deadline for following cards,
{% for card in data.cards %}
   {{loop.index}}. {{ card.title }} with Deadline {{ card.deadline.strftime("%d/%m/%Y %I:%M %p") }}
{% endfor %}"""

def send_reminder(data):
    message=Template(template).render(data=data)
    responce = requests.post(data.url,json={'text':message})
    print(responce.status_code)
    return True

template="""Hello {{ data.user.first_name }}
This is a reminder message to remind you that you have deadline for following cards,
{% for card in data.cards %}
   {{loop.index}}. {{ card.title }} with Deadline {{ card.deadline.strftime("%d/%m/%Y %I:%M %p") }}
{% endfor %}"""

def web_hook():
    url=""
    message="Hello dont forgot to post today" 
    responce = requests.post(url,json={'text':message})
    return True