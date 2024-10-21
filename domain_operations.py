import os
from config import Config, ADDITIONAL_DOMAINS
from logger import setup_logger

logger = setup_logger()


def read_domains_from_file():
    """
    Reads domains from the specified domain file.

    Returns:
        list: A list of domains read from the file.
    """
    domains = []
    try:
        with open(Config.DOMAIN_FILE, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.error(f"Domain file '{Config.DOMAIN_FILE}' not found.")
    except Exception as e:
        logger.error(f"Error reading domains from file: {e}")
    return domains


def get_domains():
    """
    Retrieves all domains from the domain file and adds additional domains from environment variables.

    Returns:
        list: A list of unique domains.
    """
    try:
        domains = read_domains_from_file()
        additional_domains = [domain.strip() for domain in ADDITIONAL_DOMAINS if domain]
        all_domains = list(set(domains + additional_domains))
        return all_domains
    except Exception as e:
        logger.error(f"Error gathering domains: {e}")
        return []


def check_domain_expiration(domain):
    """
    Placeholder function to check domain expiration.

    Args:
        domain (str): The domain name to check.

    Returns:
        int: Days until the domain expires.
    """
    # Placeholder logic for domain expiration check
    return 30


def check_ssl_expiration(domain):
    """
    Placeholder function to check SSL certificate expiration.

    Args:
        domain (str): The domain name to check.

    Returns:
        int: Days until the SSL certificate expires.
    """
    # Placeholder logic for SSL expiration check
    return 15


if __name__ == "__main__":
    domains = get_domains()
    for domain in domains:
        logger.info(f"Domain: {domain}")
