import logging

class Logger:
    def __init__(self, level=logging.INFO, format='%(message)s', decorated=False):
        self.decorated = decorated
        logging.basicConfig(level=level, format=format)

    def _decorate_message(self, message):
        if self.decorated:
            return f"====== {message} ======"
        else:
            return message

    def info(self, message):
        logging.info(self._decorate_message(message))

    def error(self, message):
        logging.error(self._decorate_message(message))

    def warning(self, message):
        logging.warning(self._decorate_message(message))

    def debug(self, message):
        logging.debug(self._decorate_message(message))
