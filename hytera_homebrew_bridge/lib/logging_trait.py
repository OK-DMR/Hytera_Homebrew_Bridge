#!/usr/bin/env python3
import logging


class LoggingTrait:
    def get_logger(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def log(self, msg: str, level=logging.DEBUG):
        self.get_logger().log(level=level, msg=msg)

    def log_exception(self, exc):
        self.get_logger().exception(exc)
