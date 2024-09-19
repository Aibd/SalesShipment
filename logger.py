import logging
import time
from logging.handlers import RotatingFileHandler

class Logger:
    _handler_added = False  # 类变量来检查是否已经添加过处理器

    def __init__(self, name, log_file, level=logging.INFO):
        """
        Initialize the logger with the given name and log file.
        """
        self.logger = logging.getLogger(name)
        if not Logger._handler_added:
            self.logger.setLevel(level)
            # 设置标志，表示处理器已添加

            # Create file handler which logs even debug messages
            fh = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=5, encoding='utf-8')
            fh.setLevel(level)

            # Create console handler with a higher log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.ERROR)

            # Create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # Add the handlers to the logger
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
            Logger._handler_added = True  # 设置标志，表示处理器已添加


    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

if __name__ == "__main__":
    log = Logger('my_app', 'log.log')
    while True:
        log.info('This is an info message')
        time.sleep(5)
#     log.debug('This is a debug message')
#     log.error('This is an error message')
#     log.warning('This is a warning message')
