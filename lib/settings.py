#!/usr/bin/env python3

import configparser


class BridgeSettings:
    SECTION_HB = "homebrew"
    SECTION_IPSC = "ip-site-connect"
    SECTION_GENERAL = "general"

    HYTERA_MODE_IPSC = "ip-site-connect"
    HYTERA_MODE_FTPC = "forward-to-pc"

    def __init__(self, filepath: str):
        parser = configparser.ConfigParser()
        parser.sections()
        parser.read(filepath)

        self.hb_master_host = parser.get(self.SECTION_HB, "master_ip")
        self.hb_master_port = parser.getint(self.SECTION_HB, "master_port")
        self.hb_local_ip = parser.get(self.SECTION_HB, "local_ip")
        self.hb_local_port = parser.getint(self.SECTION_HB, "local_port", fallback=0)
        self.hb_password = parser.get(self.SECTION_HB, "password")

        self.hb_repeater_dmr_id = parser.getint(self.SECTION_HB, "repeater_dmr_id")
        self.hb_callsign = parser.get(self.SECTION_HB, "callsign")
        self.hb_color_code = parser.getint(self.SECTION_HB, "color_code")
        self.hb_latitude = parser.get(self.SECTION_HB, "latitude")
        self.hb_longitude = parser.get(self.SECTION_HB, "longitude")
        self.hb_antenna_height = parser.getint(self.SECTION_HB, "antenna_height")
        self.hb_location = parser.get(self.SECTION_HB, "location")
        self.hb_description = parser.get(self.SECTION_HB, "description")
        self.hb_timeslots = parser.get(self.SECTION_HB, "timeslots", fallback="3")
        self.hb_url = parser.get(self.SECTION_HB, "url")
        self.hb_software_id = parser.get(self.SECTION_HB, "software_id")
        self.hb_package_id = parser.get(self.SECTION_HB, "package_id")
        self.hb_rx_freq = parser.get(self.SECTION_HB, "rx_freq")
        self.hb_tx_freq = parser.get(self.SECTION_HB, "tx_freq")
        self.hb_tx_power = parser.getint(self.SECTION_HB, "tx_power")

        self.hytera_mode = parser.get(
            self.SECTION_GENERAL, "hytera_mode", fallback=self.HYTERA_MODE_IPSC
        )

        if self.hytera_mode == self.HYTERA_MODE_IPSC:
            self.ipsc_ip = parser.get(self.SECTION_IPSC, "ip")
            self.service_port = parser.getint(self.SECTION_IPSC, "service_port")
            self.dmr_port = parser.getint(self.SECTION_IPSC, "dmr_port")
            self.rdac_port = parser.getint(self.SECTION_IPSC, "rdac_port")

    def print_settings(self):
        print("Settings Loaded:")
        print(
            f"\tHytera Repeater is expected to connect at {self.ipsc_ip}:{self.service_port}"
        )
        print(
            f"\tUpstream Homebrew/MMDVM server is expected at {self.hb_master_host}:{self.hb_master_port}"
        )
        print("\n")
