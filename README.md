# Webmin Domain and SSL Expiry Monitoring Script with Jinja2 Templated Alerts & Comprehensive Error Handling

![Webmin Monitor Logo](expiry-monitor-logo.webp)

## Overview

This Python script helps administrators monitor the expiration of SSL certificates and domain registrations for domains managed by Webmin/Virtualmin servers. It interacts with the Webmin API, fetches the list of domains, checks their SSL and domain registration expiration dates, and logs warnings if they are close to expiry. It also updates a local file (`domains.txt`) to track current domains and logs any changes. The script uses Jinja2 for templating and full customization of the email alerts.

It supports both single-run and continuous execution modes and can be set up as a systemd service or cron job for automated execution. The script includes error handling with retries and exponential backoff to manage network issues effectively.

## Features

- **Fetch Domain List from Webmin API**: Automatically retrieves the list of domains from one or more Webmin servers using the Webmin API.
- **SSL Certificate Expiration Check**: Checks SSL certificate expiration dates and logs warnings if certificates are close to expiry.
- **Domain Registration Expiration Check**: Verifies domain registration expiration dates and logs warnings if registrations are near expiry.
- **Automatic Domain Management**: Updates the local domain file (`domains.txt`) by adding new domains and removing deleted ones.
- **Customizable Email Alerts with Jinja2 Templates**: Sends HTML and plain-text email alerts using Jinja2 templates. Users can customize the templates (`email_html.j2` and `email_plain.j2`) to personalize email content for SSL and domain expiration notifications.
- **Improved Error Handling**: 
  - Uses custom error classes (`WebminAuthError`, `WebminServerError`, `WebminConnectionError`) to manage specific errors, helping to differentiate between authentication errors, server errors, and connection issues.
  - Implements persistent error alerts that trigger email notifications when the same error occurs consecutively beyond a defined threshold (`ERROR_ALERT_THRESHOLD`). The interval between persistent alerts is configurable with the `ERROR_ALERT_INTERVAL` setting.
- **Enhanced Logging**: 
  - Logs all events, including SSL and domain checks, additions, removals, and errors encountered during execution. 
  - Log entries are stored in a rotating log file (`webmin_domains.log`), which helps manage log size and maintain historical records.
- **Retry Mechanism for API Calls**: The script includes a retry mechanism that handles temporary network failures. It automatically retries failed API calls up to a specified number of attempts (`MAX_RETRIES`) with an exponentially increasing wait time (`RETRY_WAIT`).
- **Parallel Processing with Dynamic Worker Allocation**: Optimizes concurrent processing of API calls by determining the number of workers dynamically based on available CPU cores, reducing execution time.
- **Configurable**: 
  - Easily configure Webmin server URLs, API credentials, alert thresholds, retry attempts, and more through the `.env` file.
  - Allows customization of alert thresholds for SSL and domain expiration to tailor the notification schedule based on specific needs.
- **Continuous Execution Option**: 
  - Provides the option to switch between single-run and continuous loop modes. In continuous loop mode, the script runs indefinitely, checking domain and SSL expiration at regular intervals (`CHECK_INTERVAL`).
  - To enable continuous mode, uncomment the `continuous_loop()` function call and comment out the `main()` function call in the script.
  - Can be integrated with systemd for automatic startup or set up as a cron job for scheduled execution in single-run mode.
- **Systemd Service Integration**: Can be configured as a systemd service for continuous monitoring, with automatic restart capabilities and service management through systemd commands.
- **Cron Job Setup**: Can be run periodically in single-run mode using a cron job, allowing for scheduled execution at specific times.

## Why Use This Script?

- **Proactive Monitoring**: Get alerted well in advance of SSL or domain expiration to prevent downtime, security risks, or unexpected loss of domain ownership.
- **Automated Updates**: Automatically syncs the domain list from Webmin, removing the need for manual domain management.
  - **Note:** The `domains.txt` file, which stores the list of domains, will be created automatically during the first run if it doesn't already exist. This ensures seamless initialization and operation without any additional setup.
- **Flexible and Extendable**: Written in a modular way, making it easy to customize or add additional features.
- **Simple to Use**: Easy setup with basic Python knowledge, making it a valuable tool for administrators managing Webmin servers.

## Configuration

### Setting Up the Environment File
Before running the script, ensure the `.env` file is correctly set up with the variables listed below.

**Warning:** Ensure that the `.env` file is not exposed publicly as it contains sensitive information like API keys and email credentials.

```env
# Webmin server URLs (comma-separated)
WEBMIN_SERVERS=https://webmin1.example.com,https://webmin2.example.com,https://webmin3.example.com

# Corresponding API keys for Webmin servers (comma-separated, in the same order as WEBMIN_SERVERS)
WEBMIN_API_KEYS=api_key1,api_key2,api_key3

# Email configuration for sending alerts
EMAIL_HOST=smtp.example.com       # SMTP server address
EMAIL_PORT=587                    # SMTP server port (e.g., 587 for TLS)
EMAIL_USER=email@example.com      # SMTP user for authentication
EMAIL_PASSWORD=your-email-password # SMTP password for authentication
EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com  # Comma-separated list of email recipients

# Path to the domain file
DOMAIN_FILE=domains.txt           # File to store the list of current domains

# SSL and domain expiration alert thresholds
SSL_ALERT_DAYS=15                 # Number of days before SSL expiration to trigger an alert
DOMAIN_EXPIRATION_ALERT_DAYS=45   # Number of days before domain expiration to trigger an alert

# Retry configuration for network requests
MAX_RETRIES=5                     # Maximum number of retries for API calls
RETRY_WAIT=5                      # Initial wait time in seconds for retries, increases exponentially

# Log file configuration
LOG_FILE=webmin_domains.log       # Log file for storing logs of script execution

# Persistent error alert settings
ERROR_ALERT_THRESHOLD=3           # Number of consecutive errors before sending a persistent error alert
ERROR_ALERT_INTERVAL=86400        # Interval in seconds between persistent error alerts (default: 24 hours)

# Template directory (for Jinja2 templates)
TEMPLATE_DIR=./templates          # Directory where the Jinja2 email templates are stored

# Customizable email templates
EMAIL_TEMPLATE_HTML=email_html.j2 # Jinja2 template for HTML email alerts
EMAIL_TEMPLATE_PLAIN=email_plain.j2 # Jinja2 template for plain-text email alerts

# Interval in seconds between runs in continuous mode
CHECK_INTERVAL=86400              # Default interval: 24 hours
```
> **Note:** The `domains.txt` file does not need to exist before the first run of the script; it will be created automatically based on the retrieved domains.

### Additional Information on Configuration Variables

- **WEBMIN_SERVERS & WEBMIN_API_KEYS**: 
  - These variables must be set as comma-separated lists, and the order of API keys must correspond to the order of server URLs.
  - Ensure that each Webmin server has a matching API key to avoid authentication errors.
- **Email Configuration**:
  - Make sure the SMTP credentials (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`) are correctly set to enable sending email alerts.
  - The `EMAIL_RECIPIENTS` field accepts multiple email addresses separated by commas, allowing alerts to be sent to multiple recipients simultaneously.
- **SSL and Domain Expiration Alert Thresholds**:
  - Adjust `SSL_ALERT_DAYS` and `DOMAIN_EXPIRATION_ALERT_DAYS` to set the desired threshold for when to receive alerts about upcoming expirations.
  - For example, setting `SSL_ALERT_DAYS=10` will trigger an alert if an SSL certificate has 10 days or less until it expires.
- **Retry Configuration**:
  - `MAX_RETRIES` determines how many times the script will retry an API call in case of a failure.
  - `RETRY_WAIT` sets the initial wait time for retries; this will increase exponentially (e.g., 5 seconds, 10 seconds, etc.) with each attempt.
- **Persistent Error Alert Settings**:
  - `ERROR_ALERT_THRESHOLD` sets the number of consecutive errors required to trigger a persistent error alert. If the same error occurs for this many times in a row, an alert will be sent.
  - `ERROR_ALERT_INTERVAL` controls how often persistent error alerts are sent, preventing excessive email notifications for ongoing issues.
- **Template Directory**:
  - The `TEMPLATE_DIR` variable specifies where the Jinja2 templates are located. Ensure this path is correct to avoid errors when sending email alerts.
- **Customizable Email Templates**:
  - Modify `EMAIL_TEMPLATE_HTML` and `EMAIL_TEMPLATE_PLAIN` to change the content of email alerts. These templates use Jinja2 for dynamic content rendering, allowing you to customize the email layout and information.
 
#### Note About Setting Up Environment Variables

Ensure the `.env` file contains all the required variables listed in the **Configuration** section. The script checks for the existence of these variables and will exit with an error if any are missing.

> **Important:** Set these variables before the first run to avoid errors. Use the `.env` file to store and manage these variables securely.

## Running the Script

### Commands Summary
- **Run in single-run mode**:
  ```bash
  python monitor_domains.py
  ```
- **Install dependencies**:
  ```bash
  pip install -r requirements.txt
  ```
- **Check logs**:
  ```bash
  tail -f webmin_domains.log
  ```

### Single-Run Mode

By default, the script runs once and then exits.

#### To run as a Cron Job daily/weekly/etc. in Single-Run Mode

To run the script periodically in single-run mode, you can set up a cron job:

1. **Open the crontab editor**:
   ```bash
   crontab -e
   ```

2. **Add a cron job entry**:
   - To run the script daily at 2 AM, add the following

 line:
     ```bash
     0 2 * * * /usr/bin/python3 /path/to/your/script/monitor_domains.py >> /path/to/your/log/webmin_domains.log 2>&1
     ```
   - Replace `/usr/bin/python3` with the path to your Python interpreter.
   - Replace `/path/to/your/script/` with the path to the script directory.
   - Replace `/path/to/your/log/` with the path to the log directory.

3. **Save and exit the crontab editor**.

The script will now run automatically at the specified time, logging the output to the specified log file.

### Continuous Loop Mode

To enable continuous execution, follow these steps:
  1. Open the script file in a text editor.
  2. Locate the following lines near the end of the script:
     ```python
     if __name__ == "__main__":
         # main()  # Default single-run mode
         continuous_loop()  # Uncomment this line to enable continuous loop mode
     ```
  3. Uncomment the `continuous_loop()` line and comment out the `main()` line then uncomment the continuous loop block to switch to continuous mode (clear instructions are included in the script as to what should be uncommented and what to comment out).
  4. The script will now run continuously, checking for domain and SSL expiration every `CHECK_INTERVAL` seconds.

#### To run as a Systemd Service in Continuous Loop Mode

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

The script will now run as a continuous service, restarting automatically if it fails and running indefinitely.

## Comprehensive Error Handling

- **Custom Error Classes**: 
  - The script uses custom error classes (`WebminAuthError`, `WebminServerError`, `WebminConnectionError`) to manage specific errors.
  - These classes help differentiate between authentication errors (e.g., 401 Unauthorized), server-side errors (e.g., 500 Internal Server Errors), and connection-related issues (e.g., timeouts, request failures).
  - By using custom error handling, the script can manage issues more effectively, log detailed error messages, and adjust the retry mechanism as needed.
  
- **Persistent Error Alerts**: 
  - If a specific error (e.g., unauthorized access, server error) occurs repeatedly beyond the `ERROR_ALERT_THRESHOLD`, the script sends an email alert to notify administrators of the persistent issue.
  - The interval between persistent alerts is managed by the `ERROR_ALERT_INTERVAL` variable, ensuring that alerts are sent only after a specified duration to avoid overwhelming users with repeated notifications.
  - For example, if `ERROR_ALERT_THRESHOLD=3` and the same error occurs three times in succession, the script triggers a persistent error alert.
  - This mechanism prevents alert fatigue while ensuring that significant issues are escalated promptly.

- **Retry Mechanism**: 
  - The script includes a built-in retry mechanism for handling temporary network failures or timeouts.
  - It uses exponential backoff for retries, starting with an initial wait time (`RETRY_WAIT`) and increasing it exponentially up to the maximum number of retries (`MAX_RETRIES`).
  - This approach improves reliability, allowing the script to recover from temporary connectivity issues without manual intervention.

- **Detailed Logging**: 
  - All errors, including specific error codes and messages, are logged in the configured log file (`webmin_domains.log`).
  - The log includes additional details for persistent error alerts, including the type of error, affected Webmin server, and timestamp of the occurrence.

- **Example of Comprehensive Error Handling in Action**: 
  - If the script encounters an authentication error while connecting to a Webmin server, it logs the error, triggers retries (if configured), and sends a persistent alert if the issue continues beyond the defined threshold.
  - Similarly, in the case of server-side errors (e.g., HTTP 500), the script logs the error, retries the connection, and triggers an alert if the problem persists.

## Additional Information

### Dependencies

To ensure you have all the necessary Python packages, use the `requirements.txt` file to install dependencies. Run the following command:

```bash
pip install -r requirements.txt
```

The expected dependencies include:
- `requests`
- `python-dotenv`
- `tenacity`
- `jinja2`
- `smtplib` (built-in)

> **Unsupported Recommendation for Python Experienced Users:**
> Use a virtual environment to manage dependencies and prevent conflicts with other Python projects. To create and activate a virtual environment, run:
> ```bash
> python3 -m venv venv
> source venv/bin/activate  # On Windows: venv\Scripts\activate
> pip install -r requirements.txt
> ```

### Logs

Check the log file (`webmin_domains.log`) for detailed logs of activities and errors.

## Author

- **Dr. Peter O'Hara-Diaz**
- Contact: [po@floodgatetech.com](mailto:po@floodgatetech.com)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
