from domain_operations import gather_all_domains
from notifications import send_notification, render_email_template
from logger import setup_logger
from config import Config, ADDITIONAL_DOMAINS
import time

logger = setup_logger()


def gather_all_domains():
    """
    Gathers all domains from Webmin and additional domains specified in the environment variables.

    Returns:
        list: A list of unique domains to monitor.
    """
    try:
        domains = get_domains_from_webmin()
        additional_domains = [domain.strip() for domain in ADDITIONAL_DOMAINS if domain]
        unique_domains = list(set(domains + additional_domains))
        return unique_domains
    except Exception as e:
        logger.error(f"Error gathering domains: {e}")
        return []


def notify_domain_expiration(expiration_type, domain, days_until_expire):
    """
    Sends a notification email about domain or SSL expiration.

    Args:
        expiration_type (str): Type of expiration (e.g., 'SSL' or 'domain registration').
        domain (str): Domain name being monitored.
        days_until_expire (int): Number of days until expiration.
    """
    try:
        context = prepare_email_context(expiration_type, domain, days_until_expire)
        subject = context['subject']
        html_content = render_email_template(Config.EMAIL_TEMPLATE_HTML, context)
        plain_content = render_email_template(Config.EMAIL_TEMPLATE_PLAIN, context)
        send_notification(subject, html_content, plain_content)
    except Exception as e:
        logger.error(f"Error notifying domain expiration: {e}")


def prepare_email_context(expiration_type, domain, days_until_expire):
    """
    Prepares the context for an email notification.

    Args:
        expiration_type (str): Type of expiration (e.g., 'SSL' or 'domain registration').
        domain (str): Domain name being monitored.
        days_until_expire (int): Number of days until expiration.

    Returns:
        dict: Context dictionary for rendering email templates.
    """
    return {
        'subject': f"{expiration_type} expiration warning for {domain}",
        'domain': domain,
        'days_until_expire': days_until_expire,
        'logo_url': Config.LOGO_URL,
        'support_url': Config.SUPPORT_URL
    }


def monitor_domains():
    """
    Monitors domains for SSL and domain registration expiration and sends notifications as needed.
    """
    while True:
        try:
            domains = gather_all_domains()
            for domain in domains:
                days_until_expire = check_domain_expiration(domain)
                if days_until_expire <= Config.DOMAIN_EXPIRATION_ALERT_DAYS:
                    notify_domain_expiration('domain registration', domain, days_until_expire)
                ssl_days_until_expire = check_ssl_expiration(domain)
                if ssl_days_until_expire <= Config.SSL_ALERT_DAYS:
                    notify_domain_expiration('SSL', domain, ssl_days_until_expire)
            time.sleep(Config.CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"Error during domain monitoring: {e}")


if __name__ == "__main__":
    monitor_domains()
