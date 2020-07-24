#!/usr/bin/env python3

import configparser
from easysnmp import snmp_walk
from hytera_ip_site_connect.storage import Storage


class SNMP(object):
    snmp_enabled: bool = False

    def load_settings(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read("settings.ini")
        if "general" in config:
            if "snmp" in config["general"]:
                self.snmp_enabled = config["general"]["snmp"] == "enable"

    def walk_ip(self, address: tuple, storage: Storage) -> list:
        if not self.snmp_enabled:
            return list()
        ip, port = address
        data = snmp_walk(
            "1.3.6.1.4.1.40297.1.2.4", hostname=ip, community="hytera", version=1
        )
        repeater_info = storage.get_repeater_info_by_address(address)
        repeater_info.set_snmp_data(data)
        storage.set_repeater_info_by_address(address, repeater_info)
        return data
