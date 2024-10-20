# Webmin Domain and SSL Monitoring Script (Modified for Multiple API Keys)

"""
Webmin Domain and SSL Monitoring Script

This script monitors SSL certificates and domain registration expirations for domains managed by Webmin/Virtualmin servers.
It uses the Webmin API keys for authentication, with a separate API key for each Webmin server.
"""

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
from tenacity import retry, stop_after_attempt, wait_fixed
import sys

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

# Replace with your Webmin server URLs and corresponding API keys
webmin_servers = os.getenv('WEBMIN_SERVERS').split(',')
webmin_api_keys = os.getenv('WEBMIN_API_KEYS').split(',')

if len(webmin_servers) != len(webmin_api_keys):
    logging.error("The number of Webmin servers must match the number of API keys. Please check the configuration.")
    sys.exit(1)

# SSL and domain expiration configuration (loaded from environment variables)
DOMAIN_FILE = os.getenv('DOMAIN_FILE', 'domains.txt')
SSL_ALERT_DAYS = int(os.getenv('SSL_ALERT_DAYS', 15))
DOMAIN_EXPIRATION_ALERT_DAYS = int(os.getenv('DOMAIN_EXPIRATION_ALERT_DAYS', 45))

# Email configuration (loaded from environment variables)
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS').split(',')

# Retry configuration
MAX_RETRIES = int(os.geten
