#!/usr/bin/env python3

import configparser
from threading import Thread

from hytera_common.hytera_service_interface import HyteraServiceInterface
from hytera_forward_to_pc.hytera_forward_to_pc import HyteraForwardToPC
from hytera_ip_site_connect.hytera_ipsc import HyteraIPSiteConnect


class HyteraHomebrewBridge(Thread):
    hytera_service: HyteraServiceInterface = None

    def load_settings(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read("settings.ini")
        if 'general' in config:
            if 'mode' in config:
                if config['general']['mode'] == 'ip-site-connect':
                    self.hytera_service = HyteraIPSiteConnect()

        # fallback
        if self.hytera_service is None:
            self.hytera_service = HyteraForwardToPC()

        # run the hytera service
        self.hytera_service.start()
        # run the homebrew service


if __name__ == "__main__":
    t = HyteraHomebrewBridge()
    t.start()
