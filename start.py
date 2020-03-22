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
    storage: Storage = Storage.instance()

    def load_settings(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read("settings.ini")
        if "constants" in config:
            constants = config["constants"]
            if "DEFAULT_SERVICE_PORT" in constants:
                self.storage.set_default_port_p2p(
                    config["constants"]["DEFAULT_SERVICE_PORT"]
                )
            if "DEFAULT_DMR_PORT" in constants:
                self.storage.set_default_port_dmr(
                    config["constants"]["DEFAULT_DMR_PORT"]
                )
            if "DEFAULT_RDAC_PORT" in constants:
                self.storage.set_default_port_rdac(
                    config["constants"]["DEFAULT_RDAC_PORT"]
                )

    def start(self) -> None:
        self.p2p_service.start()
        self.dmr_service.start()
        self.rdac_service.start()


if __name__ == "__main__":
    t = HyteraHomebrewBridge()
    t.start()
