import logging
from modules.common import config


logging.basicConfig(
    filename = config.LOG_PATH,
    encoding = 'utf-8',
    level = logging.DEBUG,
    format = "%(asctime)s MODULE: %(module)s (%(funcName)s) - LINE: %(lineno)d - %(levelname)s - %(message)s",
    datefmt = '%d/%m/%Y %H:%M:%S'
)

logger = logging.getLogger(config.LOG_NAME)