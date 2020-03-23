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

    def _update_step(self, new_step: int, address: tuple) -> None:
        repeater_info = self.storage.get_repeater_info_by_address(address)
        if repeater_info:
            self.log("_update_step to %d" % new_step)
            repeater_info.set_dmr_step(new_step)
            self.storage.set_repeater_info_by_address(address, repeater_info)

    def step0(self, data: bytes, address: tuple) -> None:
        self._update_step(1, address)
        self.serverSocket.sendto(self.STEP0_REQUEST, address)

    def step1(self, data: bytes, address: tuple) -> None:
        if data == self.STEP0_RESPONSE:
            self._update_step(2, address)
            self.serverSocket.sendto(self.STEP1_REQUEST, address)

    def step2(self, data: bytes, address: tuple) -> None:
        if data == self.STEP1_RESPONSE:
            self._update_step(3, address)

    def step3(self, data: bytes, address: tuple) -> None:
        if data == self.STEP2_RESPONSE:
            self._update_step(4, address)

    def run(self) -> None:
        self.create_socket()
        while True:
            try:
                data, address = self.serverSocket.recvfrom(4096)
                ip, port = address
                self.log("data (%d) received from %s.%s" % (len(data), ip, port))
                self.log(data.hex())
                repeater_info = self.storage.get_repeater_info_by_address(address)
                if not repeater_info:
                    # ignoring packet from unknown repeater
                    continue
                if len(data) == 1 and repeater_info.get_dmr_step() != 1:
                    # restart process if response is zero
                    self._update_step(0, address)
                # call correct step function by name
                self.log("running current step: %d" % repeater_info.get_dmr_step())
                step_function = getattr(self, "step%d" % repeater_info.get_dmr_step())
                step_function(data, address)
            except Exception as err:
                self.selfLogger.error(err, exc_info=True)


if __name__ == "__main__":
    t = RDACService()
    t.set_storage(Storage()).start()
