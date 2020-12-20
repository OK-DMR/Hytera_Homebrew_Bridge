#!/usr/bin/env python3
import asyncio
from asyncio import Queue
from binascii import unhexlify

from bitarray import bitarray
from kaitaistruct import KaitaiStruct

from hytera_homebrew_bridge.kaitai.ip_site_connect_heartbeat import (
    IpSiteConnectHeartbeat,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.lib import settings as module_settings
from hytera_homebrew_bridge.lib.utils import byteswap_bytes


class HyteraMmdvmTranslator:
    def __init__(
        self,
        settings: module_settings.BridgeSettings,
        hytera_incoming: Queue,
        hytera_outgoing: Queue,
        mmdvm_incoming: Queue,
        mmdvm_outgoing: Queue,
    ):
        self.settings = settings
        self.queue_hytera_to_translate = hytera_incoming
        self.queue_hytera_output = hytera_outgoing
        self.queue_mmdvm_to_translate = mmdvm_incoming
        self.queue_mmdvm_output = mmdvm_outgoing
        # translation / state-machine related variables
        self.hytera_last_sequence: int = 0
        self.mmdvm_last_sequence: int = 0

    async def translate_from_hytera(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            packet: KaitaiStruct = await self.queue_hytera_to_translate.get()
            if isinstance(packet, IpSiteConnectHeartbeat):
                continue
            if isinstance(packet, IpSiteConnectProtocol):
                bitflags = bitarray(
                    [
                        # 0 => TS1, 1 => TS2
                        packet.timeslot_raw
                        == IpSiteConnectProtocol.Timeslots.timeslot_2,
                        # 0 => group call, 1 => private call
                        packet.call_type
                        == IpSiteConnectProtocol.CallTypes.private_call,
                        # 2b = frame type
                        0,
                        0,
                        # 4b = data type / voice seq
                    ]
                )
                # frame type
                if packet.slot_type in (
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_a,
                ):
                    bitflags[2] = 1
                # data type
                map = {
                    0xBBBB: "0000",
                    0xCCCC: "0001",
                    0x7777: "0010",
                    0x8888: "0011",
                    0x9999: "0100",
                    0xAAAA: "0101",
                }
                bitflags.extend(map.get(packet.slot_type) or "0000")
                self.hytera_last_sequence += 1

                out = (
                    b"DMRD"
                    + int(self.hytera_last_sequence % 0xFF).to_bytes(1, byteorder="big")
                    + packet.source_radio_id.to_bytes(3, byteorder="big")
                    + packet.destination_radio_id.to_bytes(3, byteorder="big")
                    + self.settings.get_repeater_dmrid().to_bytes(4, byteorder="big")
                    + bitflags.tobytes()
                    + bytes([0x00, 0x00, 0x00, 0x10])
                    + byteswap_bytes(packet.ipsc_payload)
                )
                await self.queue_mmdvm_output.put(out)

    async def translate_from_mmdvm(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            packet: Mmdvm = await self.queue_mmdvm_to_translate.get()
            if not isinstance(packet.command_data, Mmdvm.TypeDmrData):
                continue

            out = unhexlify(
                "0501"
                + ("01" if packet.command_data.slot_no else "00")
                + ("2222" if packet.command_data.slot_no else "1111")
                + (packet.command_data.data_type)
                + "1111"
                + "406302"
                + "01"
                + packet.command_data.target_id,
                packet.command_data.source_id,
                byteswap_bytes(packet.command_data.dmr_data),
            )
