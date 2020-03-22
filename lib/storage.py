from threading import Lock
from singleton import Singleton


class RepeaterInfo(dict):
    def get_ip(self):
        return self.get("ip")

    def get_id(self):
        return self.get("id")


@Singleton
class Storage(dict):
    storageMutex: Lock = Lock()

    @staticmethod
    def get_repeater_info_storage_key_for_address(address: tuple):
        ip, port = address
        return "repeater_" + ip

    def get_repeater_id_for_remote_ip(self, ip: str) -> int:
        return self.get_repeater_id_for_remote_address((ip, 0))

    def get_repeater_id_for_remote_address(self, address: tuple, create_if_not_exists=False) -> int:
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

    def get_repeater_info_by_address(self, address: tuple):
        storage_key = self.get_repeater_info_storage_key_for_address(address)
        with self.storageMutex:
            return self.get(storage_key)
