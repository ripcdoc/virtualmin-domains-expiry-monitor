import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for the Webmin Domain and SSL Expiry Monitoring Script.
    Loads environment variables and provides default values where applicable.
    """
    def load_env_var(name, default_value, cast_type=str):
        """
        Helper function to load an environment variable and cast it to the appropriate type.
        """
        try:
            return cast_type(os.getenv(name, default_value))
        except ValueError:
            raise RuntimeError(f"Invalid value for {name}")

    WEBMIN_SERVERS = os.getenv('WEBMIN_SERVERS', '').split(',')
    WEBMIN_API_KEYS = os.getenv('WEBMIN_API_KEYS', '').split(',')
    EMAIL_HOST = load_env_var('EMAIL_HOST', 'localhost')
    EMAIL_PORT = load_env_var('EMAIL_PORT', 587, int)
    EMAIL_USER = load_env_var('EMAIL_USER', '')
    EMAIL_PASSWORD = load_env_var('EMAIL_PASSWORD', '')
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')
    SSL_ALERT_DAYS = load_env_var('SSL_ALERT_DAYS', 15, int)
    DOMAIN_EXPIRATION_ALERT_DAYS = load_env_var('DOMAIN_EXPIRATION_ALERT_DAYS', 45, int)
    DOMAIN_FILE = load_env_var('DOMAIN_FILE', 'domains.txt')
    MAX_RETRIES = load_env_var('MAX_RETRIES', 5, int)
    RETRY_WAIT = load_env_var('RETRY_WAIT', 5, int)
    LOG_FILE = load_env_var('LOG_FILE', 'webmin_domains.log')
    ERROR_ALERT_THRESHOLD = load_env_var('ERROR_ALERT_THRESHOLD', 3, int)
    ERROR_ALERT_INTERVAL = load_env_var('ERROR_ALERT_INTERVAL', 86400, int)
    TEMPLATE_DIR = load_env_var('TEMPLATE_DIR', './templates')
    EMAIL_TEMPLATE_HTML = load_env_var('EMAIL_TEMPLATE_HTML', 'email_html.j2')
    EMAIL_TEMPLATE_PLAIN = load_env_var('EMAIL_TEMPLATE_PLAIN', 'email_plain.j2')
    CHECK_INTERVAL = load_env_var('CHECK_INTERVAL', 86400, int)
    LOGO_URL = load_env_var('LOGO_URL', 'https://example.com/logo.png')
    SUPPORT_URL = load_env_var('SUPPORT_URL', 'https://example.com/support')
    ADDITIONAL_DOMAINS = os.getenv('ADDITIONAL_DOMAINS', '').split(',')
