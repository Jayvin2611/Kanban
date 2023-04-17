import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from jinja2 import Template

Host="localhost"
Port= 1025
Mail = "kanban_report@gmail.com"
Password = ""


def send_mail(to,subject,message, attachment_file):
    msg=MIMEMultipart()
    msg["From"]= Mail
    msg["To"]= to
    msg["Subject"]= subject
    msg.attach(MIMEText(message, "plain"))
    attach = MIMEApplication(attachment_file,_subtype="pdf")
    attach.add_header('Content-Disposition','attachment; filename=MonthlyReport.pdf')
    msg.attach(attach)
    s=smtplib.SMTP(host=Host,port=Port)
    s.login(Mail,Password)
    s.send_message(msg)
    s.quit()
    return True
