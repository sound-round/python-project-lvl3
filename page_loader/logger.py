import logging
from functools import wraps


def configure_logging():
    logging.basicConfig(
        filename='log.log',
        filemode='w',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
    )


def configure_console():
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    return console


def logging_info(operation):
    def wrap(function):
        @wraps(function)
        def inner(*args, **kwargs):
            logging.info(f'{operation} started')
            result = function(*args, **kwargs)
            logging.info(f'{operation} finished')
            return result
        return inner
    return wrap
