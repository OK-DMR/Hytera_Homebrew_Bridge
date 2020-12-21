#!/usr/bin/env python3
import asyncio
from asyncio import Queue

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
        self.mmdvm_last_sequence: int = 0
        self.mmdvm_sequence_number: int = 0
        self.hytera_last_sequence_out: int = 0
        self.hytera_last_sequence_in: int = -1
        self.hytera_last_started_stream_id_out: int = -1
        self.hytera_stream_id: int = 0
        self.hytera_to_mmdvm_datatype: dict = {
            IpSiteConnectProtocol.SlotTypes.slot_type_data_a: "0100",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_b: "0101",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_c: "0000",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_d: "0001",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_e: "0010",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_f: "0011",
            IpSiteConnectProtocol.SlotTypes.slot_type_ipsc_sync: "0011",
            IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header: "0001",
            IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc: "0010",
        }
        self.mmdvm_to_hytera_slottype: dict = {
            4: IpSiteConnectProtocol.SlotTypes.slot_type_data_a,
            5: IpSiteConnectProtocol.SlotTypes.slot_type_data_b,
            0: IpSiteConnectProtocol.SlotTypes.slot_type_data_c,
            1: IpSiteConnectProtocol.SlotTypes.slot_type_data_d,
            2: IpSiteConnectProtocol.SlotTypes.slot_type_data_e,
            3: IpSiteConnectProtocol.SlotTypes.slot_type_data_f,
        }
        self.mmdvm_to_hytera_slottype_str: dict = {
            IpSiteConnectProtocol.SlotTypes.slot_type_data_a: b"\xBB\xBB",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_b: b"\xCC\xCC",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_c: b"\x77\x77",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_d: b"\x88\x88",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_e: b"\x99\x99",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_f: b"\xAA\xAA",
            IpSiteConnectProtocol.SlotTypes.slot_type_ipsc_sync: b"\xEE\xEE",
            IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header: b"\x11\x11",
            IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc: b"\x22\x22",
            IpSiteConnectProtocol.SlotTypes.slot_type_csbk: b"\x33\x33",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_header: b"\x44\x44",
            IpSiteConnectProtocol.SlotTypes.slot_type_rate_12_data: b"\x55\x55",
            IpSiteConnectProtocol.SlotTypes.slot_type_rate_34_data: b"\x66\x66",
            IpSiteConnectProtocol.SlotTypes.slot_type_unknown: b"\x00\x00",
        }

    async def translate_from_hytera(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            try:
                packet: KaitaiStruct = await self.queue_hytera_to_translate.get()
            except RuntimeError:
                continue

            if isinstance(packet, IpSiteConnectHeartbeat):
                continue
            if isinstance(packet, IpSiteConnectProtocol):
                if (
                    packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_ipsc_sync
                ):
                    continue

                if self.hytera_last_sequence_in == packet.sequence_number:
                    # do not send duplicate packets
                    continue
                else:
                    self.hytera_last_sequence_in = packet.sequence_number

                if (
                    packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header
                ):
                    if self.hytera_last_started_stream_id_out == self.hytera_stream_id:
                        # do not send duplicate start call headers
                        continue
                    else:
                        self.hytera_last_started_stream_id_out = self.hytera_stream_id

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
                        # 4b = data type / voice seq => extended below
                    ]
                )
                # data type
                bitflags.extend(
                    self.hytera_to_mmdvm_datatype.get(packet.slot_type) or "0000"
                )

                # frame type
                if packet.slot_type in (
                    IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header,
                    IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc,
                ):
                    bitflags[2] = 1
                elif (
                    packet.slot_type == IpSiteConnectProtocol.SlotTypes.slot_type_data_c
                ):
                    bitflags[3] = 1

                self.hytera_last_sequence_out = (
                    self.hytera_last_sequence_out + 1
                ) & 0xFF

                await self.queue_mmdvm_output.put(
                    b"DMRD"
                    + int(self.hytera_last_sequence_out).to_bytes(1, byteorder="big")
                    + packet.source_radio_id.to_bytes(3, byteorder="big")
                    + packet.destination_radio_id.to_bytes(3, byteorder="big")
                    + self.settings.get_repeater_dmrid().to_bytes(4, byteorder="big")
                    + bitflags.tobytes()
                    + self.hytera_stream_id.to_bytes(4, byteorder="big")
                    + byteswap_bytes(packet.ipsc_payload)
                )

                # Every time transmission is terminated, increment stream id
                if (
                    packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc
                ):
                    self.hytera_stream_id += 1
                    self.hytera_last_sequence_out = 0

                # Notify queue about finished task
                self.queue_hytera_to_translate.task_done()

    async def translate_from_mmdvm(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            try:
                packet: Mmdvm = await self.queue_mmdvm_to_translate.get()
            except RuntimeError:
                continue

            if not isinstance(packet.command_data, Mmdvm.TypeDmrData):
                continue

            self.mmdvm_sequence_number = (self.mmdvm_sequence_number + 1) & 0xFF

            slot_type: bytes
            if packet.command_data.frame_type == 2:
                if packet.command_data.data_type == 1:
                    # voice lc header
                    slot_type = b"\x11\x11"
                    self.mmdvm_sequence_number = 0
                else:
                    # terminator with lc
                    slot_type = b"\x22\x22"
            else:
                slot_type = self.mmdvm_to_hytera_slottype.get(
                    packet.command_data.data_type
                )

            swapped_bytes: bytes = byteswap_bytes(packet.command_data.dmr_data)

            data_string: bytes = (
                # source port
                self.settings.dmr_port.to_bytes(2, byteorder="little")
                +
                # magic fixed header
                b"\x00\x50"
                +
                # sequence_number
                self.mmdvm_sequence_number.to_bytes(1, byteorder="little")
                +
                # reserved_3
                b"\xE0\x00\x00"
                +
                # packet type
                b"\x01"
                +
                # reserved_7a
                b"\x00\x05\x01"
                + (b"\x02" if packet.command_data.slot_no == 1 else b"\x01")
                + b"\x00\x00\x00"
                +
                # timeslot_raw
                (b"\x22\x22" if packet.command_data.slot_no == 1 else b"\x11\x11")
                +
                # slot_type
                self.mmdvm_to_hytera_slottype_str.get(slot_type, b"\x00\x00")
                +
                # delimiter
                b"\x11\x11"
                +
                # frame_type
                b"\xBB\xBB"
                +
                # reserved_2a
                b"\x40\x5C"
                +
                # payload data
                swapped_bytes
                +
                # two byte crc16 checksum
                b"\x00\x00"
                # reserved_2b
                b"\x63\x02"
                +
                # call_type, mmdvm true = private, ipsc 00 = private
                (b"\x11" if packet.command_data.call_type else b"\x00")
                +
                # destination id
                int(packet.command_data.target_id).to_bytes(4, byteorder="little")
                +
                # source id
                max(int(packet.command_data.source_id), 4294967295).to_bytes(
                    4, byteorder="little"
                )
                +
                # reserved_1b
                b"\x00"
            )

            await self.queue_hytera_output.put(data_string)
            self.queue_mmdvm_to_translate.task_done()
