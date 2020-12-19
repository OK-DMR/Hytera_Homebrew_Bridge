#!/usr/bin/env python3
import logging
from asyncio import protocols
from typing import Optional

from hytera_homebrew_bridge.lib.settings import BridgeSettings


class LoggingProtocol(protocols.DatagramProtocol):
    def __init__(self, settings: BridgeSettings):
        super().__init__()
        self.settings = settings
        self.logger: Optional[logging.Logger] = None
        self.create_logger()

    def create_logger(self) -> None:
        if not self.logger:
            self.logger = logging.getLogger(type(self).__name__)
            self.logger.setLevel(logging.DEBUG)
            console_log_output = logging.StreamHandler()
            console_log_output.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
            )
            console_log_output.setFormatter(formatter)
            self.logger.addHandler(console_log_output)

    def log(self, msg: str, level=logging.INFO):
        self.logger.log(level, msg)
