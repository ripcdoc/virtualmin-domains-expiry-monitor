# Webmin Domain and SSL Monitoring Script with Jinja2, Improved API Error Handling, and Persistent Error Alerts

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
from jinja2 import Environment, FileSystemLoader, select_autoescape
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
    """Custom exception for Webmin authentication errors (e.g., 401 Unauthorized)."""
    pass

class WebminServerError(Exception):
    """Custom exception for Webmin server errors (e.g., 500 Internal Server Errors)."""
    pass

class WebminConnectionError(Exception):
    """Custom exception for Webmin connection errors (e.g., timeouts, request errors)."""
    pass

@retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=1, min=RETRY_WAIT, max=10))
def get_domains(webmin_url, api_key):
    """
    Fetches domains from a Webmin server using the API key, with improved error handling.

    Parameters:
    - webmin_url (str): The URL of the Webmin server.
    - api_key (str): The API key for authentication.

    Returns:
    - list: A list of domains retrieved from the Webmin server.
    """
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
        
        try:
            domains = response.text.splitlines()
            if not domains:
                logger.warning(f"Empty domain list received from {webmin_url}.")
            return domains

        except Exception as e:
            logger.error(f"Error parsing domain list from {webmin_url}: {e}")
            return []

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
    """
    Sends an email alert for persistent errors.

    Parameters:
    - webmin_url (str): The Webmin server URL.
    - error_type (str): The type of error (e.g., "Unauthorized Access").
    - error_message (str): The detailed error message.
    """
    subject = f"Persistent Error Alert: {error_type} on {webmin_url}"

    html_template = template_env.get_template(EMAIL_TEMPLATE_HTML)
    html_content = html_template.render(
        subject=subject,
        domain=webmin_url,
        expiration_type=error_type,
        days_until_expire="N/A"
    )

    plain_template = template_env.get_template(EMAIL_TEMPLATE_PLAIN)
    plain_content = plain_template.render(
        subject=subject,
        domain=webmin_url,
        expiration_type=error_type,
        days_until_expire="N/A"
    )

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
    """
    Updates the domains.txt file with the provided list of domains.

    Parameters:
    - domains (list): A list of domains to write to the file.
    """
    with open(DOMAIN_FILE, "w") as f:
        for domain in domains:
            f.write(f"{domain}\n")

def send_email(domain, expiration_type, days_until_expire):
    """
    Sends an email alert using Jinja2 templates.

    Parameters:
    - domain (str): The domain name.
    - expiration_type (str): The type of expiration (e.g., "SSL", "domain registration").
    - days_until_expire (int): Number of days left until expiration.
    """
    subject = f"{expiration_type.capitalize()} Expiration Alert: {domain}"

    html_template = template_env.get_template(EMAIL_TEMPLATE_HTML)
    html_content = html_template.render(
        subject=subject,
        domain=domain,
        expiration_type=expiration_type,
        days_until_expire=days_until_expire
    )

    plain_template = template_env.get_template(EMAIL_TEMPLATE_PLAIN)
    plain_content = plain_template.render(
        subject=subject,
        domain=domain,
        expiration_type=expiration_type,
        days_until_expire=days_until_expire
    )

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
    """
    Main function to execute the monitoring tasks.

    - Fetches domains from the configured Webmin servers.
    - Updates the local domain list.
    """
    all_domains = []

    # Fetch domains from each Webmin server using corresponding API key
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

    # Remove duplicates and update the local domain file
    all_domains = list(set(all_domains))
    update_domains_file(all_domains)

if __name__ == "__main__":
    main()
