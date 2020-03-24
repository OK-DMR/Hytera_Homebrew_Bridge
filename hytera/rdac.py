from .generic_service import GenericService
from .storage import Storage


class RDACService(GenericService):
    STEP0_REQUEST = bytes(
        [0x7E, 0x04, 0x00, 0xFE, 0x20, 0x10, 0x00, 0x00, 0x00, 0x0C, 0x60, 0xE1]
    )
    STEP0_RESPONSE = bytes([0x7E, 0x04, 0x00, 0xFD])
    STEP1_REQUEST = bytes(
        [
            0x7E,
            0x04,
            0x00,
            0x00,
            0x20,
            0x10,
            0x00,
            0x01,
            0x00,
            0x18,
            0x9B,
            0x60,
            0x02,
            0x04,
            0x00,
            0x05,
            0x00,
            0x64,
            0x00,
            0x00,
            0x00,
            0x01,
            0xC4,
            0x03,
        ]
    )
    STEP1_RESPONSE = bytes([0x7E, 0x04, 0x00, 0x10])
    STEP2_RESPONSE = bytes([0x7E, 0x04, 0x00, 0x00])
    STEP3_REQUEST = bytes(
        [0x7E, 0x04, 0x00, 0x10, 0x20, 0x10, 0x00, 0x01, 0x00, 0x0C, 0x61, 0xCE]
    )
    STEP3_RESPONSE = bytes([0x7E, 0x04, 0x00, 0x00])
    STEP4_REQUEST_1 = bytes(
        [0x7E, 0x04, 0x00, 0x10, 0x20, 0x10, 0x00, 0x02, 0x00, 0x0C, 0x61, 0xCD]
    )
    STEP4_REQUEST_2 = bytes(
        [
            0x7E,
            0x04,
            0x00,
            0x00,
            0x20,
            0x10,
            0x00,
            0x02,
            0x00,
            0x19,
            0x58,
            0xA0,
            0x02,
            0xD4,
            0x02,
            0x06,
            0x00,
            0x64,
            0x00,
            0x00,
            0x00,
            0x02,
            0x00,
            0xF0,
            0x03,
        ]
    )
    STEP4_RESPONSE_1 = bytes([0x7E, 0x04, 0x00, 0x10])
    STEP4_RESPONSE_2 = bytes([0x7E, 0x04, 0x00, 0x00])
    STEP6_REQUEST_1 = bytes(
        [0x7E, 0x04, 0x00, 0x10, 0x20, 0x10, 0x00, 0x03, 0x00, 0x0C, 0x61, 0xCC]
    )
    STEP6_REQUEST_2 = bytes(
        [
            0x7E,
            0x04,
            0x00,
            0x00,
            0x20,
            0x10,
            0x00,
            0x03,
            0x00,
            0x19,
            0x73,
            0x84,
            0x02,
            0xD6,
            0x82,
            0x06,
            0x00,
            0x00,
            0x64,
            0x00,
            0x00,
            0x00,
            0x02,
            0x6E,
            0x03,
        ]
    )
    STEP6_RESPONSE = bytes([0x7E, 0x04, 0x00, 0x10])
    STEP7_REQUEST = bytes(
        [
            0x7E,
            0x04,
            0x00,
            0x00,
            0x20,
            0x10,
            0x00,
            0x04,
            0x00,
            0x19,
            0x57,
            0x9F,
            0x02,
            0xD4,
            0x02,
            0x06,
            0x00,
            0x64,
            0x00,
            0x00,
            0x00,
            0x02,
            0x01,
            0xEF,
            0x03,
        ]
    )
    STEP7_RESPONSE_1 = bytes([0x7E, 0x04, 0x00, 0x10])
    STEP7_RESPONSE_2 = bytes([0x7E, 0x04, 0x00, 0x00])
    STEP10_REQUEST = bytes(
        [
            0x7E,
            0x04,
            0x00,
            0x00,
            0x20,
            0x10,
            0x00,
            0x15,
            0x00,
            0x18,
            0x9C,
            0x4B,
            0x02,
            0x05,
            0x00,
            0x05,
            0x00,
            0x64,
            0x00,
            0x00,
            0x00,
            0x01,
            0xC3,
            0x03,
        ]
    )
    STEP10_RESPONSE_1 = bytes([0x7E, 0x04, 0x00, 0x10])
    STEP10_RESPONSE_2 = bytes([0x7E, 0x04, 0x00, 0x00])
    STEP12_REQUEST_1 = bytes(
        [0x7E, 0x04, 0x00, 0x10, 0x20, 0x10, 0x00, 0x15, 0x00, 0x0C, 0x61, 0xBA]
    )
    STEP12_REQUEST_2 = bytes(
        [0x7E, 0x04, 0x00, 0xFB, 0x20, 0x10, 0x00, 0x16, 0x00, 0x0C, 0x60, 0xCE]
    )
    STEP12_RESPONSE = bytes([0x7E, 0x04, 0x00, 0xFA])

    def _update_step(self, new_step: int, address: tuple) -> None:
        repeater_info = self.storage.get_repeater_info_by_address(address)
        if repeater_info:
            repeater_info.set_dmr_step(new_step)
            self.storage.set_repeater_info_by_address(address, repeater_info)

    def step0(self, data: bytes, address: tuple) -> None:
        self._update_step(1, address)
        self.serverSocket.sendto(self.STEP0_REQUEST, address)

    def step1(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP0_RESPONSE)] == self.STEP0_RESPONSE:
            self._update_step(2, address)
            self.serverSocket.sendto(self.STEP1_REQUEST, address)

    def step2(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP1_RESPONSE)] == self.STEP1_RESPONSE:
            self._update_step(3, address)

    def step3(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP2_RESPONSE)] == self.STEP2_RESPONSE:
            repeater_info = self.storage.get_repeater_info_by_address(address)
            repeater_info.set_repeater_id(
                int.from_bytes(data[18:3], byteorder="little")
            )
            self.storage.set_repeater_info_by_address(address, repeater_info)
            self._update_step(4, address)
            self.serverSocket.sendto(self.STEP3_REQUEST, address)

    def step4(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP3_RESPONSE)] == self.STEP3_RESPONSE:
            self._update_step(5, address)
            self.serverSocket.sendto(self.STEP4_REQUEST_1, address)
            self.serverSocket.sendto(self.STEP4_REQUEST_2, address)

    def step5(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP4_RESPONSE_1)] == self.STEP4_RESPONSE_1:
            self._update_step(6, address)

    def step6(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP4_RESPONSE_2)] == self.STEP4_RESPONSE_2:
            repeater_info = self.storage.get_repeater_info_by_address(address)
            repeater_info.set_callsign(
                data[88:108]
                .decode("utf_16_le")
                .encode("utf-8")
                .strip(b"\x00")
                .decode("utf-8")
            )
            repeater_info.set_hardware(
                data[120:184]
                .decode("utf_16_le")
                .encode("utf-8")
                .strip(b"\x00")
                .decode("utf-8")
            )
            repeater_info.set_firmware(
                data[56:88]
                .decode("utf_16_le")
                .encode("utf-8")
                .strip(b"\x00")
                .decode("utf-8")
            )
            self.storage.set_repeater_info_by_address(address, repeater_info)
            self._update_step(7, address)
            self.serverSocket.sendto(self.STEP6_REQUEST_1, address)
            self.serverSocket.sendto(self.STEP6_REQUEST_2, address)

    def step7(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP6_RESPONSE)] == self.STEP6_RESPONSE:
            self._update_step(8, address)
            self.serverSocket.sendto(self.STEP7_REQUEST, address)

    def step8(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP7_RESPONSE_1)] == self.STEP7_RESPONSE_1:
            self._update_step(10, address)

    def step10(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP7_RESPONSE_2)] == self.STEP7_RESPONSE_2:
            repeater_info = self.storage.get_repeater_info_by_address(address)
            repeater_info.set_repeater_mode(data[26])
            repeater_info.set_tx_freq(int.from_bytes(data[29:33], byteorder="little"))
            repeater_info.set_rx_freq(int.from_bytes(data[33:37], byteorder="little"))
            self.storage.set_repeater_info_by_address(address, repeater_info)
            self.serverSocket.sendto(self.STEP10_REQUEST, address)
            self._update_step(11, address)

    def step11(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP10_RESPONSE_1)] == self.STEP10_RESPONSE_1:
            self._update_step(12, address)

    def step12(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP10_RESPONSE_2)] == self.STEP10_RESPONSE_2:
            self._update_step(13, address)
            self.serverSocket.sendto(self.STEP12_REQUEST_1, address)
            self.serverSocket.sendto(self.STEP12_REQUEST_2, address)

    def step13(self, data: bytes, address: tuple) -> None:
        if data[: len(self.STEP12_RESPONSE)] == self.STEP12_RESPONSE:
            self._update_step(14, address)
            self.log("rdac completed identification")
            self.log(self.storage.get_repeater_info_by_address(address))

    def step14(self, data: bytes, address: tuple) -> None:
        pass

    def run(self) -> None:
        self.create_socket()
        while True:
            try:
                data, address = self.serverSocket.recvfrom(4096)
                repeater_info = self.storage.get_repeater_info_by_address(address)
                if not repeater_info:
                    # ignoring packet from unknown repeater
                    continue
                if len(data) == 1 and repeater_info.get_dmr_step() != 14:
                    # restart process if response is zero
                    self._update_step(0, address)
                    self.step0(data, address)
                    continue
                elif len(data) != 1 and repeater_info.get_dmr_step() == 14:
                    # single 0x00 byte comes in once in a while, probably heartbeat?
                    self.log("extra data received %s" % data.hex())
                # call correct step function by name
                step_function = getattr(self, "step%d" % repeater_info.get_dmr_step())
                step_function(data, address)
            except Exception as err:
                self.selfLogger.error(err, exc_info=True)


if __name__ == "__main__":
    t = RDACService()
    t.set_storage(Storage()).start()
