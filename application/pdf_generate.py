from .mail_fun import *
import os
from weasyprint import HTML,CSS
from jinja2 import Template

BasePath=os.path.abspath(os.path.dirname(__file__))

def report_func(data):
    f=open(os.path.join(BasePath, "mail template", "report.html"),"r")
    template=Template(f.read())
    html=template.render(data=data)
    css=CSS(filename=os.path.join(BasePath, "mail template", "report.css"))
    pdf_byte=HTML(string=html).write_pdf(stylesheets=[css])
    message=f"hello {data.user.first_name}\nthis is summary mail please check attached Monthly Report Pdf"
    send_mail(data.user.email,"Monthly Report",message,pdf_byte)