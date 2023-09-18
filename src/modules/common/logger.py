import logging


logging.basicConfig(
    encoding = "utf-8",
    level = logging.INFO,
    format = "MODULE: %(filename)s | LINE: %(lineno)d - %(levelname)s: %(message)s",
    datefmt = "%d/%m/%Y %H:%M:%S"
)

logger = logging.getLogger()
