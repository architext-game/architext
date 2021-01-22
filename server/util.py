import logging
import entities
import os
import re


def possible_meanings(partial_string, list_of_options):
    if partial_string in list_of_options:
        return [string for string in list_of_options if partial_string == string]
    else:
        return [string for string in list_of_options if partial_string in string]

def setup_logger(logger_name, log_file, console=False, level=logging.INFO):
    """Sets up a logger that can be used across all modules.
    Example:
        setup_logger('log1', "logs.txt")  # Sets up the logger
        logger_1 = logging.getLogger('log1')  # Gets the logger (works from anywhere)
        logger_1.info('Some info to log')  # logs something
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')

# handler = logging.handlers.RotatingFileHandler(
#              LOG_FILENAME, maxBytes=20, backupCount=5)

    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s: %(message)s')
    fileHandler = logging.FileHandler(os.getcwd() + '/logs/' + log_file, 'a', 'utf-8')
    fileHandler.setFormatter(formatter)
    if console:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)  

    logger.setLevel(level)
    logger.addHandler(fileHandler)
      

    return logger


