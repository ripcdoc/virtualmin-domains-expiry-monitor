
import requests
from config import Config
import logging

logger = logging.getLogger(__name__)

def get_domains(webmin_url, api_key):
    """
    Retrieves a list of domains from the specified Webmin server.
    
    Args:
        webmin_url (str): URL of the Webmin server.
        api_key (str): API key for authentication.

    Returns:
        list: List of domain names or an empty list if an error occurs.
    """
    headers = {'Authorization': f"Bearer {api_key}", 'Accept': 'application/json'}
    try:
        response = requests.get(
            f"{webmin_url}/virtual-server/remote.cgi?program=list-domains&name-only",
            headers=headers, timeout=10, verify=True
        )
        response.raise_for_status()
        return response.text.splitlines()
    except requests.RequestException as e:
        logger.error(f"Error retrieving domains from {webmin_url}: {e}")
        return []

def gather_all_domains():
    """
    Aggregates domains from all Webmin servers and additional sources.

    Returns:
        list: Unique list of all domains.
    """
    all_domains = []

    # Fetch domains from Webmin servers
    for i, webmin_url in enumerate(Config.WEBMIN_SERVERS):
        try:
            domains = get_domains(webmin_url, Config.WEBMIN_API_KEYS[i])
            all_domains.extend(domains)
        except IndexError:
            logger.error(f"API key missing for server {webmin_url}")

    # Include additional domains from environment variables
    if Config.ADDITIONAL_DOMAINS:
        all_domains.extend([domain.strip() for domain in Config.ADDITIONAL_DOMAINS if domain.strip()])

    # Ensure the domain list is unique
    return list(set(all_domains))

