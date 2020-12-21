#!/usr/bin/env python3
import logging
from asyncio import protocols
from typing import Optional

from hytera_homebrew_bridge.lib.settings import BridgeSettings
from hytera_homebrew_bridge.lib.snmp import SNMP


class CustomBridgeDatagramProtocol(protocols.DatagramProtocol):
    def __init__(self, settings: BridgeSettings) -> None:
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

    def log(self, msg: str, level=logging.INFO) -> None:
        self.logger.log(level, msg)

    def hytera_repeater_obtain_snmp(self, address: tuple, force: bool = False) -> None:
        self.settings.hytera_repeater_ip = address[0]
        if self.settings.snmp_enabled:
            if force or not self.settings.hytera_snmp_data:
                SNMP().walk_ip(address, self.settings)
            if not self.settings.hytera_snmp_data:
                self.log("SNMP failed to walk the repeater", logging.WARN)
        else:
            self.log("SNMP is disabled", logging.WARN)
