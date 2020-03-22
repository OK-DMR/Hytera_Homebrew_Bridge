from threading import Lock
import hashlib


class RepeaterInfo(dict):
    def get_ip(self):
        return self.get("ip")

    def get_id(self):
        return self.get("id")


class Storage(dict):
    storageMutex: Lock = Lock()

    def get_repeater_id_for_remote_ip(self, ip: str) -> int:
        return self.get_repeater_id_for_remote_address((ip, 0))

    def get_repeater_id_for_remote_address(self, address: tuple) -> int:
        ip, port = address
        with self.storageMutex:
            repeater_data: RepeaterInfo = self.get("repeater_" + ip)
            if not repeater_data:
                repeater_data = RepeaterInfo()
                repeater_idx = self.get("repeaters_count", 1) + 1
                self["repeaters_count"] = repeater_idx
                repeater_data["id"] = repeater_idx
                self["repeater_" + ip] = repeater_data
                return repeater_idx
            return repeater_data.get_id()
