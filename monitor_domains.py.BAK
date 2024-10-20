__version__ = "1.0.7"  # Initial Released Version

from dotenv import load_dotenv
import os
import logging
import logging.handlers
import requests
from datetime import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tenacity import retry, stop_after_attempt, wait_exponential
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from requests.exceptions import HTTPError, Timeout, RequestException
import sys
import time

# Load environment variables from .env file
load_dotenv()

# Validate required environment variables
required_vars = [
    'WEBMIN_SERVERS', 'WEBMIN_API_KEYS', 'EMAIL_HOST', 
    'EMAIL_PORT', 'EMAIL_USER', 'EMAIL_PASSWORD', 'EMAIL_RECIPIENTS'
]
for var in required_vars:
    if not os.getenv(var):
        logging.error(f"Environment variable {var} is missing. Please check the configuration.")
        sys.exit(1)

# Initialize Webmin server URLs and corresponding API keys
webmin_servers = os.getenv('WEBMIN_SERVERS').split(',')
webmin_api_keys = os.getenv('WEBMIN_API_KEYS').split(',')

if len(webmin_servers) != len(webmin_api_keys):
    logging.error("The number of Webmin servers must match the number of API keys. Please check the configuration.")
    sys.exit(1)

# SSL and domain expiration configuration
DOMAIN_FILE = os.getenv('DOMAIN_FILE', 'domains.txt')
SSL_ALERT_DAYS = int(os.getenv('SSL_ALERT_DAYS', 15))
DOMAIN_EXPIRATION_ALERT_DAYS = int(os.getenv('DOMAIN_EXPIRATION_ALERT_DAYS', 45))

# Email configuration
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS').split(',')

# Retry configuration
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 5))
RETRY_WAIT = int(os.getenv('RETRY_WAIT', 5))

# Persistent error alert configuration
ERROR_ALERT_THRESHOLD = int(os.getenv('ERROR_ALERT_THRESHOLD', 3))
ERROR_ALERT_INTERVAL = int(os.getenv('ERROR_ALERT_INTERVAL', 86400))

# Template configuration
TEMPLATE_DIR = os.getenv('TEMPLATE_DIR', './templates')
EMAIL_TEMPLATE_HTML = os.getenv('EMAIL_TEMPLATE_HTML', 'email_html.j2')
EMAIL_TEMPLATE_PLAIN = os.getenv('EMAIL_TEMPLATE_PLAIN', 'email_plain.j2')

# Continuous loop configuration
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 86400))  # Default: 24 hours

# Default HTML email template
DEFAULT_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ subject }}</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 20px; }
        .content { margin-bottom: 20px; }
        .footer { text-align: center; font-size: 12px; color: #888; margin-top: 30px; }
        .btn { background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }
        .btn:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://example.com/logo.png" alt="Webmin Monitor Logo" width="100">
            <h2>{{ subject }}</h2>
        </div>
        <div class="content">
            <p><strong>Domain:</strong> {{ domain }}</p>
            <p><strong>Expiration Type:</strong> {{ expiration_type }}</p>
            <p><strong>Days Until Expiry:</strong> {{ days_until_expire }}</p>
            <p>Please take the necessary actions to renew the domain or SSL certificate to avoid service disruptions.</p>
            <a href="https://example.com/support" class="btn">Support</a>
        </div>
        <div class="footer">
            <p>&copy; 2024 Dr. Peter O'Hara-Diaz. All rights reserved.</p>
            <p>This email was generated using the default template. You can customize it by following the instructions in the <a href="https://github.com/ripcdoc/virtualmin-domains-expiry-monitor/blob/main/README.md">README</a>.</p>
        </div>
    </div>
</body>
</html>
"""

# Default plaintext email template
DEFAULT_PLAIN_TEMPLATE = """
Subject: {{ subject }}

Domain: {{ domain }}
Expiration Type: {{ expiration_type }}
Days Until Expiry: {{ days_until_expire }}

Please take the necessary actions to renew the domain or SSL certificate to avoid service disruptions.

For assistance, visit our support page: https://example.com/support

© 2024 Dr. Peter O'Hara-Diaz. All rights reserved.

This email was generated using the default template. You can customize it by following the instructions in the README: 
https://github.com/ripcdoc/virtualmin-domains-expiry-monitor/blob/main/README.md
"""

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = os.getenv('LOG_FILE', 'webmin_domains.log')
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=102400, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)

# Determine max_workers dynamically based on CPU cores
cpu_cores = multiprocessing.cpu_count()
max_workers = cpu_cores * 2

# Initialize Jinja2 environment
template_loader = FileSystemLoader(searchpath=TEMPLATE_DIR)
template_env = Environment(
    loader=template_loader,
    autoescape=select_autoescape(['html', 'xml'])
)

# Custom error classes
class WebminAuthError(Exception):
    pass

class WebminServerError(Exception):
    pass

class WebminConnectionError(Exception):
    pass

@retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=1, min=RETRY_WAIT, max=10))
def get_domains(webmin_url, api_key):
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Accept': 'application/json'
    }

    try:
        response = requests.get(
            f"{webmin_url}/virtual-server/remote.cgi?program=list-domains&name-only",
            headers=headers,
            timeout=10,
            verify=False
        )

        response.raise_for_status()

        if not response.text:
            logger.warning(f"No domains found in the response from {webmin_url}.")
            return []

        domains = response.text.splitlines()
        if not domains:
            logger.warning(f"Empty domain list received from {webmin_url}.")
        return domains

    except HTTPError as http_err:
        if response.status_code == 401:
            error_msg = f"Unauthorized access to {webmin_url}. Check API key."
            logger.error(error_msg)
            send_persistent_error_alert(webmin_url, "Unauthorized Access", error_msg)
            raise WebminAuthError(error_msg)
        elif response.status_code >= 500:
            error_msg = f"Server error {response.status_code} from {webmin_url}."
            logger.error(error_msg)
            raise WebminServerError(error_msg)
        else:
            logger.error(f"HTTP error {response.status_code} from {webmin_url}: {http_err}")
    except Timeout:
        error_msg = f"Timeout error when connecting to {webmin_url}."
        logger.error(error_msg)
        raise WebminConnectionError(error_msg)
    except RequestException as req_err:
        error_msg = f"Request error for {webmin_url}: {req_err}"
        logger.error(error_msg)
        raise WebminConnectionError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error when fetching domains from {webmin_url}: {e}"
        logger.error(error_msg)
        raise WebminConnectionError(error_msg)

    return []

def send_persistent_error_alert(webmin_url, error_type, error_message):
    subject = f"Persistent Error Alert: {error_type} on {webmin_url}"

    try:
        html_template = template_env.get_template(EMAIL_TEMPLATE_HTML)
        html_content = html_template.render(
            subject=subject,
            domain=webmin_url,
            expiration_type=error_type,
            days_until_expire="N/A"
        )
    except TemplateNotFound:
        logger.error(f"HTML template '{EMAIL_TEMPLATE_HTML}' not found. Using default template.")
        html_content = DEFAULT_HTML_TEMPLATE

    try:
        plain_template = template_env.get_template(EMAIL_TEMPLATE_PLAIN)
        plain_content = plain_template.render(
            subject=subject,
            domain=webmin_url,
            expiration_type=error_type,
            days_until_expire="N/A"
        )
    except TemplateNotFound:
        logger.error(f"Plaintext template '{EMAIL_TEMPLATE_PLAIN}' not found. Using default template.")
        plain_content = DEFAULT_PLAIN_TEMPLATE

    try:
        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = ", ".join(EMAIL_RECIPIENTS)

        msg.attach(MIMEText(plain_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_USER, EMAIL_RECIPIENTS, msg.as_string())
            logger.info("Persistent error email alert sent successfully.")
    except Exception as e:
        logger.error(f"Error sending persistent error alert: {e}")

def update_domains_file(domains):
    with open(DOMAIN_FILE, "w") as f:
        for domain in domains:
            f.write(f"{domain}\n")

def send_email(domain, expiration_type, days_until_expire):
    subject = f"{expiration_type.capitalize()} Expiration Alert: {domain}"

    try:
        html_template = template_env.get_template(EMAIL_TEMPLATE_HTML)
        html_content = html_template.render(
            subject=subject,
            domain=domain,
            expiration_type=expiration_type,
            days_until_expire=days_until_expire
        )
    except TemplateNotFound:
        logger.error(f"HTML template '{EMAIL_TEMPLATE_HTML}' not found. Using default template.")
        html_content = DEFAULT_HTML_TEMPLATE

    try:
        plain_template = template_env.get_template(EMAIL_TEMPLATE_PLAIN)
        plain_content = plain_template.render(
            subject=subject,
            domain=domain,
            expiration_type=expiration_type,
            days_until_expire=days_until_expire
        )
    except TemplateNotFound:
        logger.error(f"Plaintext template '{EMAIL_TEMPLATE_PLAIN}' not found. Using default template.")
        plain_content = DEFAULT_PLAIN_TEMPLATE

    try:
        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = ", ".join(EMAIL_RECIPIENTS)

        msg.attach(MIMEText(plain_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_USER, EMAIL_RECIPIENTS, msg.as_string())
            logger.info("Email sent successfully.")
    except Exception as e:
        logger.error(f"Error sending email: {e}")

def main():
    all_domains = []

    for i, webmin_url in enumerate(webmin_servers):
        try:
            domains = get_domains(webmin_url, webmin_api_keys[i])
            if domains:
                all_domains.extend(domains)
        except WebminAuthError:
            logger.error(f"Authorization error for server {webmin_url}. Skipping server.")
        except WebminServerError:
            logger.error(f"Server error for {webmin_url}. Skipping server.")
        except WebminConnectionError:
            logger.error(f"Connection error for {webmin_url}. Skipping server.")
        except Exception as e:
            logger.error(f"Unexpected error for {webmin_url}: {e}")

    all_domains = list(set(all_domains))
    update_domains_file(all_domains)

# Uncomment the following lines to enable continuous loop mode
# def continuous_loop():
#     while True:
#         main()
#         logger.info(f"Sleeping for {CHECK_INTERVAL} seconds before the next run.")
#         time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()  # Default single-run mode (comment this line out if enabling continuous loop mode above)
    # continuous_loop() # Uncomment this line if enabling continuous loop mode above)
