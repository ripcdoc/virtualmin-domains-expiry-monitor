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
   ```
2. **pip**: Python's package installer. You can install it by following the [official guide](https://pip.pypa.io/en/stable/installation/).
3. **WHOIS Tool**: This script relies on the `whois` command line utility to check domain registrations. Make sure it is installed on your system.
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get install whois
     ```
   - **CentOS/RHEL**:
     ```bash
     sudo yum install whois
     ```
4. **OpenSSL**: Required for checking SSL certificates.
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get install openssl
     ```
   - **CentOS/RHEL**:
     ```bash
     sudo yum install openssl
     ```
5. **SMTP Access**: Ensure that SMTP credentials are available to allow the script to send email alerts.

## Dependencies

This script requires several Python packages to function correctly. All the necessary packages are listed in the `requirements.txt` file included in this repository. Before proceeding with the installation, ensure you have Python and `pip` installed on your system.

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

This command will install all required packages specified in the `requirements.txt` file, ensuring the script operates as intended.

## Installation

1. Clone the repository or download the script to your local machine.
   ```bash
   git clone https://github.com/ripcdoc/virtualmin-domains-expiry-monitor.git
   cd virtualmin-domains-expiry-monitor
   ```
2. Install required Python packages using the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```

## Environment Configuration

The script relies on environment variables for configuration. You need to create a `.env` file in the same directory as the script with the following variables:

### `.env` File Example
```env
# Webmin Configuration
WEBMIN_SERVERS=http://server1:10000,http://server2:10000
WEBMIN_USERS=username1,username2
WEBMIN_PASSWORDS=password1,password2

# SSL and Domain Expiration Configuration
DOMAIN_FILE=domains.txt
SSL_ALERT_DAYS=15
DOMAIN_EXPIRATION_ALERT_DAYS=45

# Logging Configuration
LOG_FILE=webmin_domains.log

# Email Configuration
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=your-email-password
EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com
EMAIL_SUBJECT_ssl_expiration=SSL Certificate Expiration Alert for {domain}
EMAIL_MESSAGE_ssl_expiration=The SSL certificate for domain {domain} will expire soon. Please take action.
EMAIL_SUBJECT_domain_expiration=Domain Registration Expiration Alert for {domain}
EMAIL_MESSAGE_domain_expiration=The domain {domain} will expire soon. Please renew it.
```

- **WEBMIN_SERVERS**: URLs of Webmin servers to monitor.
- **WEBMIN_USERS**: Corresponding usernames for Webmin servers.
- **WEBMIN_PASSWORDS**: Corresponding passwords for Webmin servers.
- **SSL_ALERT_DAYS**: Number of days before SSL expiration to trigger an alert.
- **DOMAIN_EXPIRATION_ALERT_DAYS**: Number of days before domain registration expiration to trigger an alert.
- **LOG_FILE**: File path for logging outputs.
- **Email Configuration**: SMTP settings and email templates for alerts.

## Usage

To run the script, use the following command:
```bash
python check_ssl_and_domain_expiration.py
```
The script will:
- Fetch domains from the configured Webmin servers.
- Check SSL and domain registration expiration.
- Log relevant information and send email alerts as necessary.

## Important Notes

- Make sure all environment variables are properly configured in the `.env` file.
- If any required variable is missing, the script will log an error and exit.
- Ensure that `whois` and `openssl` tools are installed and accessible in your system's PATH.

## Setting Up Dependencies

Make sure to install all required Python packages by running the following command after cloning the repository:
```bash
pip install -r requirements.txt
```
This will install:
- `requests`: For making HTTP requests to the Webmin API.
- `python-dotenv`: For loading environment variables from the `.env` file.
- `whois`: Required for performing WHOIS lookups.

## Error Handling

- The script includes checks for missing environment variables and will log an error and stop execution if any are missing.
- If SMTP credentials are incorrect, the email alert will fail. Ensure that all SMTP-related variables are properly configured.

## Logging

- Logs are written to a rotating file specified by the `LOG_FILE` environment variable.
- Logging levels can be adjusted directly in the script if necessary.

## Example Configurations

### `.env.sample`
Create a file named `.env` from the example `.env.sample` provided below:
```env
# Webmin Configuration
WEBMIN_SERVERS=http://server1:10000,http://server2:10000
WEBMIN_USERS=username1,username2
WEBMIN_PASSWORDS=password1,password2

# SSL and Domain Expiration Configuration
DOMAIN_FILE=domains.txt
SSL_ALERT_DAYS=15
DOMAIN_EXPIRATION_ALERT_DAYS=45

# Logging Configuration
LOG_FILE=webmin_domains.log

# Email Configuration
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=your-email-password
EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com
EMAIL_SUBJECT_ssl_expiration=SSL Certificate Expiration Alert for {domain}
EMAIL_MESSAGE_ssl_expiration=The SSL certificate for domain {domain} will expire soon. Please take action.
EMAIL_SUBJECT_domain_expiration=Domain Registration Expiration Alert for {domain}
EMAIL_MESSAGE_domain_expiration=The domain {domain} will expire soon. Please renew it.
```

## Troubleshooting

1. **SMTP Issues**:
   - Verify that your SMTP credentials are correct.
   - Ensure that your email provider allows third-party applications to send emails.
2. **WHOIS Command Issues**:
   - If the WHOIS command isn't working, ensure it is installed and accessible in the system's PATH.
3. **OpenSSL Issues**:
   - Make sure that OpenSSL is installed and accessible for SSL checks.
4. **Script Fails to Fetch Domains**:
   - Check if the Webmin API is enabled and accessible from the server running the script.
   - Ensure the credentials are correct and have necessary permissions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributions

Feel free to submit issues or pull requests to improve this script.

## Author

Created by Dr. Peter O'Hara-Diaz. Contributions and feedback are welcome!

## Contact

For support, please contact [po@floodgatetech.com].
