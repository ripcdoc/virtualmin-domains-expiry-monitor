import os
import requests
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


def write_domains_to_file(domains):
    """
    Writes a list of domains to the specified domain file.

    Args:
        domains (list): A list of domains to write to the file.
    """
    try:
        with open(Config.DOMAIN_FILE, 'w') as file:
            for domain in domains:
                file.write(f"{domain}\n")
    except Exception as e:
        logger.error(f"Error writing domains to file: {e}")


def get_domains_from_webmin():
    """
    Retrieves domains from Webmin servers using the API.

    Returns:
        list: A list of domains retrieved from Webmin servers.
    """
    domains = []
    for server, api_key in zip(Config.WEBMIN_SERVERS, Config.WEBMIN_API_KEYS):
        if server and api_key:
            try:
                response = requests.get(
                    f"https://{server}/virtual-server/remote.cgi",
                    params={
                        'program': 'list-domains',
                        'multiline': '',
                        'json': ''
                    },
                    headers={
                        'Authorization': f"Bearer {api_key}"
                    },
                    verify=False  # Note: In a production environment, set up proper SSL verification
                )
                response.raise_for_status()
                data = response.json()
                domains += [domain['name'] for domain in data.get('domains', [])]
            except requests.RequestException as e:
                logger.error(f"Error fetching domains from Webmin server '{server}': {e}")
    return domains


def get_domains():
    """
    Retrieves all domains from the domain file, adds additional domains from Webmin API, and adds additional domains from environment variables.
    Updates the domain file with all gathered domains.

    Returns:
        list: A list of unique domains.
    """
    try:
        domains_from_file = read_domains_from_file()
        domains_from_webmin = get_domains_from_webmin()
        additional_domains = [domain.strip() for domain in ADDITIONAL_DOMAINS if domain]
        all_domains = list(set(domains_from_file + domains_from_webmin + additional_domains))

        # Write the consolidated list back to the domain file
        write_domains_to_file(all_domains)

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
