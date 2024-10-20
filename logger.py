
import logging

def setup_logger(log_file='app.log'):
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
