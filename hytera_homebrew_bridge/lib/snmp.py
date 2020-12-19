#!/usr/bin/env python3

from easysnmp import snmp_walk

from hytera_homebrew_bridge.lib.settings import BridgeSettings


class SNMP:
    @staticmethod
    def walk_ip(address: tuple, settings: BridgeSettings) -> list:
        ip, port = address
        try:
            settings.hytera_snmp_data = snmp_walk(
                "1.3.6.1.4.1.40297.1.2.4",
                hostname=ip,
                community=settings.snmp_family,
                version=1,
            )
        except SystemError:
            settings.hytera_snmp_data = list()

        return settings.hytera_snmp_data
