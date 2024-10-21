
from domain_operations import gather_all_domains
from notifications import send_email, render_email_template
from logger import setup_logger
from config import Config
import time
import signal
import sys

logger = setup_logger()

def main():
    """
    Main function for monitoring domains.
    Gathers all domains and checks for expiration or other events.
    """
    try:
        all_domains = gather_all_domains()

        for domain in all_domains:
            # Placeholder for checking expiration or any other processing
            pass
    except Exception as e:
        logger.error(f"Error in main: {e}")

def continuous_loop():
    """
    Continuous loop for running the main function at regular intervals.
    """
    def handle_exit(signum, frame):
        logger.info("Received exit signal. Shutting down...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    while True:
        main()
        logger.info(f"Sleeping for {Config.CHECK_INTERVAL} seconds before the next run.")
        time.sleep(Config.CHECK_INTERVAL)

if __name__ == "__main__":
    # Uncomment the next line to enable continuous loop mode
    # continuous_loop()

    # Comment the following line if enabling continuous loop mode
    main()
    
