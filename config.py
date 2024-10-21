
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration settings for the domain expiry monitor application.
    Values are loaded from environment variables.
    """
    try:
        WEBMIN_SERVERS = os.getenv('WEBMIN_SERVERS', '').split(',')
        WEBMIN_API_KEYS = os.getenv('WEBMIN_API_KEYS', '').split(',')
        EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
        EMAIL_PORT = int(os.getenv('EMAIL_PORT', 25))
        EMAIL_USER = os.getenv('EMAIL_USER', '')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
        EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')
        SSL_ALERT_DAYS = int(os.getenv('SSL_ALERT_DAYS', 15))
        DOMAIN_EXPIRATION_ALERT_DAYS = int(os.getenv('DOMAIN_EXPIRATION_ALERT_DAYS', 45))
        DOMAIN_FILE = os.getenv('DOMAIN_FILE', 'domains.txt')
        ADDITIONAL_DOMAINS = os.getenv('ADDITIONAL_DOMAINS', '').split(',')
    except Exception as e:
        raise RuntimeError(f"Error loading configuration: {e}")
