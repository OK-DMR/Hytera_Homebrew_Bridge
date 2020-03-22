from threading import Lock
from .singleton import Singleton
from .constants import *


class RepeaterInfo(dict):
    def get_ip(self):
        return self.get("ip")

    def get_id(self):
        return self.get("id")


@Singleton
class Storage(dict):
    STORAGE_KEY_P2P_PORT = "P2P_port"
    STORAGE_KEY_RDAC_PORT = "RDAC_port"
    STORAGE_KEY_DMR_PORT = "DMR_port"

    storageMutex: Lock = Lock()

    @staticmethod
    def get_repeater_info_storage_key_for_address(address: tuple) -> str:
        ip, port = address
        return "repeater_" + ip

    def get_default_port_p2p(self):
        with self.storageMutex:
            return self.get(self.STORAGE_KEY_P2P_PORT, DEFAULT_P2P_PORT)

    def get_default_port_rdac(self):
        with self.storageMutex:
            return self.get(self.STORAGE_KEY_RDAC_PORT, DEFAULT_RDAC_PORT)

    def get_default_port_dmr(self):
        with self.storageMutex:
            return self.get(self.STORAGE_KEY_DMR_PORT, DEFAULT_DMR_PORT)

    def set_default_port_p2p(self, port: int) -> None:
        with self.storageMutex:
            self[self.STORAGE_KEY_P2P_PORT] = port

    def set_default_port_rdac(self, port: int) -> None:
        with self.storageMutex:
            self[self.STORAGE_KEY_RDAC_PORT] = port

    def set_default_port_dmr(self, port: int) -> None:
        with self.storageMutex:
            self[self.STORAGE_KEY_DMR_PORT] = port

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
        with self.storageMutex:
            return self.get(storage_key)
