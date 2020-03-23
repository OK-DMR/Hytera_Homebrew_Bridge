from threading import Lock
from .constants import *


class RepeaterInfo(dict):
    def get_ip(self):
        return self.get("ip")

    def get_id(self):
        return self.get("id")


class Storage(dict):
    STORAGE_KEY_P2P_PORT = "P2P_port"
    STORAGE_KEY_RDAC_PORT = "RDAC_port"
    STORAGE_KEY_DMR_PORT = "DMR_port"

    storageMutex: Lock = Lock()

    @staticmethod
    def get_repeater_info_storage_key_for_address(address: tuple) -> str:
        ip, port = address
        return "repeater_" + ip

    def get_service_port(self, service_name: str) -> int:
        from .p2p import P2PService
        from .rdac import RDACService
        from .dmr import DMRService

        if service_name == P2PService.__name__:
            return self.get(self.STORAGE_KEY_P2P_PORT, DEFAULT_P2P_PORT)
        elif service_name == RDACService.__name__:
            return self.get(self.STORAGE_KEY_RDAC_PORT, DEFAULT_RDAC_PORT)
        elif service_name == DMRService.__name__:
            return self.get(self.STORAGE_KEY_DMR_PORT, DEFAULT_DMR_PORT)
        raise TypeError("Unknown service type: %s" % service_name)

    def set_service_port(self, service_name: str, port: int) -> None:
        if port > 65535 or port < 1:
            port = None

        from .p2p import P2PService
        from .rdac import RDACService
        from .dmr import DMRService

        if service_name == P2PService.__name__:
            self[self.STORAGE_KEY_P2P_PORT] = port if port else DEFAULT_P2P_PORT
        elif service_name == RDACService.__name__:
            self[self.STORAGE_KEY_RDAC_PORT] = port if port else DEFAULT_RDAC_PORT
        elif service_name == DMRService.__name__:
            self[self.STORAGE_KEY_DMR_PORT] = port if port else DEFAULT_DMR_PORT

    def get_service_ip(self):
        return DEFAULT_SERVICE_IP

    def get_repeater_id_for_remote_ip(self, ip: str) -> int:
        return self.get_repeater_id_for_remote_address((ip, 0))

    def get_repeater_id_for_remote_address(
        self, address: tuple, create_if_not_exists=False
    ) -> int:
        storage_key = self.get_repeater_info_storage_key_for_address(address)
        with self.storageMutex:
            repeater_data: RepeaterInfo = self.get(storage_key)
            if not repeater_data:
                if not create_if_not_exists:
                    return -1
                repeater_data = RepeaterInfo()
                repeater_idx = self.get("repeaters_count", 1) + 1
                self["repeaters_count"] = repeater_idx
                repeater_data["id"] = repeater_idx
                self[storage_key] = repeater_data
                return repeater_idx
            return repeater_data.get_id()

    def get_repeater_info_by_ip(self, ip: str) -> RepeaterInfo:
        return self.get_repeater_info_by_address((ip, 0))

    def get_repeater_info_by_address(self, address: tuple) -> RepeaterInfo:
        storage_key = self.get_repeater_info_storage_key_for_address(address)
        return self.get(storage_key)
