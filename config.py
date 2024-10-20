
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WEBMIN_SERVERS = os.getenv('WEBMIN_SERVERS').split(',')
    WEBMIN_API_KEYS = os.getenv('WEBMIN_API_KEYS').split(',')
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS').split(',')
    SSL_ALERT_DAYS = int(os.getenv('SSL_ALERT_DAYS', 15))
    DOMAIN_EXPIRATION_ALERT_DAYS = int(os.getenv('DOMAIN_EXPIRATION_ALERT_DAYS', 45))
    DOMAIN_FILE = os.getenv('DOMAIN_FILE', 'domains.txt')
    
    # New variable for additional domains
    ADDITIONAL_DOMAINS = os.getenv('ADDITIONAL_DOMAINS', '').split(',')
