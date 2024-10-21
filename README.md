# Webmin Domain and SSL Expiry Monitoring Script with Jinja2 Templated Alerts & Comprehensive Error Handling

![Webmin Monitor Logo](expiry-monitor-logo.webp)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/github/license/ripcdoc/virtualmin-domains-expiry-monitor)
![GitHub Issues](https://img.shields.io/github/issues/ripcdoc/virtualmin-domains-expiry-monitor)
![GitHub Forks](https://img.shields.io/github/forks/ripcdoc/virtualmin-domains-expiry-monitor)
![GitHub Stars](https://img.shields.io/github/stars/ripcdoc/virtualmin-domains-expiry-monitor)
![Last Commit](https://img.shields.io/github/last-commit/ripcdoc/virtualmin-domains-expiry-monitor)
![PyPI - Downloads](https://img.shields.io/pypi/dm/virtualmin-domains-expiry-monitor)

## Table of Contents
- [Introduction](#introduction)
- [Version Information](#version-information)
- [Features](#features)
- [Why Use This Script?](#why-use-this-script)
- [Quick Start Guide](#quick-start-guide)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example Outputs](#example-outputs)
- [Testing](#testing)
- [CI/CD Integration](#cicd-integration)
- [Logo Placeholder](#logo-placeholder)
- [Unit and Service Sections](#unit-and-service-sections)
- [Common Issues](#common-issues)
- [Error Handling Settings](#error-handling-settings)
- [Proactive Monitoring Feature](#proactive-monitoring-feature)
- [Continuous Loop Enablement](#continuous-loop-enablement)
- [Additional Requirements](#additional-requirements)
- [Webmin Configuration Details](#webmin-configuration-details)
- [Author](#author)
- [Release Notes](#release-notes)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This Python script helps administrators monitor the expiration of SSL certificates and domain registrations for domains managed by Webmin/Virtualmin servers. It interacts with the Webmin API, fetches the list of domains, checks their SSL and domain registration expiration dates, and logs warnings if they are close to expiry. It also updates a local file (`domains.txt`) to track current domains and logs any changes. The script uses Jinja2 for templating and full customization of the email alerts.

It supports both single-run and continuous execution modes and can be set up as a systemd service or cron job for automated execution. The script includes error handling with retries and exponential backoff to manage network issues effectively.

This script now uses a **modular design**, with different modules handling configuration, domain operations, notifications, and logging, enhancing maintainability and scalability. It also now handles additional domains not hosted on a Webmin server (user configurable via the `.env` file).

## Version Information

### Current Version: v2.0.0rc (Released on 2024-10-21)

#### Notable Changes:
- **CI/CD Integration**:
  - **Implemented**: automated unit testing, static code analysis, multi-version compatibility checks, and test coverage reporting.
  - **Multi-Version Testing**: now supports Python `3.8`, `3.9`, `3.10`, **`and 3.11`**, providing broader compatibility assurance.
- **Dynamic Batch Size Calculation**: Automatically adjusts batch sizes based on API rate limits, processing time, and delay settings, offering improved scalability and performance.
- **Enhanced Concurrency**: The new release optimizes parallel processing using threading, enabling faster domain monitoring for large lists.
- **Advanced Error Handling**: Added custom exceptions and comprehensive try-catch blocks to improve robustness and error resilience across modules.
- **Improved Notification System**: Added support for logo URLs and support URLs in email templates, providing branded and informative alerts.
- **Detailed Documentation**: Updated README, contributing guidelines, and environment variable descriptions for easier setup and configuration.
> **For full details**, please see the [Release Notes](RELEASE_NOTES.md) and [Changelog](https://github.com/ripcdoc/virtualmin-domains-expiry-monitor/compare/v1.1.1...v2.0.0rc).

## Features
- **Concurrent Domain Monitoring**: Uses threading to check multiple domains simultaneously.
- **Batch Processing**: Processes domains in batches to manage API load and prevent rate limits.
- **Static Analysis and Unit Testing**: Integrated tools for code quality and robustness, ensuring reliability.
- **Multi-Version Testing**: Supports Python 3.8, 3.9, 3.10, and 3.11 (if included in CI/CD) to ensure compatibility.
- **Modular Architecture**: The script is structured into separate modules:
  - `config.py`: Manages configuration loading from the `.env` file.
  - `domain_operations.py`: Handles domain retrieval from Webmin servers and includes support for additional domains.
  - `notifications.py`: Manages email alerts using Jinja2 templates.
  - `logger.py`: Sets up centralized logging.
  - `domain_monitor.py`: Acts as the main controller to orchestrate the workflow.
- **Fetch Domain List from Webmin API**: Automatically retrieves the list of domains from one or more Webmin servers using the Webmin API.
- **SSL Certificate Expiration Check**: Checks SSL certificate expiration dates and logs warnings if certificates are close to expiry.
- **Domain Registration Expiration Check**: Verifies domain registration expiration dates and logs warnings if registrations are near expiry.
- **Automatic Domain Management**: Updates the local domain file (`domains.txt`) by adding new domains and removing deleted ones.
- **Support for Additional Domains**: Users can specify additional domains to be monitored by setting the `ADDITIONAL_DOMAINS` variable in the `.env` file.
- **Customizable Email Alerts with Jinja2 Templates**: Sends HTML and plain-text email alerts using Jinja2 templates. Users can customize the templates (`email_html.j2` and `email_plain.j2`) for SSL and domain expiration notifications.
- **Comprehensive Error Handling**: 
  - Uses custom error classes (e.g., `WebminAuthError`, `WebminServerError`, `WebminConnectionError`) to manage specific errors, differentiating between authentication, server, and connection issues.
  - Implements persistent error alerts that trigger email notifications when errors occur consecutively beyond a defined threshold (`ERROR_ALERT_THRESHOLD`).
- **Enhanced Logging**: 
  - Logs all events, including SSL and domain checks, additions, removals, and errors encountered during execution.
  - Log entries are stored in a rotating log file (`webmin_domains.log`), which helps manage log size and maintain historical records.
- **Retry Mechanism for API Calls**: Includes a retry mechanism that handles temporary network failures, automatically retrying failed API calls up to a specified number of attempts (`MAX_RETRIES`), with exponentially increasing wait times.
- **Parallel Processing with Dynamic Worker Allocation**: Optimizes concurrent processing of API calls by dynamically determining the number of workers based on available CPU cores, reducing execution time.
- **Configurable**: 
  - Easily configure Webmin server URLs, API credentials, alert thresholds, retry attempts, and more through the `.env` file.
  - New feature: Automatic batch size calculation based on API rate limits and processing time.
  - Allows customization of alert thresholds for SSL and domain expiration to tailor the notification schedule.
- **Continuous Execution Option**: 
  - Provides the option to switch between single-run and continuous loop modes. 
  - In continuous loop mode, the script runs indefinitely, checking domain and SSL expiration at regular intervals (`CHECK_INTERVAL`).
  - Can be integrated with systemd for automatic startup or set up as a cron job for scheduled execution in single-run mode.
- **Systemd Service Integration**: Configurable as a systemd service for continuous monitoring, with automatic restart capabilities and service management through systemd commands.
- **Cron Job Setup**: Can be run periodically in single-run mode using a cron job, allowing for scheduled execution at specific times.

## Why Use This Script?
- **Proactive Monitoring**: Get alerted well in advance of SSL or domain expiration to prevent downtime, security risks, or unexpected loss of domain ownership.
- **Automated Updates**: Automatically syncs the domain list from Webmin, removing the need for manual domain management.
  - **Note:** The `domains.txt` file, which stores the list of domains, will be created automatically during the first run if it doesn't already exist. This ensures seamless initialization and operation without any additional setup.
- **Flexible and Extendable**: Written in a modular way, making it easy to customize or add additional features.
- **Simple to Use**: Easy setup with basic Python knowledge, making it a valuable tool for administrators managing Webmin servers.

## Quick Start Guide

### Step 1: Clone the Repository

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/ripcdoc/virtualmin-domains-expiry-monitor.git
   cd virtualmin-domains-expiry-monitor
   ```

### Step 2: Install Python Dependencies

1. Ensure you have Python 3 installed.
2. Install the required packages from the `requirements.txt` file:
   ```bash
   python -m pip install -r requirements.txt
   ```

### Step 3: Set Up Environment Variables

1. Copy the sample environment file and rename it:
   ```bash
   cp .env.sample .env
   ```
2. Open the `.env` file and configure the following variables:
   - **Webmin server URLs and API keys**: Set `WEBMIN_SERVERS` & `WEBMIN_API_KEYS`.
   - **Batch processing settings**: Adjust variables like `BATCH_SIZE`, `API_RATE_LIMIT`, and `AVG_PROCESSING_TIME`.
   - **Email settings**: Configure variables like `EMAIL_SENDER`, `EMAIL_RECIPIENT`, `SMTP_SERVER`, etc.
   - **Other settings**: Customize SSL alert days, domain expiration days, retry settings, etc., as needed.

> **Note**: Ensure proper API access is configured in your Webmin control panel.

### Step 4: Verify Template Files

1. Check the `templates/` directory for the default email templates:
   - `email_html.j2`
   - `email_plain.j2`
2. If needed, create customized templates and update the `.env` file accordingly.

### Step 5: Run the Script

1. Execute the script to check domain and SSL expiration:
   ```bash
   python domain_monitor.py
   ```
2. Check the console output and the log file (`webmin_domains.log`) to ensure proper execution.

### Step 6: Enable Continuous Loop Mode (Optional)

1. Open the `domain_monitor.py` script.
2. Locate the following lines near the end of the script:
   ```python
   if __name__ == "__main__":
       main()  # Default single-run mode
       # continuous_loop()  # Uncomment this line to enable continuous loop mode
   ```
3. Uncomment the `continuous_loop()` line and comment out the `main()` line.
4. Save the script and run it:
   ```bash
   python domain_monitor.py
   ```

### Step 7: Set Up as a Systemd Service (Optional)

If using continuous loop mode, you can run the script as a **systemd service**:

1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/webmin-monitor.service
   ```
2. Add the following configuration:
   ```ini
   [Unit]
   Description=Webmin Domain and SSL Monitoring Script (Continuous)
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/your/script/
   ExecStart=/usr/bin/python3 /path/to/your/script/domain_monitor.py
   Restart=always
   RestartSec=10
   EnvironmentFile=/path/to/your/script/.env

   [Install]
   WantedBy=multi-user.target
   ```
   - Replace `your-username` and `/path/to/your/script/` accordingly.

3. Enable and start the service:
   ```bash
   sudo systemctl enable webmin-monitor.service
   sudo systemctl start webmin-monitor.service
   ```

### Step 8: Set Up as a Cron Job (Optional)

If using single-run mode, set up a cron job to run the script periodically:

1. Open the crontab editor:
   ```bash
   crontab -e
   ```
2. Add the cron job entry:
   ```bash
   0 2 * * * /usr/bin/python3 /path/to/your/script/domain_monitor.py >> /path/to/your/log/webmin_domains.log 2>&1
   ```

### Step 9: Review Logs and Monitor Alerts

- Check the log file for any errors or warnings:
  ```bash
  tail -f webmin_domains.log
  ```
- Monitor email alerts for SSL or domain expirations.

> **Troubleshooting**: If you encounter issues, refer to the **Troubleshooting** section below.














## Installation
- Ensure Python 3.8 or higher is installed.
- Install required dependencies using:
  ```bash
  python -m pip install -r requirements.txt
  ```

## Configuration
- The `.env` file should include:
  - `WEBMIN_SERVERS`, `WEBMIN_API_KEYS`, `BATCH_SIZE`, `BATCH_DELAY`, etc.
- Example `.env` configuration:
  ```
  WEBMIN_SERVERS=https://webmin1.example.com,https://webmin2.example.com
  WEBMIN_API_KEYS=api_key1,api_key2
  BATCH_SIZE=5
  BATCH_DELAY=2
  ```

## Usage
- **Basic Usage**: Run the script using `python domain_monitor.py`.
- **Continuous Monitoring**: The script checks domains continuously at the interval defined in `.env`.
- **Log Outputs**: Check `webmin_domains.log` for detailed logs.

## Example Outputs

### 1. Sample Log Output
```
2024-10-25 12:00:00,000 - INFO - Checking domain expiration: example.com
2024-10-25 12:00:05,000 - INFO - Domain example.com will expire in 30 days.
2024-10-25 12:00:10,000 - INFO - Notification sent for domain expiration: example.com
```

### 2. Sample Email Alert (Plain Text)
```
Subject: Domain Expiry Alert: example.com

Hello,

This is an automated notification regarding the domain registration for the following domain:

Domain: example.com
Days until expiration: 30

Please renew the domain registration to avoid service interruptions.

---
This is an automated message. Please do not reply.
```

### 3. Sample Command-Line Output
```
$ python domain_monitor.py
Checking domain expiration: example.com
Domain example.com will expire in 30 days.
Notification sent for domain expiration: example.com
```

## Testing
- **Unit Tests**: Run unit tests using pytest:
  ```bash
  pytest tests/
  ```
- **Static Analysis**: Run flake8 and pylint for code quality checks:
  ```bash
  flake8 .
  pylint **/*.py
  ```
- **Multi-Version Testing**: Run tox for testing compatibility across Python versions:
  ```bash
  tox
  ```

## CI/CD Integration
- The CI/CD pipeline is configured using GitHub Actions.
- It includes:
  - Static Analysis: Runs flake8 and pylint.
  - Multi-Version Testing: Tests Python 3.8, 3.9, and 3.10 using tox.
  - Unit Testing: Uses pytest to validate functionality across modules.

## Contributing
- Contributions are welcome! Please follow the contribution guidelines in the CONTRIBUTING.md file.
- Open issues for bug reports or feature requests and submit pull requests for new features or fixes.

## Logo Placeholder
- The email templates include a placeholder image at the top of the HTML email, which can be replaced with your organization's logo. To update, modify the `src` attribute of the `<img>` tag in `email_html.j2`.

## Unit and Service Sections
- To run the script as a systemd service, follow these steps:
  1. Create a systemd service file (e.g., `/etc/systemd/system/domain-monitor.service`):
     ```
     [Unit]
     Description=Domain and SSL Expiry Monitor
     After=network.target

     [Service]
     ExecStart=/usr/bin/python3 /path/to/domain_monitor.py
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```
  2. Enable and start the service:
     ```bash
     sudo systemctl enable domain-monitor
     sudo systemctl start domain-monitor
     ```

## Common Issues
If you encounter issues while running the script, consider the following solutions:
- Ensure all environment variables are set correctly in the `.env` file.
- Verify that the Webmin servers are accessible and that the API keys are valid.
- Check the logs (`webmin_domains.log`) for detailed error messages.

## Error Handling Settings
- **ERROR_ALERT_THRESHOLD**: Sets the number of consecutive errors required to trigger a persistent error alert. If the same error occurs for this many times, an alert is sent.
- **MAX_RETRIES**: Determines how many times the script will retry an API call in case of a failure.

## Proactive Monitoring Feature
- The script sends alerts well in advance of domain or SSL expiration to prevent downtime, security risks, or unexpected loss of domain ownership.

## Continuous Loop Enablement
- To enable continuous monitoring, uncomment the `continuous_loop()` line in `domain_monitor.py`.
  ```python
  if __name__ == "__main__":
      # continuous_loop()  # Uncomment this line to enable continuous loop mode
  ```

## Additional Requirements
- The script requires specific dependencies, including:
  - `jinja2` for email template rendering.

## Webmin Configuration Details
- The `.env` file should specify the following:
  - **WEBMIN_SERVERS**: A comma-separated list of Webmin server URLs.
  - **WEBMIN_API_KEYS**: Corresponding API keys for the Webmin servers.

## Author
- **Dr. Peter O'Hara-Diaz**
- Contact: [po@floodgatetech.com](mailto:po@floodgatetech.com)

## Release Notes
**For detailed release notes of the latest version, including new features, improvements, and bug fixes, please see the [Release Notes](RELEASE_NOTES.md).**

### Changelog for v2.0.0rc

#### 🚀 Major Enhancements
- **Dynamic Batch Size Calculation**: Automatically adjusts batch size for domain checks based on API limits and processing time.
- **Parallel Processing with Threading**: Improved performance by enabling concurrent checks using threading.
- **Advanced Error Handling**: Added custom exceptions and try-catch blocks to improve error resilience.
- **CI/CD Integration**: Implemented automated testing, coverage reporting, and multi-version testing.
- **Enhanced Notification System**: Added support for branded email templates with support and logo URLs.

#### 🛠️ Improvements
- Detailed comments and documentation added to environment configuration.
- Revised README with new sections for setup, configuration, and performance features.
- Optimized logging with more descriptive messages and log level control.

#### 🐛 Bug Fixes
- Resolved missing variables in the environment file.
- Fixed silent failures by improving error propagation and logging.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
