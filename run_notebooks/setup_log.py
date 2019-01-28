import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
format_string = '%(asctime)s | %(name)s | %(levelname)s: %(message)s'
formatter = logging.Formatter(format_string)


def setup_logger(filename, level=logging.DEBUG):
    handler = logging.FileHandler(filename, mode='w')
    handler.setLevel(level)
    handler.setFormatter(formatter)
    handler.addFilter(logging.Filter('root'))

    logger.addHandler(handler)


stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.addFilter(logging.Filter('root'))
logger.addHandler(stream_handler)
