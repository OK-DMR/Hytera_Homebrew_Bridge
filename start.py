#!/usr/bin/env python3

from threading import Thread
from lib.p2p import P2PService
from lib.dmr import DMRService
from lib.rdac import RDACService
from lib.storage import Storage
import configparser


class HyteraHomebrewBridge(Thread):
    p2p_service: P2PService = P2PService()
    dmr_service: DMRService = DMRService()
    rdac_service: RDACService = RDACService()
    storage: Storage = Storage()

    def load_settings(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read("settings.ini")
        if "constants" in config:
            constants = config["constants"]
            if "default_service_port" in constants:
                self.storage.set_service_port(
                    P2PService.__name__, int(constants["default_service_port"])
                )
            if "default_dmr_port" in constants:
                self.storage.set_service_port(
                    DMRService.__name__, int(constants["default_dmr_port"])
                )
            if "default_rdac_port" in constants:
                self.storage.set_service_port(
                    RDACService.__name__, int(constants["default_rdac_port"])
                )
            if "default_service_ip" in constants:
                self.storage.set_service_ip(str(constants["default_service_ip"]))

    def start(self) -> None:
        self.load_settings()

        self.dmr_service.set_storage(self.storage).start()
        self.rdac_service.set_storage(self.storage).start()
        self.p2p_service.set_storage(self.storage).start()


if __name__ == "__main__":
    t = HyteraHomebrewBridge()
    t.start()
