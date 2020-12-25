#!/usr/bin/env python3
import logging
from asyncio import protocols

from hytera_homebrew_bridge.lib.logging_trait import LoggingTrait
from hytera_homebrew_bridge.lib.settings import BridgeSettings
from hytera_homebrew_bridge.lib.snmp import SNMP


class CustomBridgeDatagramProtocol(protocols.DatagramProtocol, LoggingTrait):
    def __init__(self, settings: BridgeSettings) -> None:
        super().__init__()
        self.settings = settings

    def hytera_repeater_obtain_snmp(self, address: tuple, force: bool = False) -> None:
        self.settings.hytera_repeater_ip = address[0]
        if self.settings.snmp_enabled:
            if force or not self.settings.hytera_snmp_data:
                SNMP().walk_ip(address, self.settings)
        else:
            self.log_warning("SNMP is disabled")
