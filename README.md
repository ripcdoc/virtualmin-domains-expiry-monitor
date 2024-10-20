# Webmin Domain and SSL Monitoring Script

![Webmin Monitor Logo](./expiry-monitor-logo.webp)

## Overview

This Python script is designed to help administrators monitor the expiration of SSL certificates and domain registrations for domains managed by Webmin/Virtualmin servers. The script interacts with the Webmin API, fetches the list of domains, checks their SSL and domain registration expiration dates, and logs warnings if they are close to expiry. It also updates a local file (`domains.txt`) to keep track of current domains and logs any changes.

## Features

- **Fetch Domain List from Webmin API**: Automatically retrieves the list of domains from one or more Webmin servers using the Webmin API.
- **SSL Certificate Expiration Check**: Checks the SSL certificate expiration date for each domain and logs a warning if the certificate is within a configurable number of days (default is 15 days).
- **Domain Registration Expiration Check**: Verifies the domain registration expiration and logs a warning if the registration is within a configurable number of days (default is 45 days).
- **Automatic Domain Management**: Updates the local domain file (`domains.txt`) by adding new domains and removing deleted ones.
- **Email Notifications**: Sends email notifications to configured recipients if SSL certificates or domains are about to expire.
- **Configurable**: Uses environment variables for easy customization.
- **Logging**: Logs all events, including SSL and domain checks, additions, and removals, as well as any errors encountered during execution.

## Why Use This Script?

- **Proactive Monitoring**: Get alerted well in advance of SSL or domain expiration to prevent downtime, security risks, or unexpected loss of domain ownership.
- **Automated Updates**: Save time by automatically syncing the domain list from Webmin, removing the need for manual domain management.
- **Flexible and Extendable**: The Python script is written in a modular way, making it easy to customize for specific needs or to add additional features.
- **Simple to Use**: With basic Python knowledge, users can easily set up and run this script, making it a valuable tool for administrators managing Webmin servers.

## Prerequisites

Before using the script, make sure you have the following prerequisites:

1. **Python 3.6+**: Ensure Python is installed on your machine. You can check this by running:
   ```bash
   python --version
