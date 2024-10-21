
"""
domain_monitor.py

This script is the main entry point for monitoring domain and SSL certificate expirations.
It runs continuously and checks domains in batches, sending notifications when expirations
are approaching. It utilizes threading for concurrent processing and handles rate limiting.
"""

from domain_operations import get_domains, check_domain_expiration, check_ssl_expiration
from notifications import send_notification, render_email_template
from logger import setup_logger
from config import Config
from exceptions import DomainFetchError, SSLCertificateError, NotificationError
import time
import threading

logger = setup_logger()

def notify_domain_expiration(expiration_type, domain, days_until_expire):
    """
    Sends a notification email about domain or SSL expiration.

    Parameters:
    - expiration_type (str): Type of expiration ('domain' or 'SSL').
    - domain (str): Domain name being monitored.
    - days_until_expire (int): Number of days until expiration.

    Raises:
    - NotificationError: If there is an issue with sending the notification.
    """
    try:
        context = prepare_email_context(expiration_type, domain, days_until_expire)
        html_content = render_email_template('email_html.j2', context)
        plain_content = render_email_template('email_plain.j2', context)
        send_notification(f'{expiration_type} Expiry Alert: {domain}', html_content, plain_content)
        logger.info(f'Notification sent for {expiration_type} expiration: {domain}')
    except NotificationError as e:
        logger.error(f'Notification failed for {expiration_type} expiration: {domain}. Error: {e}')

def check_domains_concurrently(domains):
    """
    Checks domain expiration concurrently using threading.

    Parameters:
    - domains (list): List of domain names to check.

    Each domain is checked in a separate thread to enhance performance and reduce
    processing time for larger lists of domains. Exception handling ensures errors
    do not propagate across threads.
    """
    threads = []
    for domain in domains:
        try:
            t = threading.Thread(target=check_domain_expiration, args=(domain,))
            t.start()
            threads.append(t)
        except DomainFetchError as e:
            logger.error(f'Error fetching domain data for {domain}: {e}')
        except SSLCertificateError as e:
            logger.error(f'SSL certificate error for {domain}: {e}')

    for t in threads:
        t.join()

def main():
    """
    Main loop for continuous domain monitoring.

    This function runs indefinitely, checking domains at regular intervals.
    It uses batch processing and rate limiting to prevent API overload.
    """
    while True:
        try:
            domains = get_domains()
            if domains:
                check_domains_concurrently(domains)
            else:
                logger.warning("No domains found to monitor.")
        except DomainFetchError as e:
            logger.error(f'Error fetching domains: {e}')

        # Wait for the specified interval before the next check
        time.sleep(Config.CHECK_INTERVAL)

if __name__ == '__main__':
    main()
