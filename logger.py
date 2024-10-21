import logging


def setup_logger():
    """
    Sets up and returns a logger instance.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("webmin_domains")
    logger.setLevel(logging.DEBUG)
    
    # Create file handler which logs messages
    file_handler = logging.FileHandler("webmin_domains.log")
    file_handler.setLevel(logging.INFO)
    
    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()

if __name__ == "__main__":
    logger.info("Logger setup complete.")
