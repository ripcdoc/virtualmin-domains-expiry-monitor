
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from config import Config

def send_email(subject, html_content, plain_content):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = Config.EMAIL_USER
    msg['To'] = ", ".join(Config.EMAIL_RECIPIENTS)

    msg.attach(MIMEText(plain_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(Config.EMAIL_HOST, Config.EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
        smtp.sendmail(Config.EMAIL_USER, Config.EMAIL_RECIPIENTS, msg.as_string())

def render_email_template(template_name, context):
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template(template_name)
    return template.render(context)
