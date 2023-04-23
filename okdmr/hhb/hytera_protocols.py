#!/usr/bin/env python3
import asyncio
import socket
from asyncio import transports, Queue
from binascii import hexlify
from typing import Optional, Tuple, Dict

from kaitaistruct import ValidationNotEqualError, KaitaiStruct
from okdmr.dmrlib.utils.parsing import parse_hytera_data
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol

from okdmr.hhb.callback_interface import CallbackInterface
from okdmr.hhb.custom_bridge_datagram_protocol import (
    CustomBridgeDatagramProtocol,
)
from okdmr.hhb.packet_format import (
    common_log_format,
)
from okdmr.hhb.settings import BridgeSettings


class HyteraP2PProtocol(CustomBridgeDatagramProtocol):
    COMMAND_PREFIX: bytes = bytes([0x50, 0x32, 0x50])
    PING_PREFIX: bytes = bytes([0x0A, 0x00, 0x00, 0x00, 0x14])
    ACK_PREFIX: bytes = bytes([0x0C, 0x00, 0x00, 0x00, 0x14])

    PACKET_TYPE_REQUEST_REGISTRATION = 0x10
    PACKET_TYPE_REQUEST_DMR_STARTUP = 0x11
    PACKET_TYPE_REQUEST_RDAC_STARTUP = 0x12
    KNOWN_PACKET_TYPES = [
        PACKET_TYPE_REQUEST_DMR_STARTUP,
        PACKET_TYPE_REQUEST_RDAC_STARTUP,
        PACKET_TYPE_REQUEST_REGISTRATION,
    ]

    def __init__(
        self, settings: BridgeSettings, repeater_accepted_callback: CallbackInterface
    ):
        super().__init__(settings)
        self.transport: Optional[transports.DatagramTransport] = None
        self.repeater_accepted_callback = repeater_accepted_callback

    @staticmethod
    def packet_is_command(data: bytes) -> bool:
        return data[:3] == HyteraP2PProtocol.COMMAND_PREFIX

    @staticmethod
    def packet_is_ping(data: bytes) -> bool:
        return data[4:9] == HyteraP2PProtocol.PING_PREFIX

    @staticmethod
    def packet_is_ack(data: bytes) -> bool:
        return data[4:9] == HyteraP2PProtocol.ACK_PREFIX

    @staticmethod
    def command_get_type(data: bytes) -> int:
        return data[20] if len(data) > 20 else 0

    def handle_registration(self, data: bytes, address: Tuple[str, int]) -> None:
        data = bytearray(data)
        data[3] = 0x50
        # set repeater ID
        data[4] += 1
        # set operation result status code
        data[13] = 0x01
        data[14] = 0x01
        data[15] = 0x5A
        data.append(0x01)

        self.transport.sendto(data, address)

        asyncio.gather(self.hytera_repeater_obtain_snmp(address))
        self.settings.hytera_is_registered[address[0]] = True
        asyncio.get_running_loop().create_task(
            self.repeater_accepted_callback.homebrew_connect(address[0])
        )

    def handle_rdac_request(self, data: bytes, address: Tuple[str, int]) -> None:
        if not self.settings.hytera_is_registered.get(address[0]):
            self.log_debug(
                f"Rejecting RDAC request for not-registered repeater {address[0]}"
            )
            self.transport.sendto(bytes([0x00]), address)
            return

        response_address = (address[0], self.settings.p2p_port)

        data = bytearray(data)
        # set RDAC id
        data[4] += 1
        # set operation result status code
        data[13] = 0x01
        data.append(0x01)

        self.settings.hytera_repeater_data[address[0]].hytera_repeater_ip = address[0]

        self.transport.sendto(data, response_address)
        self.log_debug("RDAC Accept for %s:%s" % address)

        # redirect repeater to correct RDAC port
        data = self.get_redirect_packet(data, self.settings.rdac_port)
        self.transport.sendto(data, response_address)

    @staticmethod
    def get_redirect_packet(data: bytearray, target_port: int):
        print(f"Providing redirect packet to port {target_port}")
        data = data[: len(data) - 1]
        data[4] = 0x0B
        data[12] = 0xFF
        data[13] = 0xFF
        data[14] = 0x01
        data[15] = 0x00
        data += bytes([0xFF, 0x01])
        data += target_port.to_bytes(2, "little")
        return data

    def handle_dmr_request(self, data: bytes, address: Tuple[str, int]) -> None:
        if not self.settings.hytera_is_registered.get(address[0]):
            self.log_debug(
                f"Rejecting DMR request for not-registered repeater {address[0]}"
            )
            self.transport.sendto(bytes([0x00]), address)
            return

        response_address = (address[0], self.settings.p2p_port)

        data = bytearray(data)
        # set DMR id
        data[4] += 1
        data[13] = 0x01
        data.append(0x01)

        self.transport.sendto(data, response_address)
        self.log_debug("DMR Accept for %s:%s" % address)

        data = self.get_redirect_packet(
            data, self.settings.get_repeater_dmr_port(address[0])
        )
        self.transport.sendto(data, response_address)

    def handle_ping(self, data: bytes, address: Tuple[str, int]) -> None:
        if not self.settings.hytera_is_registered.get(address[0]):
            self.log_debug(
                f"Rejecting ping request for not-registered repeater {address[0]}"
            )
            self.transport.sendto(bytes([0x00]), address)
            return
        data = bytearray(data)
        data[12] = 0xFF
        data[14] = 0x01
        self.transport.sendto(data, address)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.log_debug("connection lost")
        if exc:
            self.log_exception(exc)

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.transport = transport
        sock: socket.socket = transport.get_extra_info("socket")
        if sock:
            self.log_debug(f"new peer {sock}")
        self.log_debug("connection prepared")

    def datagram_received(self, data: bytes, address: Tuple[str, int]) -> None:
        packet_type = self.command_get_type(data)
        is_command = self.packet_is_command(data)
        self.settings.ensure_repeater_data(address)
        if is_command:
            if packet_type not in self.KNOWN_PACKET_TYPES:
                if not self.packet_is_ack(data):
                    self.log_error("Received %s bytes from %s" % (len(data), address))
                    self.log_error(data.hex())
                    self.log_error("Idle packet of type:%s received" % packet_type)
            if packet_type == self.PACKET_TYPE_REQUEST_REGISTRATION:
                self.handle_registration(data, address)
            elif packet_type == self.PACKET_TYPE_REQUEST_RDAC_STARTUP:
                self.handle_rdac_request(data, address)
            elif packet_type == self.PACKET_TYPE_REQUEST_DMR_STARTUP:
                self.handle_dmr_request(data, address)
        elif self.packet_is_ping(data):
            self.handle_ping(data, address)
        else:
            self.log_error(
                "Idle packet received, %d bytes from %s" % (len(data), address)
            )
            self.log_debug(data.hex())

    def send_connection_reset(self):
        self.log_debug("Sending Connection Reset")
        self.transport.sendto(bytes([0x00]))

    def disconnect(self):
        self.log_warning("Self Disconnect")
        if self.transport and not self.transport.is_closing():
            self.send_connection_reset()


class HyteraRDACProtocol(CustomBridgeDatagramProtocol):
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

    def __init__(
        self, settings: BridgeSettings, rdac_completed_callback: CallbackInterface
    ):
        super().__init__(settings)
        self.transport: Optional[transports.DatagramTransport] = None
        self.rdac_completed_callback = rdac_completed_callback
        self.step: Dict[str, int] = dict()

    def step0(self, _: bytes, address: Tuple[str, int]) -> None:
        self.log_debug("RDAC identification started")
        self.step[address[0]] = 1
        self.transport.sendto(self.STEP0_REQUEST, address)

    def step1(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP0_RESPONSE)] == self.STEP0_RESPONSE:
            self.step[address[0]] = 2
            self.transport.sendto(self.STEP1_REQUEST, address)

    def step2(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP1_RESPONSE)] == self.STEP1_RESPONSE:
            self.step[address[0]] = 3

    def step3(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP2_RESPONSE)] == self.STEP2_RESPONSE:
            self.settings.hytera_repeater_id = int.from_bytes(
                data[18:21], byteorder="little"
            )
            self.step[address[0]] = 4
            self.transport.sendto(self.STEP3_REQUEST, address)

    def step4(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP3_RESPONSE)] == self.STEP3_RESPONSE:
            self.step[address[0]] = 5
            self.transport.sendto(self.STEP4_REQUEST_1, address)
            self.transport.sendto(self.STEP4_REQUEST_2, address)

    def step5(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP4_RESPONSE_1)] == self.STEP4_RESPONSE_1:
            self.step[address[0]] = 6

    def step6(self, data: bytes, address: Tuple[str, int]) -> None:
        ip: str = address[0]
        if data[: len(self.STEP4_RESPONSE_2)] == self.STEP4_RESPONSE_2:
            self.settings.hytera_repeater_data[ip].hytera_callsign = (
                data[88:108]
                .decode("utf_16_le")
                .encode("utf-8")
                .strip(b"\x00")
                .decode("utf-8")
            )
            self.settings.hytera_repeater_data[ip].hytera_hardware = (
                data[120:184]
                .decode("utf_16_le")
                .encode("utf-8")
                .strip(b"\x00")
                .decode("utf-8")
            )
            self.settings.hytera_repeater_data[ip].hytera_firmware = (
                data[56:88]
                .decode("utf_16_le")
                .encode("utf-8")
                .strip(b"\x00")
                .decode("utf-8")
            )
            self.settings.hytera_repeater_data[ip].hytera_serial_number = (
                data[184:216]
                .decode("utf_16_le")
                .encode("utf-8")
                .strip(b"\x00")
                .decode("utf-8")
            )
            self.step[address[0]] = 7
            self.transport.sendto(self.STEP6_REQUEST_1, address)
            self.transport.sendto(self.STEP6_REQUEST_2, address)

    def step7(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP6_RESPONSE)] == self.STEP6_RESPONSE:
            self.step[address[0]] = 8
            self.transport.sendto(self.STEP7_REQUEST, address)

    def step8(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP7_RESPONSE_1)] == self.STEP7_RESPONSE_1:
            self.step[address[0]] = 10

    def step10(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP7_RESPONSE_2)] == self.STEP7_RESPONSE_2:
            self.settings.hytera_repeater_data[address[0]].hytera_repeater_mode = data[
                26
            ]
            self.settings.hytera_repeater_data[
                address[0]
            ].hytera_tx_freq = int.from_bytes(data[29:33], byteorder="little")
            self.settings.hytera_repeater_data[
                address[0]
            ].hytera_rx_freq = int.from_bytes(data[33:37], byteorder="little")
            self.step[address[0]] = 11
            self.transport.sendto(self.STEP10_REQUEST, address)

    def step11(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP10_RESPONSE_1)] == self.STEP10_RESPONSE_1:
            self.step[address[0]] = 12

    def step12(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP10_RESPONSE_2)] == self.STEP10_RESPONSE_2:
            self.step[address[0]] = 13
            self.transport.sendto(self.STEP12_REQUEST_1, address)
            self.transport.sendto(self.STEP12_REQUEST_2, address)

    def step13(self, data: bytes, address: Tuple[str, int]) -> None:
        if data[: len(self.STEP12_RESPONSE)] == self.STEP12_RESPONSE:
            self.step[address[0]] = 14
            self.log_debug("rdac completed identification")
            self.settings.print_repeater_configuration()
            asyncio.gather(self.hytera_repeater_obtain_snmp(address))
            asyncio.get_running_loop().create_task(
                self.rdac_completed_callback.homebrew_connect(address[0])
            )

    def step14(self, data: bytes, address: Tuple[str, int]) -> None:
        pass

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.log_info("connection lost")
        if exc:
            self.log_exception(exc)

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.transport = transport
        self.log_debug("connection prepared")

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        self.settings.ensure_repeater_data(addr)

        if not self.step.get(addr[0]):
            self.step[addr[0]] = 0

        if len(data) == 1 and self.step[addr[0]] != 14:
            if self.step[addr[0]] == 4:
                self.log_warning(
                    "check repeater zone programming, if Digital IP"
                    "Multi-Site Connect mode allows data pass from timeslots"
                )
            self.log_warning(
                "restart process if response is protocol reset and current step is not 14"
            )
            self.step[addr[0]] = 0
            self.step0(data, addr)
        elif len(data) != 1 and self.step[addr[0]] == 14:
            self.log_error("RDAC finished, received extra data %s" % hexlify(data))
        elif len(data) == 1 and self.step[addr[0]] == 14:
            if data[0] == 0x00:
                # no data available response
                self.transport.sendto(bytes(0x41), addr)
        else:
            getattr(self, "step%d" % self.step[addr[0]])(data, addr)


class HyteraDMRProtocol(CustomBridgeDatagramProtocol):
    def __init__(
        self,
        settings: BridgeSettings,
        queue_incoming: Queue,
        queue_outgoing: Queue,
        hytera_repeater_ip: str,
    ) -> None:
        super().__init__(settings)
        self.transport: Optional[transports.DatagramTransport] = None
        self.queue_incoming = queue_incoming
        self.queue_outgoing = queue_outgoing
        self.ip: str = hytera_repeater_ip
        print(
            f"HyteraDMRProtocol on creation expecting ip {self.ip} and port {self.settings.get_repeater_dmr_port(self.ip)}"
        )

    async def send_hytera_from_queue(self) -> None:
        while asyncio.get_running_loop().is_running():
            ip, packet = await self.queue_outgoing.get()
            assert isinstance(ip, str)
            assert isinstance(packet, bytes)
            if self.transport and not self.transport.is_closing():
                ipsc = IpSiteConnectProtocol.from_bytes(packet)
                self.log_debug(
                    common_log_format(
                        proto="HHB->HYTER",
                        from_ip_port=(),
                        to_ip_port=(),
                        use_color=True,
                        packet_data=ipsc,
                        dmrdata_hash="",
                    )
                )
                self.transport.sendto(packet, (ip, self.settings.dmr_port))

            # notify about outbound done
            self.queue_outgoing.task_done()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.log_info("connection lost")
        if exc:
            self.log_exception(exc)

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.transport = transport
        self.log_debug("connection prepared")

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        if self.ip != addr[0]:
            self.log_debug(
                f"HyteraDMRProtocol ignore from {addr[0]} expected {self.ip} data {data.hex()}"
            )
            return
        else:
            self.log_debug(f"HyteraDMRProtocol accept from {addr[0]} data {data.hex()}")

        self.settings.ensure_repeater_data(addr)

        try:
            hytera_data: KaitaiStruct = parse_hytera_data(data)
            self.queue_incoming.put_nowait((addr[0], hytera_data))

            self.log_debug(
                common_log_format(
                    proto="HYTER->HHB",
                    from_ip_port=(),
                    to_ip_port=(),
                    use_color=True,
                    packet_data=hytera_data,
                    dmrdata_hash="",
                )
            )
        except EOFError as e:
            self.log_error(f"Cannot parse IPSC DMR packet {hexlify(data)} from {addr}")
            self.log_exception(e)
        except ValidationNotEqualError as e:
            self.log_error(f"Cannot parse IPSC DMR packet {hexlify(data)} from {addr}")
            self.log_error("Parser for Hytera data failed to match the packet data")
            self.log_exception(e)
        except BaseException as e:
            self.log_error("[datagram_received] unhandled exception")
            self.log_exception(e)