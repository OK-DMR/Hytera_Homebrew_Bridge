from .generic_service import GenericService
from .constants import *


class P2PService(GenericService):

    COMMAND_PREFIX: bytes = bytes([0x50, 0x32, 0x50])
    PING_PREFIX: bytes = bytes([0x0A, 0x00, 0x00, 0x00, 0x14])

    PACKET_TYPE_REQUEST_REGISTRATION = 0x10
    PACKET_TYPE_REQUEST_DMR_STARTUP = 0x11
    PACKET_TYPE_REQUEST_RDAC_STARTUP = 0x12
    KNOWN_PACKET_TYPES = [
        PACKET_TYPE_REQUEST_DMR_STARTUP,
        PACKET_TYPE_REQUEST_RDAC_STARTUP,
        PACKET_TYPE_REQUEST_REGISTRATION,
    ]

    def __init__(self):
        super().__init__()
        self.listenPort = self.DEFAULT_LISTEN_PORT = DEFAULT_P2P_PORT

    def packet_is_command(self, data: bytes) -> bool:
        ret = data[:3] == self.COMMAND_PREFIX
        self.log("packet_is_command:%s" % ret)
        return ret

    def packet_is_ping(self, data: bytes) -> bool:
        ret = data[4:5] == self.PING_PREFIX
        self.log("packet_is_ping:%s" % ret)
        return ret

    def command_get_type(self, data: bytes) -> int:
        ret = data[20] if len(data) > 20 else 0
        self.log("command_get_type:%s (datalen:%s)" % (ret, len(data)))
        return ret

    def handle_registration(self, data: bytes, address: tuple) -> None:
        ip, port = address
        repeater_idx = self.storage.get_repeater_id_for_remote_address(
            address, create_if_not_exists=True
        )
        self.log(
            "registration of remote %s.%s assigned id %d" % (ip, port, repeater_idx)
        )
        data = bytearray(data)
        # set repeater ID
        data[4] = repeater_idx
        # set operation result status code
        data[13] = 0x01
        data.append(0x01)
        self.serverSocket.sendto(data, address)
        self.log("registration response for %s.%s" % address)
        self.log(data.hex())

    def handle_rdac_request(self, data: bytes, address: tuple) -> None:
        repeater_idx = self.storage.get_repeater_id_for_remote_address(
            address, create_if_not_exists=False
        )
        if repeater_idx <= 0:
            self.log(
                "Ignoring RDAC request for unknown repeater (originated from %s.%s)"
                % address
            )
            return
        data = bytearray(data)
        # set RDAC id
        data[4] = repeater_idx
        # set operation result status code
        data[13] = 0x01
        data.append(0x01)
        self.serverSocket.sendto(data, address)
        self.log("rdac response for %s.%s" % address)
        self.log(data.hex())

    def handle_dmr_request(self, data: bytes, address: tuple) -> None:
        repeater_idx = self.storage.get_repeater_id_for_remote_address(
            address, create_if_not_exists=False
        )
        if repeater_idx <= 0:
            self.log(
                "Ignoring DMR request for unknown repeater (originated from %s.%s)"
                % address
            )
            return
        data = bytearray(data)
        # set DMR id
        data[4] = repeater_idx
        data[13] = 0x01
        data.append(0x01)
        self.serverSocket.sendto(data, address)
        self.log("dmr response for %s.%s" % address)
        self.log(data.hex())

    def handle_ping(self, data: bytes, address: tuple) -> None:
        data = bytearray(data)
        data[12] += 1
        self.serverSocket.sendto(data, address)
        self.log("pong sent to %s.%s" % address)
        self.log(data.hex())

    def run(self) -> None:
        self.create_socket()
        while True:
            try:
                data, address = self.serverSocket.recvfrom(4096)
                ip, port = address
                packet_type = self.command_get_type(data)
                is_command = self.packet_is_command(data)
                self.log("Received %s bytes from %s:%s" % (len(data), ip, port))
                self.log(data.hex())
                if is_command:
                    if packet_type not in self.KNOWN_PACKET_TYPES:
                        self.log("Unknown packet of type:%s received" % packet_type)
                    if packet_type == self.PACKET_TYPE_REQUEST_REGISTRATION:
                        self.handle_registration(data, address)
                    elif packet_type == self.PACKET_TYPE_REQUEST_RDAC_STARTUP:
                        self.handle_rdac_request(data, address)
                    elif packet_type == self.PACKET_TYPE_REQUEST_DMR_STARTUP:
                        self.handle_dmr_request(data, address)
                elif self.packet_is_ping(data):
                    self.handle_ping(data, address)
            except Exception as err:
                self.selfLogger.error(err, exc_info=True)


if __name__ == "__main__":
    t = P2PService()
    t.start()
