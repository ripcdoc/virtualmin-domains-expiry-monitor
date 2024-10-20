# Webmin Domain and SSL Monitoring Script

![Webmin Monitor Logo](./expiry-monitor-logo.webp)

## Overview

This Python script is designed to help administrators monitor the **expiration of SSL certificates** and **domain registrations** for domains managed by **Webmin/Virtualmin servers**. The script interacts with the Webmin API, fetches the list of domains, checks their SSL and domain registration expiration dates, and logs warnings if they are close to expiry. It also updates a local file (`domains.txt`) to keep track of current domains and logs any changes.

## Features

- **Fetch Domain List from Webmin API**: Automatically retrieves the list of domains from one or more Webmin servers using the Webmin API.
- **SSL Certificate Expiration Check**: Checks the SSL certificate expiration date for each domain and logs a warning if the certificate is within 15 days of expiration.
- **Domain Registration Expiration Check**: Verifies the domain registration expiration and logs a warning if the registration is within 45 days of expiration.
- **Automatic Domain Management**: Updates the local domain file (`domains.txt`) by adding new domains and removing deleted ones.
- **Logging**: Logs all events, including SSL and domain checks, additions, and removals, as well as any errors encountered during execution.
- **Configurable**: Easily configure Webmin server URLs, API credentials, and alert thresholds.

## Why Use This Script?

- **Proactive Monitoring**: Get alerted well in advance of SSL or domain expiration to prevent downtime, security risks, or unexpected loss of domain ownership.
- **Automated Updates**: Save time by automatically syncing the domain list from Webmin, removing the need for manual domain management.
- **Flexible and Extendable**: The Python script is written in a modular way, making it easy to customize for specific needs or to add additional features.
- **Simple to Use**: With basic Python knowledge, users can easily set up and run this script, making it a valuable tool for administrators managing Webmin servers.

## How It Works

**MAIN EXECUTION FLOW:**

Fetches domains from each Webmin server, removes duplicates, and updates the domain file.
Reads the updated domain list from the file and checks SSL and domain expiration for each domain.

1. **Imports Necessary Modules:**

Imports several Python modules required for network interaction (requests), subprocesses (subprocess), logging (logging), file operations (os), and date-time calculations (datetime).

2. **Configurations:**

Configures a list of Webmin servers (`webmin_servers`), along with their credentials (`webmin_users` and `webmin_passwords`).
Sets parameters for SSL certificate (`SSL_ALERT_DAYS`) and domain registration (`DOMAIN_EXPIRATION_ALERT_DAYS`) expiry notifications.

3. **Logging Setup:**

Configures a logger that writes messages to a log file (`webmin_domains.log`) with rotating capabilities to avoid excessive growth of log files.

4. **Maintain Master List of Domains**

Uses Webmin API to fetch the list of domains for each configured Webmin server.
Errors during this process are logged.
Updates a text file (`domains.txt`) containing the list of domains fetched from the Webmin servers.

5. **Check SSL Expiration:**

Uses `openssl` to check the SSL certificate of each domain and calculates the days remaining until expiry.
Logs a warning if the SSL certificate will expire soon (<= `SSL_ALERT_DAYS` days).

6. **Check Domain Registration Expiration:**

Uses the `whois` command to check the domain registration expiry date.
Logs a warning if the domain registration will expire soon (<= `DOMAIN_EXPIRATION_ALERT_DAYS` days).

1. **Fetches Domains from Webmin API**:
   - Connects to specified Webmin servers using the API and retrieves the list of managed domains.
   
2. **Updates Local Domain File (`domains.txt`)**:
   - Compares the fetched domain list with the existing local file and updates it by adding new domains and removing deleted ones.

3. **Checks SSL Certificate Expiration**:
   - Uses OpenSSL to check the expiration date of each domain`s SSL certificate.
   - Logs a warning if the SSL certificate expires within a specified number of days (default: 15 days).

4. **Checks Domain Registration Expiration**:
   - Uses the `whois` utility to determine the domain registration expiration date.
   - Logs a warning if the domain registration expires within a specified number of days (default: 45 days).

5. **Logging and Error Handling**:
   - All events and errors are logged in a rotating log file (`webmin_domains.log`) for easy monitoring and troubleshooting.
  
+-------------------------------------------+
|        Webmin Domain & SSL Monitor        |
+-------------------------------------------+

+-------------------------------------------+
|  1) Fetch Domain List from Webmin API     |
|     - Connect to Webmin servers           |
|     - Retrieve domain list                |
+-------------------------------------------+
                     |
                     v
+-------------------------------------------+
|  2) Update Local Domain File (domains.txt)|
|     - Add new domains                     |
|     - Remove deleted domains              |
+-------------------------------------------+
                     |
                     v
+-------------------------------------------+
|  3) Check SSL Certificate Expiration      |
|     - Use OpenSSL to check expiration     |
|     - Alert if SSL expires within 15 days |
+-------------------------------------------+
                     |
                     v
+-------------------------------------------+
|  4) Check Domain Registration Expiration  |
|     - Use WHOIS to check expiration       |
|     - Alert if domain expires within 45   |
|       days                                |
+-------------------------------------------+
                     |
                     v
+-------------------------------------------+
|  5) Log Results                           |
|     - Log warnings and errors to file     |
|     - Log changes to domain file          |
+-------------------------------------------+

## Requirements

- Python 3
- `requests` library (`pip3 install requests`)
- OpenSSL (`sudo apt install openssl`)
- WHOIS utility (`sudo apt install whois`)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/webmin-domain-ssl-monitor.git
   cd webmin-domain-ssl-monitor
   ```

2. **Install required Python dependencies**:
   ```bash
   pip3 install requests
   ```

3. **Edit the script to set up your Webmin server credentials and settings**:
   - Open `check_ssl_and_domain_expiration.py` and modify the following variables:
     ```python
     webmin_servers = ["http://server1:10000", "http://server2:10000"]
     webmin_users = ["username1", "username2"]
     webmin_passwords = ["password1", "password2"]
     ```
   - Adjust the SSL and domain expiration alert thresholds if needed:
     ```python
     SSL_ALERT_DAYS = 15
     DOMAIN_EXPIRATION_ALERT_DAYS = 45
     ```

4. **Run the script**:
   ```bash
   python3 check_ssl_and_domain_expiration.py
   ```

5. **(Optional) Set up a daily cron job**:
   - If you want to run the script daily, add a cron job:
     ```bash
     crontab -e
     ```
   - Add the following line to run the script daily at midnight:
     ```bash
     0 0 * * * /usr/bin/python3 /path/to/check_ssl_and_domain_expiration.py
     ```

## Configuration

### Webmin API Access
- Ensure that Webmin`s API is enabled on each server and that the API user has permission to list domains.
- API access is set up via basic authentication. Ensure the user credentials are kept secure.

### Adjusting Alert Thresholds
- You can modify the number of days for SSL and domain expiration alerts by changing the values of `SSL_ALERT_DAYS` and `DOMAIN_EXPIRATION_ALERT_DAYS` at the top of the script.

## Troubleshooting

- **Script Fails to Fetch Domains**: 
  - Check if the Webmin API is enabled and accessible from the server running the script.
  - Ensure the credentials are correct and have necessary permissions.

- **SSL or WHOIS Errors**: 
  - Ensure that OpenSSL and the WHOIS utility are installed and accessible from the command line.
  - Check if the domain in question has a valid SSL certificate and WHOIS data available.

- **Logging Issues**:
  - Ensure that the log file`s directory is writable. Adjust permissions or change the logging path if needed.

## Author

Created by **Dr. Peter O`Hara-Diaz**. This script is intended for use by system administrators to simplify the monitoring of SSL and domain expiration on Webmin-managed servers.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Feel free to fork the repository, open issues, or submit pull requests to improve the script. All contributions are welcome!

## Disclaimer

This script is provided as-is without any guarantees or warranties. Use it at your own risk and ensure it meets your requirements before using it in a production environment.
