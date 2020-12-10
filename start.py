#!/usr/bin/env python3

import configparser
from threading import Thread

from homebrew.homebrew_service import HomebrewService
from hytera_common.hytera_service_interface import HyteraServiceInterface
from hytera_forward_to_pc.hytera_forward_to_pc import HyteraForwardToPC
from hytera_ip_site_connect.hytera_ipsc import HyteraIPSiteConnect


class HyteraHomebrewBridge(Thread):
    hytera_service: HyteraServiceInterface = None
    homebrew_service: HomebrewService = None

    def start(self):
        # load settings
        self.load_settings()
        # run the hytera service
        self.hytera_service.start()
        # run the homebrew service
        self.homebrew_service.start()

    def load_settings(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read("settings.ini")
        if "general" in config:
            if "mode" in config["general"]:
                if config["general"]["mode"] == "ip-site-connect":
                    print("ip-site-connect mode")
                    self.hytera_service = HyteraIPSiteConnect()

        # fallback
        if self.hytera_service is None:
            print("forward-to-pc mode")
            self.hytera_service = HyteraForwardToPC()


if __name__ == "__main__":
    t = HyteraHomebrewBridge()
    t.start()
