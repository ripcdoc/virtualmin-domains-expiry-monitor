
"""
notifications.py

This module handles email notifications for domain and SSL expiration alerts. It uses SMTP
to send emails and Jinja2 templates for rendering HTML and plain text content. Error handling
ensures that notification failures are logged.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from config import Config
from logger import setup_logger
from exceptions import NotificationError

logger = setup_logger()

def send_notification(subject, html_content, plain_content):
    """
    Sends an email notification using SMTP.

    Parameters:
    - subject (str): Subject of the email.
    - html_content (str): HTML content of the email.
    - plain_content (str): Plain text content of the email.

    Raises:
    - NotificationError: If there is an issue with sending the email.
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = Config.EMAIL_SENDER
        msg['To'] = Config.EMAIL_RECIPIENT

        msg.attach(MIMEText(plain_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.login(Config.SMTP_USER, Config.SMTP_PASS)
            server.sendmail(Config.EMAIL_SENDER, Config.EMAIL_RECIPIENT, msg.as_string())
        logger.info(f"Notification sent: {subject}")
    except smtplib.SMTPException as e:
        raise NotificationError(f"SMTP error while sending notification: {e}")
    except Exception as e:
        raise NotificationError(f"Unexpected error while sending notification: {e}")

def render_email_template(template_name, context):
    """
    Renders an email template using Jinja2.

    Parameters:
    - template_name (str): Name of the template file.
    - context (dict): Context data for rendering the template.

    Returns:
    - str: Rendered email content.

    Raises:
    - NotificationError: If there is an issue rendering the template.
    """
    try:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template(template_name)
        return template.render(context)
    except TemplateNotFound:
        raise NotificationError(f"Template not found: {template_name}")
    except Exception as e:
        raise NotificationError(f"Error rendering email template: {e}")
