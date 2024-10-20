
import requests
from config import Config

def get_domains(webmin_url, api_key):
    headers = {'Authorization': f"Bearer {api_key}", 'Accept': 'application/json'}
    try:
        response = requests.get(
            f"{webmin_url}/virtual-server/remote.cgi?program=list-domains&name-only",
            headers=headers, timeout=10, verify=False
        )
        response.raise_for_status()
        return response.text.splitlines()
    except requests.RequestException as e:
        return []

def gather_all_domains():
    all_domains = []

    # Fetch domains from Webmin servers
    for i, webmin_url in enumerate(Config.WEBMIN_SERVERS):
        domains = get_domains(webmin_url, Config.WEBMIN_API_KEYS[i])
        all_domains.extend(domains)

    # Include additional domains from the environment variable
    if Config.ADDITIONAL_DOMAINS:
        all_domains.extend([domain.strip() for domain in Config.ADDITIONAL_DOMAINS if domain.strip()])

    # Ensure the domain list is unique
    all_domains = list(set(all_domains))
    return all_domains
