# Webmin Domain and SSL Monitoring Script

![Webmin Monitor Logo](webmin-monitor-logo.png)

## Overview

This Python script is designed to help administrators monitor the expiration of SSL certificates and domain registrations for domains managed by Webmin/Virtualmin servers. The script interacts with the Webmin API, fetches the list of domains, checks their SSL and domain registration expiration dates, and logs warnings if they are close to expiry. It also updates a local file (`domains.txt`) to keep track of current domains and logs any changes.

## Features

- **Fetch Domain List from Webmin API**: Automatically retrieves the list of domains from one or more Webmin servers using the Webmin API.
- **SSL Certificate Expiration Check**: Checks the SSL certificate expiration date for each domain and logs a warning if the certificate is within 15 days of expiration.
- **Domain Registration Expiration Check**: Verifies the domain registration expiration and logs a warning if the registration is within 45 days of expiration.
- **Automatic Domain Management**: Updates the local domain file (`domains.txt`) by adding new domains and removing deleted ones.
- **Logging**: Logs all events, including SSL and domain checks, additions, and removals, as well as any errors encountered during execution.
- **Configurable**: Easily configure Webmin server URLs, API credentials, alert thresholds, and execution mode (single-run or continuous).
- **Improved Error Handling**: Uses custom error classes for better error management and persistent error alerts when certain errors recur.
- **Continuous Execution Option**: Allows switching between single-run and continuous loop modes by uncommenting specific lines in the script.

## Why Use This Script?

- **Proactive Monitoring**: Get alerted well in advance of SSL or domain expiration to prevent downtime, security risks, or unexpected loss of domain ownership.
- **Automated Updates**: Save time by automatically syncing the domain list from Webmin, removing the need for manual domain management.
- **Flexible and Extendable**: The Python script is written in a modular way, making it easy to customize for specific needs or to add additional features.
- **Simple to Use**: With basic Python knowledge, users can easily set up and run this script, making it a valuable tool for administrators managing Webmin servers.

## How It Works

1. **Fetches Domain List from Webmin Servers**: 
   - Uses the Webmin API to retrieve the list of domains.
   - Updates the local domain file (`domains.txt`).

2. **Checks SSL Certificate Expiration**: 
   - Uses OpenSSL to check the expiration date of SSL certificates.

3. **Checks Domain Registration Expiration**: 
   - Uses WHOIS to verify domain registration expiration dates.

4. **Logs Results**: 
   - All activities and errors are logged in a rotating log file (`webmin_domains.log`).

5. **Handles Errors and Alerts**: 
   - Uses custom error classes to handle different errors (e.g., unauthorized access, server errors).
   - Sends persistent error alerts if specific errors (e.g., 401 Unauthorized) recur.

## Configuration

Before running the script, set up the `.env` file with the following variables:

```env
# Webmin server URLs (comma-separated)
WEBMIN_SERVERS=https://webmin1.example.com,https://webmin2.example.com,https://webmin3.example.com

# Corresponding API keys for Webmin servers (comma-separated, in the same order as WEBMIN_SERVERS)
WEBMIN_API_KEYS=api_key1,api_key2,api_key3

# Email configuration for sending alerts
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=email@example.com
EMAIL_PASSWORD=your-email-password
EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com

# Path to the domain file
DOMAIN_FILE=domains.txt

# SSL and domain expiration alert thresholds
SSL_ALERT_DAYS=15
DOMAIN_EXPIRATION_ALERT_DAYS=45

# Retry configuration for network requests
MAX_RETRIES=5           # Maximum number of retries for API calls
RETRY_WAIT=5            # Initial wait time in seconds for retry, will increase exponentially

# Log file configuration
LOG_FILE=webmin_domains.log

# Persistent error alert settings
ERROR_ALERT_THRESHOLD=3 # Number of consecutive errors before sending a persistent error alert
ERROR_ALERT_INTERVAL=86400 # Interval in seconds between persistent error alerts (default: 24 hours)

# Template directory (for Jinja2 templates)
TEMPLATE_DIR=./templates

# Customizable email templates
EMAIL_TEMPLATE_HTML=email_html.j2
EMAIL_TEMPLATE_PLAIN=email_plain.j2

# Interval in seconds between runs in continuous mode
CHECK_INTERVAL=86400  # Default: 24 hours
```








### Switching to Continuous Execution mode

The script can be run in two modes: **single-run** or **continuous loop**.

- **Single-Run Mode**: By default, the script runs once and then exits.
- **Continuous Loop Mode**: To enable continuous execution, follow these steps:
  1. Open the script file in a text editor.
  2. Locate the following lines near the end of the script:
     ```python
     if __name__ == "__main__":
         # main()  # Default single-run mode
         continuous_loop()  # Uncomment this line to enable continuous loop mode
     ```
  3. Uncomment the `continuous_loop()` line and comment out the `main()` line to switch to continuous mode.
  4. The script will now run continuously, checking for domain and SSL expiration every `CHECK_INTERVAL` seconds.

#### Running as a Systemd Service (if using Continuous Execution mode)

To set up the script as a systemd service for continuous execution:

1. **Create a systemd service file**:
   ```bash
   sudo nano /etc/systemd/system/webmin-monitor.service
   ```

2. **Add the following content to the service file**:
   ```ini
   [Unit]
   Description=Webmin Domain and SSL Monitoring Script (Continuous)
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/your/script/
   ExecStart=/usr/bin/python3 /path/to/your/script/monitor_domains.py
   Restart=always
   RestartSec=10
   EnvironmentFile=/path/to/your/script/.env

   [Install]
   WantedBy=multi-user.target
   ```

   - Replace `your-username` with your system username.
   - Replace `/path/to/your/script/` with the actual path where the script is located.
   - Replace `/usr/bin/python3` with the path to your Python interpreter.

3. **Enable and start the service**:
   ```bash
   sudo systemctl enable webmin-monitor.service
   sudo systemctl start webmin-monitor.service
   ```

4. **Check the status of the service**:
   ```bash
   sudo systemctl status webmin-monitor.service
   ```
### Improved Error Handling

- **Custom Error Classes**: 
  - The script uses custom error classes (`WebminAuthError`, `WebminServerError`, `WebminConnectionError`) for more specific error handling.
  - This helps to differentiate between authentication errors, server errors, and connection issues, making troubleshooting easier.
- **Persistent Error Alerts**: 
  - If a specific error (e.g., unauthorized access) occurs repeatedly beyond the `ERROR_ALERT_THRESHOLD`, the script sends an email alert.
  - The interval between alerts is controlled by the `ERROR_ALERT_INTERVAL` variable.

## Usage

To run the script, use the following command:

```bash
python monitor_domains.py
```

If using continuous mode, the script will run indefinitely, checking for domain and SSL expiration at regular intervals.

### Additional Information

- **Dependencies**: Ensure you have the required dependencies installed by running:
  ```bash
  pip install -r requirements.txt
  ```
- **Logs**: Check the log file (`webmin_domains.log`) for detailed logs of activities and errors.

## Author

- **Dr. Peter O'Hara-Diaz**
- Contact: [po@floodgatetech.com](mailto:po@floodgatetech.com)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
