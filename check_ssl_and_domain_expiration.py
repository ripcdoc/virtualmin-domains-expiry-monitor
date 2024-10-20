import logging
import logging.handlers
import requests
import os
from datetime import datetime, timedelta
import subprocess

# Replace with your Webmin server URLs and credentials
webmin_servers = ["http://server1:10000", "http://server2:10000"]
webmin_users = ["username1", "username2"]
webmin_passwords = ["password1", "password2"]

# SSL and domain expiration configuration
DOMAIN_FILE = "domains.txt"
SSL_ALERT_DAYS = 15  # Days before SSL certificate expiration to alert
DOMAIN_EXPIRATION_ALERT_DAYS = 45  # Days before domain expiration to alert

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the root logger level to DEBUG

# Create a rotating file handler
handler = logging.handlers.RotatingFileHandler("webmin_domains.log", maxBytes=102400, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)

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
        for line in result.stdout.splitlines():
            if "Expiry Date" in line or "Expiration Date" in line:
                expire_date_str = line.split(":")[1].strip()
                expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d")
                days_until_expire = (expire_date - datetime.now()).days
                if days_until_expire <= DOMAIN_EXPIRATION_ALERT_DAYS:
                    logger.warning(f"Domain {domain} registration expires in {days_until_expire} days!")
    except Exception as e:
        logger.error(f"Error checking domain expiration for {domain}: {e}")

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

    # Read updated domains from the file and check SSL/domain expiration
    if os.path.exists(DOMAIN_FILE):
        with open(DOMAIN_FILE, "r") as f:
            for domain in f:
                domain = domain.strip()
                if domain:
                    check_ssl_expiration(domain)
                    check_domain_expiration(domain)

if __name__ == "__main__":
    main()
