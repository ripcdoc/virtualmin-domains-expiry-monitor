
import logging

def setup_logger(log_file='app.log', level=logging.INFO):
    """
    Sets up the application logger.

    Args:
        log_file (str): The log file to write logs to.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    try:
        logger = logging.getLogger(__name__)
        logger.setLevel(level)

        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)

        if not logger.hasHandlers():
            logger.addHandler(handler)

        return logger
    except Exception as e:
        print(f"Failed to set up logger: {e}")
        return None

