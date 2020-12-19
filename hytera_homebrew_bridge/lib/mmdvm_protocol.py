#!/usr/bin/env python3
import asyncio
import struct
from asyncio import transports
from binascii import hexlify, a2b_hex
from hashlib import sha256
from typing import Optional, Callable, Tuple

from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.lib.logging_protocol import LoggingProtocol
from hytera_homebrew_bridge.lib.settings import BridgeSettings


class MMDVMProtocol(LoggingProtocol):
    CON_NEW: int = 1
    CON_LOGIN_REQUEST_SENT: int = 2
    CON_LOGIN_RESPONSE_SENT: int = 3
    CON_LOGIN_SUCCESSFULL: int = 4
    CON_AUTHENTICATION_FAILED: int = 5

    def __init__(self, settings: BridgeSettings, connection_lost_callback: Callable):
        super().__init__(settings)
        self.settings = settings
        self.transport: Optional[transports.DatagramTransport] = None
        self.connection_lost_callback = connection_lost_callback
        self.connection_status = self.CON_NEW

    async def periodic_maintenance(self):
        while not asyncio.get_event_loop().is_closed():
            await asyncio.sleep(5)
            if self.connection_status == self.CON_NEW:
                self.send_login_request()
            elif self.connection_status == self.CON_LOGIN_REQUEST_SENT:
                self.send_login_request()
            elif self.connection_status == self.CON_LOGIN_SUCCESSFULL:
                self.send_ping()
            elif self.connection_status == self.CON_AUTHENTICATION_FAILED:
                self.connection_status = self.CON_NEW
                self.send_login_request()

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.log("MMDVM socket connected")
        self.transport = transport
        self.send_login_request()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        self.log("MMDVM socket closed")
        if exc:
            self.logger.exception(exc)
        self.connection_lost_callback()

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        packet = Mmdvm.from_bytes(data)
        if isinstance(packet.command_data, Mmdvm.TypeMasterNotAccept):
            if self.connection_status == self.CON_LOGIN_REQUEST_SENT:
                self.connection_status = self.CON_NEW
                self.log("Master did not accept our login request")
            elif self.connection_status == self.CON_LOGIN_RESPONSE_SENT:
                self.connection_status = self.CON_NEW
                self.log("Master did not accept our password challenge response")
        elif isinstance(packet.command_data, Mmdvm.TypeMasterRepeaterAck):
            if self.connection_status == self.CON_LOGIN_REQUEST_SENT:
                self.log("Sending Login Response")
                self.send_login_response(packet.command_data.repeater_id_or_challenge)
            elif self.connection_status == self.CON_LOGIN_RESPONSE_SENT:
                self.log("Master Login Accept")
                self.connection_status = self.CON_LOGIN_SUCCESSFULL
                self.send_configuration()
        elif isinstance(packet.command_data, Mmdvm.TypeMasterPong):
            # self.log("Master PONG received")
            pass
        elif isinstance(packet.command_data, Mmdvm.TypeMasterClosing):
            self.log("Master Closing connection")
            self.connection_status = self.CON_NEW
        elif isinstance(packet.command_data, Mmdvm.TypeDmrData):
            self.dmrd_received(data)
        else:
            self.log(f"UNHANDLED {packet.__class__.__name__} {hexlify(data)}")

    def dmrd_received(self, data: bytes):
        pass

    def send_login_request(self) -> None:
        self.log("Sending Login Request")
        self.connection_status = self.CON_LOGIN_REQUEST_SENT
        request = struct.pack(">4sI", b"RPTL", self.settings.hb_repeater_dmr_id)
        self.transport.sendto(request)

    def send_login_response(self, challenge: int):
        self.log("Sending Login Response (Challenge response)")
        self.connection_status = self.CON_LOGIN_RESPONSE_SENT
        challenge_response = struct.pack(
            ">4sI32s",
            b"RPTK",
            self.settings.hb_repeater_dmr_id,
            a2b_hex(
                sha256(
                    b"".join(
                        [
                            challenge.to_bytes(length=4, byteorder="big"),
                            self.settings.hb_password.encode(),
                        ]
                    )
                ).hexdigest()
            ),
        )
        self.transport.sendto(challenge_response)

    def send_configuration(self):
        self.log("Sending self configuration to master")
        packet = struct.pack(
            ">4sI8s9s9s2s2s8s9s3s20s19s1s124s40s40s",
            b"RPTC",
            self.settings.hb_repeater_dmr_id,
            self.settings.hb_callsign[0:8].ljust(8).encode(),
            self.settings.hb_rx_freq[0:9].rjust(9, "0").encode(),
            self.settings.hb_tx_freq[0:9].rjust(9, "0").encode(),
            str(self.settings.hb_tx_power & 0xFFFF).rjust(2, "0").encode(),
            str(self.settings.hb_color_code & 0xFFFF).rjust(2, "0").encode(),
            self.settings.hb_latitude[0:8].rjust(8, "0").encode(),
            self.settings.hb_longitude[0:9].rjust(9, "0").encode(),
            str(min(max(self.settings.hb_antenna_height, 0), 999))[0:3]
            .rjust(3, "0")
            .encode(),
            self.settings.hb_location[0:20].ljust(20).encode(),
            self.settings.hb_description[0:19].ljust(19).encode(),
            self.settings.hb_timeslots[0:1].encode(),
            self.settings.hb_url[0:124].ljust(124).encode(),
            self.settings.hb_software_id[0:40].ljust(40).encode(),
            self.settings.hb_package_id[0:40].ljust(40).encode(),
        )
        self.transport.sendto(packet)

    def send_ping(self):
        packet = struct.pack(">7sI", b"RPTPING", self.settings.hb_repeater_dmr_id)
        self.transport.sendto(packet)

    def send_closing(self):
        self.log("Closing MMDVM connection")
        packet = struct.pack(">5sI", b"RPTCL", self.settings.hb_repeater_dmr_id)
        self.transport.sendto(packet)

    def disconnect(self):
        if self.transport and not self.transport.is_closing():
            self.send_closing()
