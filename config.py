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
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 5))
    RETRY_WAIT = int(os.getenv('RETRY_WAIT', 5))
    LOG_FILE = os.getenv('LOG_FILE', 'webmin_domains.log')
    ERROR_ALERT_THRESHOLD = int(os.getenv('ERROR_ALERT_THRESHOLD', 3))
    ERROR_ALERT_INTERVAL = int(os.getenv('ERROR_ALERT_INTERVAL', 86400))
    TEMPLATE_DIR = os.getenv('TEMPLATE_DIR', './templates')
    EMAIL_TEMPLATE_HTML = os.getenv('EMAIL_TEMPLATE_HTML', 'email_html.j2')
    EMAIL_TEMPLATE_PLAIN = os.getenv('EMAIL_TEMPLATE_PLAIN', 'email_plain.j2')
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 86400))
    LOGO_URL = os.getenv('LOGO_URL', 'https://example.com/logo.png')
    SUPPORT_URL = os.getenv('SUPPORT_URL', 'https://example.com/support')
    # Variable for additional domains
    # ADDITIONAL_DOMAINS = os.getenv('ADDITIONAL_DOMAINS', '').split(',')
    
