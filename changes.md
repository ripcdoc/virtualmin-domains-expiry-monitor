# Webmin Domain Monitoring Script

This script monitors SSL certificate and domain registration expiration dates for domains hosted on Webmin servers. 

## Setup Instructions

### Step 1: Install Dependencies

First, install the required Python dependencies by running:

```sh
pip install -r requirements.txt
```

Ensure that `requirements.txt` includes:
```text
python-dotenv
requests
```

### Step 2: Set Up Environment Variables

1. Copy the provided `.env.sample` file to `.env`:

```sh
cp .env.sample .env
```

2. Edit the `.env` file to set the appropriate values for your setup. Here are the variables you need to set:

- **WEBMIN_SERVERS**: A comma-separated list of your Webmin server URLs. For example:
  ```
  WEBMIN_SERVERS="http://server1:10000,http://server2:10000"
  ```
  
- **WEBMIN_USERS**: A comma-separated list of usernames for each of the Webmin servers. Make sure the order corresponds to the Webmin servers list. For example:
  ```
  WEBMIN_USERS="username1,username2"
  ```
  
- **WEBMIN_PASSWORDS**: A comma-separated list of passwords for each of the Webmin servers. Make sure the order corresponds to the usernames list. For example:
  ```
  WEBMIN_PASSWORDS="password1,password2"
  ```

- **DOMAIN_FILE**: The path where the domains list will be stored. You can leave this as `domains.txt` if you don't need to change it.

- **LOG_FILE**: The path to the log file for this script. You can leave this as `webmin_domains.log`.

- **SSL_ALERT_DAYS**: The number of days before the SSL certificate expires that you want to be alerted. Default is 15 days.

- **DOMAIN_EXPIRATION_ALERT_DAYS**: The number of days before the domain registration expires that you want to be alerted. Default is 45 days.

### Step 3: Running the Script Manually

You can run the script manually by executing:

```sh
python3 script.py
```

### Step 4: Set Up a Cron Job

To run the script daily, you can create a cron job:

1. Open the cron job editor:

```sh
crontab -e
```

2. Add the following line to schedule the script at midnight every day:

```sh
0 0 * * * /usr/bin/python3 /path/to/your/script.py
```

Make sure the `.env` file is in the same directory as the script, or modify the script to point to the correct location.

## Notes

- The **.env** file should not be shared or committed to version control, as it contains sensitive information like usernames and passwords. Add the `.env` file to `.gitignore` to ensure it is not accidentally shared:

```
.env
```

### Step 5: Log Files

The script creates log files that store information about domain checks. You can adjust the log file location in the `.env` file using the **LOG_FILE** variable.

---

This guide should help you set up and run the Webmin domain monitoring script easily. If you encounter any issues, please reach out to the support team or consult the documentation for further assistance.
```

### **3. Requirements File (`requirements.txt`)**

The `requirements.txt` file lists the Python packages necessary for the script:

```
python-dotenv
requests
```

### **Summary of Changes**

- **Revised Script**: Modified the script to load all configurable parameters from a `.env` file.
- **`.env.sample` File**: Provided a sample `.env` file with all the necessary configurations.
- **`README.md` Documentation**: Added detailed setup instructions for the user, including environment setup, running the script, and setting up cron jobs.
- **`requirements.txt` File**: Listed necessary Python libraries.
