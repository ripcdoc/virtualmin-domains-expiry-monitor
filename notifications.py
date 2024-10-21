import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from config import Config
from logger import setup_logger

logger = setup_logger()


def send_notification(subject, html_content, plain_content):
    """
    Sends an email notification.

    Args:
        subject (str): Subject of the email.
        html_content (str): HTML formatted email content.
        plain_content (str): Plain text formatted email content.
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
    except TemplateNotFound:
        logger.error(f"Template '{template_name}' not found.")
        return ""
    except Exception as e:
        logger.error(f"Error rendering template '{template_name}': {e}")
        return ""


if __name__ == "__main__":
    context = {
        'subject': "Test Email Subject",
        'domain': "example.com",
        'days_until_expire': 10,
        'logo_url': Config.LOGO_URL,
        'support_url': Config.SUPPORT_URL
    }
    html_content = render_email_template(Config.EMAIL_TEMPLATE_HTML, context)
    plain_content = render_email_template(Config.EMAIL_TEMPLATE_PLAIN, context)
    send_notification(context['subject'], html_content, plain_content)
