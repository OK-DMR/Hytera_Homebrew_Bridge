#!/usr/bin/env python3
import asyncio
from asyncio import Queue
from binascii import unhexlify, hexlify

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
        self.hytera_stream_id: int = 0

    async def translate_from_hytera(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            packet: KaitaiStruct = await self.queue_hytera_to_translate.get()
            if isinstance(packet, IpSiteConnectHeartbeat):
                continue
            if isinstance(packet, IpSiteConnectProtocol):
                print(
                    f"HYT incoming seq:{packet.sequence_number} "
                    f"slot-type: {packet.slot_type} "
                    f"frame-type: {packet.frame_type} "
                    f"call-type: {packet.call_type} "
                )

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
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_c,
                    IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header,
                ):
                    bitflags[2] = 1
                # data type
                map = {
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_a: "0100",
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_b: "0101",
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_c: "0000",
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_d: "0001",
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_e: "0010",
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_f: "0011",
                    IpSiteConnectProtocol.SlotTypes.slot_type_ipsc_sync: "0100",
                    IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header: "0001",
                    IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc: "0010",
                }
                bitflags.extend(map.get(packet.slot_type) or "0000")
                print(
                    f"bitflags {bitflags} slot-type {repr(packet.slot_type)} sequence {self.hytera_last_sequence}"
                )
                self.hytera_last_sequence = (self.hytera_last_sequence + 1) & 0xFF

                if (
                    packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header
                    or packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc
                ):
                    self.hytera_stream_id += 1

                print(f"settings repeater id: {self.settings.get_repeater_dmrid()}")

                out = (
                    b"DMRD"
                    + int(self.hytera_last_sequence).to_bytes(1, byteorder="big")
                    + packet.source_radio_id.to_bytes(3, byteorder="big")
                    + packet.destination_radio_id.to_bytes(3, byteorder="big")
                    + self.settings.get_repeater_dmrid().to_bytes(4, byteorder="big")
                    + bitflags.tobytes()
                    + self.hytera_stream_id.to_bytes(4, byteorder="big")
                    + byteswap_bytes(packet.ipsc_payload)
                )
                await self.queue_mmdvm_output.put(out)

    async def translate_from_mmdvm(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            packet: Mmdvm = await self.queue_mmdvm_to_translate.get()
            if not isinstance(packet.command_data, Mmdvm.TypeDmrData):
                continue

            print(
                f"MMDVM data-type:{packet.command_data.data_type} "
                f"slot-no:{packet.command_data.slot_no} "
                f"frame-type:{packet.command_data.frame_type} "
                f"call-type:{packet.command_data.call_type}"
                f"stream-no:{packet.command_data.stream_id}"
            )

            data_string = (
                "0501"
                + ("01" if packet.command_data.slot_no else "00")
                + ("2222" if packet.command_data.slot_no else "1111")
                + str(
                    hexlify(
                        packet.command_data.data_type.to_bytes(1, byteorder="little")
                    ),
                    "utf8",
                )
                + "1111"
                + "406302"
                + "01"
                + str(
                    hexlify(
                        packet.command_data.target_id.to_bytes(3, byteorder="little")
                    ),
                    "utf8",
                )
                + str(
                    hexlify(
                        packet.command_data.source_id.to_bytes(3, byteorder="little")
                    ),
                    "utf8",
                )
                + str(hexlify(byteswap_bytes(packet.command_data.dmr_data)), "utf8")
            )

            out = unhexlify(data_string)

            # await self.queue_hytera_output.put(out)
