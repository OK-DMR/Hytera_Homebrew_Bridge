import time

from .generic_service import GenericHyteraService
from .storage import Storage


class P2PHyteraService(GenericHyteraService):
    # letters P2P
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

    @staticmethod
    def packet_is_command(data: bytes) -> bool:
        return data[:3] == P2PHyteraService.COMMAND_PREFIX

    @staticmethod
    def packet_is_ping(data: bytes) -> bool:
        return data[4:9] == P2PHyteraService.PING_PREFIX

    @staticmethod
    def command_get_type(data: bytes) -> int:
        return data[20] if len(data) > 20 else 0

    def handle_registration(self, data: bytes, address: tuple) -> None:
        ip, port = address
        repeater_idx = self.storage.get_repeater_id_for_remote_address(
            address, create_if_not_exists=True
        )
        self.log(
            "registration of remote %s.%s assigned id %d" % (ip, port, repeater_idx)
        )

        repeater_data = self.storage.get_repeater_info_by_address(address)
        now = time.time()
        if now - repeater_data.get_last_p2p_response() < 10:
            self.log(
                "Ignoring registration request, last response was before %d seconds"
                % (now - repeater_data.get_last_p2p_response())
            )
            return
        repeater_data.set_last_p2p_response(now)
        self.storage.set_repeater_info_by_address(address, repeater_data)

        data = bytearray(data)
        # set repeater ID
        data[4] += 1
        # set operation result status code
        data[13] = 0x01
        data.append(0x01)
        self.serverSocket.sendto(data, address)
        self.log("registration response for %s.%s" % address)
        self.log(data.hex())

    def handle_rdac_request(self, data: bytes, address: tuple) -> None:
        ip, port = address
        repeater_idx = self.storage.get_repeater_id_for_remote_address(
            address, create_if_not_exists=False
        )
        if repeater_idx <= 0:
            self.log(
                "Ignoring RDAC request for unknown repeater (originated from %s:%s)"
                % address
            )
            return

        repeater_data = self.storage.get_repeater_info_by_address(address)
        now = time.time()
        if now - repeater_data.get_last_rdac_response() < 10:
            self.log(
                "Ignoring DMR request, last response was before %d seconds"
                % (now - repeater_data.get_last_rdac_response())
            )
            return
        repeater_data.set_last_rdac_response(now)
        repeater_data.set_rdac_port(port)
        self.storage.set_repeater_info_by_address(address, repeater_data)
        response_address = (repeater_data.get_ip(), repeater_data.get_p2p_port())

        data = bytearray(data)
        # set RDAC id
        data[4] += 1
        # set operation result status code
        data[13] = 0x01
        data.append(0x01)
        self.serverSocket.sendto(data, response_address)
        self.log("RDAC Accept for %s.%s" % response_address)

        # redirect repeater to correct RDAC port
        data = data[: len(data) - 1]
        data[4] = 0x0B
        data[12] = 0xFF
        data[13] = 0xFF
        data[14] = 0x01
        data[15] = 0x00
        data += bytes([0xFF, 0x01])
        from .rdac import RDACHyteraService

        target_rdac_port = self.storage.get_service_port(RDACHyteraService.__name__)
        data += target_rdac_port.to_bytes(2, "little")
        self.log(
            "RDAC Redirect to port %s response for %s.%s"
            % (target_rdac_port, address[0], address[1])
        )
        self.serverSocket.sendto(data, response_address)

    def handle_dmr_request(self, data: bytes, address: tuple) -> None:
        ip, port = address
        repeater_idx = self.storage.get_repeater_id_for_remote_address(
            address, create_if_not_exists=False
        )
        if repeater_idx <= 0:
            self.log(
                "Ignoring DMR request for unknown repeater (originated from %s.%s)"
                % address
            )
            return

        repeater_data = self.storage.get_repeater_info_by_address(address)
        now = time.time()
        if now - repeater_data.get_last_dmr_response() < 10:
            self.log(
                "Ignoring DMR request, last response was before %d seconds"
                % (now - repeater_data.get_last_dmr_response())
            )
            return
        repeater_data.set_last_dmr_response(now)
        repeater_data.set_dmr_port(port)
        self.storage.set_repeater_info_by_address(address, repeater_data)
        response_address = (repeater_data.get_ip(), repeater_data.get_p2p_port())

        data = bytearray(data)
        # set DMR id
        data[4] += 1
        data[13] = 0x01
        data.append(0x01)
        self.serverSocket.sendto(data, response_address)
        self.log("DMR Accept for %s.%s" % address)

        # redirect repeater to correct DMRService port
        data = data[: len(data) - 1]
        data[4] = 0x0B
        data[12] = 0xFF
        data[13] = 0xFF
        data[14] = 0x01
        data[15] = 0x00

        data += bytes([0xFF, 0x01])
        from .dmr import DMRHyteraService

        target_dmr_port = self.storage.get_service_port(DMRHyteraService.__name__)
        data += target_dmr_port.to_bytes(2, "little")
        self.log(
            "DMR Redirect to port %s response for %s.%s"
            % (target_dmr_port, address[0], address[1])
        )
        self.serverSocket.sendto(data, response_address)

    def handle_ping(self, data: bytes, address: tuple) -> None:
        repeater_idx = self.storage.get_repeater_id_for_remote_address(
            address, create_if_not_exists=False
        )
        if repeater_idx <= 0:
            self.log(
                "Ignoring ping for unknown repeater (originated from %s.%s)" % address
            )
            return

        data = bytearray(data)
        data[12] += 1
        self.serverSocket.sendto(data, address)

    def run(self) -> None:
        self.create_socket()
        while True:
            try:
                data, address = self.serverSocket.recvfrom(4096)
                ip, port = address
                packet_type = self.command_get_type(data)
                is_command = self.packet_is_command(data)
                if is_command:
                    if packet_type not in self.KNOWN_PACKET_TYPES:
                        self.log("Received %s bytes from %s:%s" % (len(data), ip, port))
                        self.log(data.hex())
                        self.log("Unknown packet of type:%s received" % packet_type)
                    if packet_type == self.PACKET_TYPE_REQUEST_REGISTRATION:
                        self.handle_registration(data, address)
                    elif packet_type == self.PACKET_TYPE_REQUEST_RDAC_STARTUP:
                        self.handle_rdac_request(data, address)
                    elif packet_type == self.PACKET_TYPE_REQUEST_DMR_STARTUP:
                        self.handle_dmr_request(data, address)
                elif self.packet_is_ping(data):
                    self.handle_ping(data, address)
                else:
                    self.log(
                        "Unknown packet received, %d bytes from %s:%s"
                        % (len(data), ip, port)
                    )
                    self.log(data.hex())
            except Exception as err:
                self.selfLogger.error(err, exc_info=True)


if __name__ == "__main__":
    t = P2PHyteraService()
    t.set_storage(Storage()).start()
