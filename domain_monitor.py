
from domain_operations import gather_all_domains
from notifications import send_email, render_email_template
from logger import setup_logger
from config import Config
import time

logger = setup_logger()

def main():
    all_domains = gather_all_domains()

    for domain in all_domains:
        # Placeholder for checking expiration or any other processing
        pass

def continuous_loop():
    while True:
        main()
        logger.info(f"Sleeping for {Config.CHECK_INTERVAL} seconds before the next run.")
        time.sleep(Config.CHECK_INTERVAL)

if __name__ == "__main__":
    # Uncomment the next line to enable continuous loop mode
    # continuous_loop()

    # Comment the following line if enabling continuous loop mode
    main()
