
"""
domain_operations.py

This module handles domain-related operations, including checking domain and SSL certificate
expirations. It uses HTTP requests to interact with external APIs and reads domain data from files.
Error handling ensures robust processing for different types of failures.
"""

import os
import requests
from config import Config
from logger import setup_logger
from exceptions import DomainFetchError, SSLCertificateError

logger = setup_logger()

def read_domains_from_file():
    """
    Reads domain names from the specified file.

    Returns:
    - list: List of domain names read from the file.

    Raises:
    - DomainFetchError: If the file cannot be found or read.
    """
    try:
        domains = []
        with open(Config.DOMAIN_FILE, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
        return domains
    except FileNotFoundError:
        raise DomainFetchError(f"Domain file not found: {Config.DOMAIN_FILE}")
    except Exception as e:
        raise DomainFetchError(f"Unexpected error reading domain file: {e}")

def check_domain_expiration(domain):
    """
    Checks the expiration date of a given domain.

    Parameters:
    - domain (str): The domain name to check.

    Returns:
    - str: Expiration date of the domain.

    Raises:
    - DomainFetchError: If the API request fails or the response is invalid.
    """
    try:
        response = requests.get(f"https://api.example.com/domain/{domain}/expiration")
        if response.status_code != 200:
            raise DomainFetchError(f"Failed to fetch expiration data for {domain}")
        data = response.json()
        return data.get("expiration_date")
    except requests.RequestException as e:
        raise DomainFetchError(f"HTTP error while fetching domain data for {domain}: {e}")

def check_ssl_expiration(domain):
    """
    Checks the SSL certificate expiration date of a given domain.

    Parameters:
    - domain (str): The domain name to check.

    Returns:
    - str: SSL certificate expiration date.

    Raises:
    - SSLCertificateError: If the API request fails or the response is invalid.
    """
    try:
        response = requests.get(f"https://api.example.com/domain/{domain}/ssl")
        if response.status_code != 200:
            raise SSLCertificateError(f"Failed to fetch SSL data for {domain}")
        data = response.json()
        return data.get("ssl_expiration_date")
    except requests.RequestException as e:
        raise SSLCertificateError(f"HTTP error while fetching SSL data for {domain}: {e}")
