import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
format_string = '%(asctime)s | %(name)s | %(levelname)s: %(message)s'
formatter = logging.Formatter(format_string)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logFile = '.error_log_detail'
file_handler = logging.FileHandler(logFile, mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
file_handler.addFilter(logging.Filter('root'))

logFile = '.error_log_summary'
summary_handler = logging.FileHandler(logFile, mode='w')
summary_handler.setFormatter(formatter)
summary_handler.setLevel(logging.INFO)
summary_handler.addFilter(logging.Filter('root'))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(summary_handler)
