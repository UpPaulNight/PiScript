import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str, log_file: str = 'events.log') -> logging.Logger:

    # Check to see if the log file exists, if not create it with permissions so
    # that any user can write to it

    if not os.path.isfile(log_file):
        open(log_file, 'a').close()
        os.chmod(log_file, 0o664)
        os.chown(log_file, 1000, 1000)  # Change owner and group to pauls user and group

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Rotating file handler
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8', mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
