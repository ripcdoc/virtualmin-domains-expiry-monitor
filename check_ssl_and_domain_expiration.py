# Import necessary Python modules
from dotenv import load_dotenv
import os
import logging
import logging.handlers
import requests
from datetime import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor
import multiprocessing  # To get the number of CPU cores
import smtplib  # For sending email alerts
import sys

# Load environment variables from .env file
load_dotenv()

# Validate required environment variables
required_vars = ['WEBMIN_SERVERS', 'WEBMIN_USERS', 'WEBMIN_PASSWORDS', 'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USER', 'EMAIL_PASSWORD', 'EMAIL_RECIPIENTS']
for var in required_vars:
    if not os.getenv(var):
        logging.error(f"Environment variable {var} is missing. Please check the configuration.")
        sys.exit(1)

# Replace with your Webmin server URLs (credentials are pulled from environment variables)
webmin_servers = os.getenv('WEBMIN_SERVERS').split(',')
webmin_users = os.getenv('WEBMIN_USERS').split(',')
webmin_passwords = os.getenv('WEBMIN_PASSWORDS').split(',')

# SSL and domain expiration configuration (loaded from environment variables)
DOMAIN_FILE = os.getenv('DOMAIN_FILE', 'domains.txt')
SSL_ALERT_DAYS = int(os.getenv('SSL_ALERT_DAYS', 15))  # Days before SSL certificate expiration to alert
DOMAIN_EXPIRATION_ALERT_DAYS = int(os.getenv('DOMAIN_EXPIRATION_ALERT_DAYS', 45))  # Days before domain expiration to alert

# Email configuration (loaded from environment variables)
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS').split(',')

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the root logger level to DEBUG

# Create a rotating file handler
log_file = os.getenv('LOG_FILE', 'webmin_domains.log')
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=102400, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)

# Determine max_workers dynamically based on CPU cores
cpu_cores = multiprocessing.cpu_count()
max_workers = cpu_cores * 2  # Typically, 2 times the number of CPU cores is good for I/O bound tasks

# Function to fetch domains from Webmin API
def get_domains(webmin_url, user, password):
    try:
        response = requests.get(f"{webmin_url}/virtual-server/remote.cgi?program=list-domains&name-only",
                               auth=(user, password))
        response.raise_for_status()  # Raise an exception for error status codes
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching domains from {webmin_url}: {e}")
        return []

# Function to update domains.txt
def update_domains_file(domains):
    with open(DOMAIN_FILE, "w") as f:
        for domain in domains:
            f.write(f"{domain}\n")

# Function to check SSL certificate expiration
def check_ssl_expiration(domain):
    try:
        result = subprocess.run(
            ["openssl", "s_client", "-connect", f"{domain}:443", "-servername", domain],
            input="",
            capture_output=True,
            text=True,
            timeout=10
        )
        for line in result.stdout.splitlines():
            if "notAfter=" in line:
                expire_date_str = line.split('=')[1].strip()
                expire_date = datetime.strptime(expire_date_str, "%b %d %H:%M:%S %Y %Z")
                days_until_expire = (expire_date - datetime.now()).days
                if days_until_expire <= SSL_ALERT_DAYS:
                    logger.warning(f"SSL certificate for {domain} expires in {days_until_expire} days!")
                    send_email(domain, "ssl_expiration", days_until_expire)
                logger.info(f"Checked SSL certificate for {domain}: {days_until_expire} days remaining.")
    except Exception as e:
        logger.error(f"Error checking SSL for {domain}: {e}")

# Function to check domain registration expiration
def check_domain_expiration(domain):
    try:
        result = subprocess.run(
            ["whois", domain],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Attempt to extract the expiration date using common keywords
        keywords = ["Expiry Date", "Expiration Date"]
        expire_date = None
        for keyword in keywords:
            for line in result.stdout.splitlines():
                if keyword in line:
                    expire_date_str = line.split(":")[1].strip()
                    try:
                        expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d")
                        break  # Found a valid date
                    except ValueError:
                        # Try other formats (e.g., %b %d %Y)
                        try:
                            expire_date = datetime.strptime(expire_date_str, "%b %d %Y")
                            break
                        except ValueError:
                            logger.warning(f"Could not parse expiration date for {domain}: {expire_date_str}")

        if expire_date:
            days_until_expire = (expire_date - datetime.now()).days
            if days_until_expire <= DOMAIN_EXPIRATION_ALERT_DAYS:
                logger.warning(f"Domain {domain} registration expires in {days_until_expire} days!")
                send_email(domain, "domain_expiration", days_until_expire)
            logger.info(f"Checked domain registration for {domain}: {days_until_expire} days remaining.")
        else:
            logger.warning(f"Could not find expiration date for {domain}")

    except Exception as e:
        logger.error(f"Error checking domain expiration for {domain}: {e}")

# Function to send an email alert
def send_email(domain, expiration_type, days_until_expire):
    subject = os.getenv(f"EMAIL_SUBJECT_{expiration_type}")
    message_template = os.getenv(f"EMAIL_MESSAGE_{expiration_type}")
    
    if not subject or not message_template:
        logger.error(f"Email subject or message template for {expiration_type} is missing. Please check the configuration.")
        return
    
    message = message_template.format(domain=domain, days_until_expire=days_until_expire)
    
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_USER, EMAIL_RECIPIENTS, f"Subject: {subject}\n\n{message}")
            logger.info("Email sent successfully.")
    except Exception as e:
        logger.error(f"Error sending email: {e}")

# Main function to run the daily check
def main():
    all_domains = []

    # Fetch domains from each Webmin server and update domains.txt
    for i, webmin_url in enumerate(webmin_servers):
        domains = get_domains(webmin_url, webmin_users[i], webmin_passwords[i])
        if domains:
            all_domains.extend(domains)

    # Remove duplicates and update the local domain file
    all_domains = list(set(all_domains))
    update_domains_file(all_domains)

    # Run domain checks in parallel with dynamic thread allocation
    if os.path.exists(DOMAIN_FILE):
        with open(DOMAIN_FILE, "r") as f:
            domains = [domain.strip() for domain in f if domain.strip()]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(check_ssl_expiration, domains)
            executor.map(check_domain_expiration, domains)

if __name__ == "__main__":
    main()
