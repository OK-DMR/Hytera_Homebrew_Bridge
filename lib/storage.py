from threading import Lock
from .constants import *


class RepeaterInfo(dict):
    KEY_IP = "ip"
    KEY_ID = "id"
    KEY_LAST_RDAC_RESPONSE = "last_rdac_response"
    KEY_LAST_P2P_RESPONSE = "last_p2p_response"
    KEY_LAST_DMR_RESPONSE = "last_dmr_response"
    KEY_REMOTE_P2P_PORT = "remote_p2p_port"
    KEY_REMOTE_RDAC_PORT = "remote_rdac_port"
    KEY_REMOTE_DMR_PORT = "remote_dmr_port"
    KEY_DMR_STEP = "current_dmr_step"

    def get_ip(self):
        return self.get(self.KEY_IP)

    def set_ip(self, ip: str):
        self[self.KEY_IP] = ip

    def get_id(self):
        return self.get(self.KEY_ID)

    def set_id(self, new_id: int):
        self[self.KEY_ID] = new_id

    def get_dmr_step(self):
        return self.get(self.KEY_DMR_STEP, 0)

    def get_p2p_port(self):
        return self.get(self.KEY_REMOTE_P2P_PORT)

    def set_p2p_port(self, port: int):
        self[self.KEY_REMOTE_P2P_PORT] = int(port)

    def get_rdac_port(self):
        return self.get(self.KEY_REMOTE_RDAC_PORT)

    def set_rdac_port(self, port: int):
        self[self.KEY_REMOTE_RDAC_PORT] = int(port)

    def get_dmr_port(self):
        return self.get(self.KEY_REMOTE_DMR_PORT)

    def set_dmr_port(self, port: int):
        self[self.KEY_REMOTE_DMR_PORT] = int(port)

    def get_last_rdac_response(self):
        return self.get(self.KEY_LAST_RDAC_RESPONSE, 0)

    def set_last_rdac_response(self, time):
        self[self.KEY_LAST_RDAC_RESPONSE] = time

    def get_last_p2p_response(self):
        return self.get(self.KEY_LAST_P2P_RESPONSE, 0)

    def set_last_p2p_response(self, time):
        self[self.KEY_LAST_P2P_RESPONSE] = time

    def get_last_dmr_response(self):
        return self.get(self.KEY_LAST_DMR_RESPONSE, 0)

    def set_last_dmr_response(self, time):
        self[self.KEY_LAST_DMR_RESPONSE] = time


class Storage(dict):
    STORAGE_KEY_P2P_PORT = "P2P_port"
    STORAGE_KEY_RDAC_PORT = "RDAC_port"
    STORAGE_KEY_DMR_PORT = "DMR_port"
    STORAGE_KEY_SERVICE_IP = "Service_IP"

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
        return self.get(self.STORAGE_KEY_SERVICE_IP, DEFAULT_SERVICE_IP)

    def set_service_ip(self, new_ip: str):
        self[self.STORAGE_KEY_SERVICE_IP] = new_ip if new_ip else DEFAULT_SERVICE_IP

    def get_repeater_id_for_remote_ip(self, ip: str) -> int:
        return self.get_repeater_id_for_remote_address((ip, 0))

    def get_repeater_id_for_remote_address(
        self, address: tuple, create_if_not_exists=False
    ) -> int:
        storage_key = self.get_repeater_info_storage_key_for_address(address)
        ip, port = address
        with self.storageMutex:
            repeater_data: RepeaterInfo = self.get(storage_key)
            if not repeater_data:
                if not create_if_not_exists:
                    return -1
                repeater_data = RepeaterInfo()
                repeater_idx = self.get("repeaters_count", 1) + 1
                self["repeaters_count"] = repeater_idx
                repeater_data.set_id(repeater_idx)
                repeater_data.set_ip(ip)
                repeater_data.set_p2p_port(port)
                self[storage_key] = repeater_data
                return repeater_idx
            return repeater_data.get_id()

    def get_repeater_info_by_ip(self, ip: str) -> RepeaterInfo:
        return self.get_repeater_info_by_address((ip, 0))

    def get_repeater_info_by_address(self, address: tuple) -> RepeaterInfo:
        storage_key = self.get_repeater_info_storage_key_for_address(address)
        return self.get(storage_key)

    def set_repeater_info_by_address(self, address: tuple, info: RepeaterInfo) -> None:
        with self.storageMutex:
            self[self.get_repeater_info_storage_key_for_address(address)] = info
