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
        self.mmdvm_last_sequence: int = 0
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
                    IpSiteConnectProtocol.SlotTypes.slot_type_data_c,
                    IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header,
                    IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc,
                ):
                    bitflags[2] = 1

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

            print(
                f"MMDVM data-type:{packet.command_data.data_type} "
                f"slot-no:{packet.command_data.slot_no} "
                f"frame-type:{packet.command_data.frame_type} "
                f"call-type:{packet.command_data.call_type}"
                f"stream-no:{packet.command_data.stream_id}"
            )

            data_string = b""

            out = unhexlify(data_string)
            await self.queue_hytera_output.put(out)
            self.queue_mmdvm_to_translate.task_done()
