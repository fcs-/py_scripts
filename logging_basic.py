#coding: utf-8
import logging
import sys

"""脚本用来展示logging模块的基本用法.
"""

logger = logging.getLogger("AppName")

formatter = logging.Formatter('%(asctime)s %(levelname)-8s: (%(name)s)%(pathname)s %(message)s')

file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.formater = formatter

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)

logger.debug("This is debug message")
logger.info("This is info message")
logger.warning("This is warning message")
logger.error("This is error message")
logger.fatal("This is fatal message")
logger.critical("This is critical message")

try:
     1/0
except:
    logger.exception("except: ")

logger.removeHandler(file_handler)
logger.debug("This is debug info ---- 2")

logger.setLevel(logging.ERROR)
logger.info("This is info msg")
logger.warning("This warning msg")
logger.error("This is error msg")
logger.fatal("This is fatal msg")
logger.critical("This is critical msg")

