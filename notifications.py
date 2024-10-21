import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from config import Config
import logging

logger = logging.getLogger(__name__)

def prepare_email_context(expiration_type, domain, days_until_expire):
    """
    Prepares the context for rendering email templates with common variables.

    Args:
        expiration_type (str): Type of expiration (e.g., 'SSL' or 'domain registration').
        domain (str): Domain name being monitored.
        days_until_expire (int): Number of days until expiration.

    Returns:
        dict: Context data for email templates.
    """
    return {
        'subject': f"{expiration_type.capitalize()} Expiration Alert: {domain}",
        'expiration_type': expiration_type,
        'domain': domain,
        'days_until_expire': days_until_expire,
        'logo_url': Config.LOGO_URL,
        'support_url': Config.SUPPORT_URL
    }

def send_email(subject, html_content, plain_content):
    """
    Sends an email with the specified subject and content.
    
    Args:
        subject (str): Subject of the email.
        html_content (str): HTML content of the email.
        plain_content (str): Plain text content of the email.
    """
    try:
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
    except smtplib.SMTPException as e:
        logger.error(f"Failed to send email: {e}")

def render_email_template(template_name, context):
    """
    Renders an email template with the given context.
    
    Args:
        template_name (str): The name of the template file.
        context (dict): Context data for template rendering.

    Returns:
        str: Rendered email content.
    """
    try:
        env = Environment(loader=FileSystemLoader(Config.TEMPLATE_DIR))
        template = env.get_template(template_name)
        return template.render(context)
    except Exception as e:
        logger.error(f"Error rendering template '{template_name}': {e}")
        return ""

# Example function to demonstrate usage
def notify_domain_expiration(expiration_type, domain, days_until_expire):
    """
    Sends a notification email about domain or SSL expiration.

    Args:
        expiration_type (str): Type of expiration (e.g., 'SSL' or 'domain registration').
        domain (str): Domain name being monitored.
        days_until_expire (int): Number of days until expiration.
    """
    context = prepare_email_context(expiration_type, domain, days_until_expire)
    subject = context['subject']
    html_content = render_email_template(Config.EMAIL_TEMPLATE_HTML, context)
    plain_content = render_email_template(Config.EMAIL_TEMPLATE_PLAIN, context)
    
    send_email(subject, html_content, plain_content)
