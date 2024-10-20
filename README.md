# Webmin/Virtualmin Domain and SSL Monitoring Script

![Expiry Monitor Logo](expiry-monitor-logo.webp)

## Overview

This Python script monitors SSL certificate expirations and domain registration expirations for domains managed by Webmin/Virtualmin servers. It uses the Webmin API to automatically fetch domain lists and check for SSL and domain registration expirations. The script also sends email alerts to notify administrators when domains or SSL certificates are approaching their expiration dates.

## Features

- **Domain List Fetching from Webmin API**: Automatically retrieves domain lists from Webmin servers using their respective API keys.
- **SSL Certificate Expiration Monitoring**: Checks SSL certificates for expiration and sends alerts when they are close to expiring.
- **Domain Registration Expiration Monitoring**: Tracks domain registration expiration dates and sends notifications when they approach expiration.
- **Email Alerts**: Sends alerts to specified email recipients regarding SSL and domain registration expirations.
- **Rotating Log File**: All actions, including successful checks and errors, are logged in a rotating log file.
- **Simple End-User Configuration**: Uses environment variables for easy configuration.
- **Automated Execution**: Supports scheduling via cron job for regular checks (could be modified to run as a `systemd` service).

## Why Use This Script?

- **Proactive Monitoring**: Be alerted in advance to prevent downtime, security risks, or unexpected loss of domain ownership.
- **Centralized Management**: Allows administrators to manage multiple Webmin servers from a single script.
- **Automated Updates**: Reduces manual oversight by automatically updating and tracking domains.
- **Simple Configuration**: Easy-to-set-up environment variables make it flexible and adaptable to various use cases.

## Prerequisites

Ensure you have the following prerequisites installed:

1. **Python 3.6+**
   - Check Python version: `python --version`

2. **pip**: Python's package manager.
   - Install pip if not already installed.

3. **WHOIS Tool**: Used for domain registration checks.
   - Install WHOIS:
     - Ubuntu/Debian: `sudo apt-get install whois`
     - CentOS/RHEL: `sudo yum install whois`

4. **OpenSSL**: Used for checking SSL certificates.
   - Install OpenSSL:
     - Ubuntu/Debian: `sudo apt-get install openssl`
     - CentOS/RHEL: `sudo yum install openssl`

5. **SMTP Access**: SMTP credentials for sending email alerts.

## Dependencies

Install required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Installation

### Option 1: Clone the Repository

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ripcdoc/virtualmin-domains-expiry-monitor.git
    cd virtualmin-domains-expiry-monitor
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the `.env` file:**

    Create a `.env` file in the root directory using the template provided in the included `env.sample` file.

### Option 2: Manual Download

If you prefer to manually download the script instead of cloning the GitHub repository, follow these steps:

1. **Download the script:**
   - Go to the GitHub repository page: [virtualmin-domains-expiry-monitor](https://github.com/ripcdoc/virtualmin-domains-expiry-monitor).
   - Click on the script file(s) and use the "Download" button to save them to your local system.

2. **Install the prerequisites:**
   - Make sure you have Python 3.6+ installed.
   - Install the required Python packages using pip:

     ```bash
     pip install -r requirements.txt
     ```

   - You can create a `requirements.txt` file yourself with the following content:

     ```
     python-dotenv
     requests
     tenacity
     smtplib
     ```

3. **Set up the `.env` file:**
   - Create a new file named `.env` in the same directory as the script and use the following template:

     ```env
     WEBMIN_SERVERS=https://webmin1.example.com,https://webmin2.example.com,https://webmin3.example.com
     WEBMIN_API_KEYS=api_key1,api_key2,api_key3
     EMAIL_HOST=smtp.example.com
     EMAIL_PORT=587
     EMAIL_USER=email@example.com
     EMAIL_PASSWORD=your-email-password
     EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com
     DOMAIN_FILE=domains.txt
     SSL_ALERT_DAYS=15
     DOMAIN_EXPIRATION_ALERT_DAYS=45
     MAX_RETRIES=3
     RETRY_WAIT=5
     LOG_FILE=webmin_domains.log
     ```

4. **Run the script:**

    To run the script manually:

    ```bash
    python monitor_domains.py
    ```

## Configuration

### Setting Up Webmin API Users and API Keys

1. **Log in to each Webmin server:**
   - Access the Webmin dashboard at `https://<your-server-ip>:10000/` and log in.

2. **Create a new Webmin user:**
   - Navigate to `Webmin Users`.
   - Click on `Create a new Webmin user`.
   - Enter a username and set "API key" as the authentication method.

3. **Generate an API key:**
   - Enable "API Access" in the user settings.
   - Generate and copy the API key.
   - Ensure the user has permissions for necessary Virtualmin modules.

4. **Update the `.env` file:**
   - Set `WEBMIN_SERVERS` to a comma-separated list of Webmin URLs.
   - Set `WEBMIN_API_KEYS` to a comma-separated list of corresponding API keys, matching the order of servers.

5. **Test the configuration:**
   - Run the script to verify it fetches domains from each Webmin server using the API keys.

## Automating the Script Execution

To ensure the script runs regularly, you can set it up as a cron job:

1. **Edit the crontab:**

    Open the crontab editor:

    ```bash
    crontab -e
    ```

2. **Add a cron job entry:**

    To run the script daily at 2 AM, add the following line:

    ```bash
    0 2 * * * /usr/bin/python3 /path/to/your/script/monitor_domains.py >> /path/to/your/log/webmin_domains.log 2>&1
    ```

    - Replace `/usr/bin/python3` with the path to your Python interpreter.
    - Replace `/path/to/your/script/` with the path to the script directory.
    - Replace `/path/to/your/log/` with the path to the log directory.

3. **Save and exit the editor.**

The script will now run automatically every day at 2 AM.

## Logging

Logs are stored in a rotating log file specified by the `LOG_FILE` variable in the `.env` file (default: `webmin_domains.log`). Log entries include domain checks, SSL checks, email notifications, and errors.

## Troubleshooting

- **Mismatch in number of servers and API keys:** Ensure that the number of Webmin URLs matches the number of API keys in the `.env` file.
- **Missing environment variables:** Check that all required variables are set in the `.env` file.
- **Email sending issues:** Verify SMTP configuration and credentials.
- **WHOIS or OpenSSL not found:** Ensure WHOIS and OpenSSL are installed and available in your system's PATH.
- **Cron job issues:** Verify file paths, permissions, and correct configuration of cron.

## Author

- **Dr. Peter O'Hara-Diaz**
- Contact: [po@floodgatetech.com](mailto:po@floodgatetech.com)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
