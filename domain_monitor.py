"""
domain_monitor.py

This script is the main entry point for monitoring domain and SSL certificate expirations.
It runs continuously and checks domains in batches, sending notifications when expirations
are approaching. It utilizes threading for concurrent processing and handles rate limiting.

New functionality has been added to automatically calculate the optimal batch size based on 
user-defined parameters such as API rate limits, processing time, and delays between batches.
"""

import os
import math
import time
import threading
from dotenv import load_dotenv

from domain_operations import get_domains, check_domain_expiration, check_ssl_expiration
from notifications import send_notification, render_email_template
from logger import setup_logger
from config import Config
from exceptions import DomainFetchError, SSLCertificateError, NotificationError

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logger()

# Get environment variables or set defaults
# BATCH_SIZE (optional): Overrides dynamic calculation if set manually
batch_size_env = os.getenv('BATCH_SIZE', None)

# API rate limit: Maximum number of allowed requests per interval
api_rate_limit = int(os.getenv('API_RATE_LIMIT', '100'))  # Default: 100 requests/minute

# Rate limit interval: Duration of the rate limit interval in seconds
rate_limit_interval = int(os.getenv('RATE_LIMIT_INTERVAL', '60'))  # Default: 60 seconds

# Average processing time: Average time to check each domain, in seconds
avg_processing_time = float(os.getenv('AVG_PROCESSING_TIME', '0.5'))  # Default: 0.5 seconds

# Delay between batches: Delay in seconds between processing each batch of domains
delay_between_batches = int(os.getenv('BATCH_DELAY', '2'))  # Default: 2 seconds

# Maximum allowed batch size: Upper limit for batch size to prevent server overload
max_batch_size = int(os.getenv('MAX_BATCH_SIZE', '20'))  # Default: 20

# Calculate the optimal batch size based on the defined parameters
# Formula: B = min(floor(R / ((T_d + T_s) / T_i)), Max_B)
optimal_batch_size = min(
    math.floor(api_rate_limit / ((delay_between_batches + avg_processing_time) / rate_limit_interval)),
    max_batch_size
)

# Determine the final batch size to use
# If BATCH_SIZE is set manually, it overrides the calculated value
batch_size = int(batch_size_env) if batch_size_env else optimal_batch_size

# Output the batch size for debugging
logger.info(f"Calculated optimal batch size: {optimal_batch_size}")
if batch_size_env:
    logger.info(f"Using batch size: {batch_size} (overridden by BATCH_SIZE env variable)")
else:
    logger.info(f"Using batch size: {batch_size} (calculated)")

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

    The batch size is dynamically calculated or manually set, affecting how many
    domains are checked concurrently in each batch.
    """
    threads = []
    for i in range(0, len(domains), batch_size):
        batch = domains[i:i + batch_size]
        for domain in batch:
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

        # Add delay between batches
        if delay_between_batches > 0 and i + batch_size < len(domains):
            logger.info(f"Waiting for {delay_between_batches} seconds before next batch...")
            time.sleep(delay_between_batches)

def main():
    """
    Main loop for continuous domain monitoring.

    This function runs indefinitely, checking domains at regular intervals.
    It uses batch processing and rate limiting to prevent API overload.

    The batch size can be dynamically adjusted or manually set based on configuration.
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
