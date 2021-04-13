#!/usr/bin/env python3
from asyncio import Queue
from time import time

import asyncio
from bitarray import bitarray
from kaitaistruct import KaitaiStruct

from hytera_homebrew_bridge.kaitai.ip_site_connect_heartbeat import (
    IpSiteConnectHeartbeat,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.lib import settings as module_settings
from hytera_homebrew_bridge.lib.logging_trait import LoggingTrait
from hytera_homebrew_bridge.lib.utils import (
    byteswap_bytes,
    assemble_hytera_ipsc_packet,
    assemble_hytera_ipsc_wakeup_packet,
    assemble_hytera_ipsc_sync_packet,
)


class TimeslotInfo(LoggingTrait):
    def __init__(self, timeslot: int):
        self.timeslot: int = timeslot
        self.seq_no_hytera_in: int = 0
        self.seq_no_hytera_out: int = 0
        self.seq_no_mmdvm_in: int = 0
        self.seq_no_mmdvm_out: int = 0


class HyteraMmdvmTranslator(LoggingTrait):
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
        self.hytera_last_sent_timestamp: int = 0
        self.hytera_last_sequence_out: int = 0
        self.hytera_last_sequence_in: int = -1
        self.hytera_last_started_stream_id_out: int = -1
        self.hytera_stream_id: int = 0
        # 9.3.6 Data Type of ETSI TS 102 361-1 V2.5.1
        self.hytera_to_mmdvm_datatype: dict = {
            # for voice frames
            IpSiteConnectProtocol.SlotTypes.slot_type_data_a: "0100",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_b: "0101",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_c: "0000",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_d: "0001",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_e: "0010",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_f: "0011",
            IpSiteConnectProtocol.SlotTypes.slot_type_sync: "0011",
            # for data frames
            IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header: "0001",
            IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc: "0010",
            IpSiteConnectProtocol.SlotTypes.slot_type_csbk: "0011",
            # 4,5 are MBC Header/Continuation, not known in hytera yet
            IpSiteConnectProtocol.SlotTypes.slot_type_data_header: "0110",
            IpSiteConnectProtocol.SlotTypes.slot_type_rate_12_data: "0111",
            IpSiteConnectProtocol.SlotTypes.slot_type_rate_34_data: "1000",
            # idle, rate 1 data, unified single block data, not known in hytera yet
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
            IpSiteConnectProtocol.SlotTypes.slot_type_sync: b"\xEE\xEE",
            IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header: b"\x11\x11",
            IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc: b"\x22\x22",
            IpSiteConnectProtocol.SlotTypes.slot_type_csbk: b"\x33\x33",
            IpSiteConnectProtocol.SlotTypes.slot_type_data_header: b"\x44\x44",
            IpSiteConnectProtocol.SlotTypes.slot_type_rate_12_data: b"\x55\x55",
            IpSiteConnectProtocol.SlotTypes.slot_type_rate_34_data: b"\x66\x66",
            IpSiteConnectProtocol.SlotTypes.slot_type_unknown: b"\x00\x00",
        }

    def up_mmdvm_sequence_number(self):
        self.mmdvm_sequence_number = (self.mmdvm_sequence_number + 1) & 0xFF

    async def translate_from_hytera(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            try:
                packet: KaitaiStruct = await self.queue_hytera_to_translate.get()
            except RuntimeError as e:
                self.log_error("HYTERA->MMDVM Could not get Hytera packet from queue")
                self.log_exception(e)
                continue

            if isinstance(packet, IpSiteConnectHeartbeat):
                self.log_debug("HYTERA->MMDVM Received IPSC Heartbeat, not translating")
                continue

            if isinstance(packet, IpSiteConnectProtocol):
                if packet.slot_type == IpSiteConnectProtocol.SlotTypes.slot_type_sync:
                    # self.log_debug(
                    #    "HYTERA->MMDVM Received IPSC Sync packet, not translating"
                    # )
                    continue
                if (
                    packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_wakeup_request
                ):
                    self.log_debug(
                        "HYTERA->MMDVM Received IPSC Wakeup packet, not translating"
                    )
                    continue

                if self.hytera_last_sequence_in == packet.sequence_number:
                    # do not send duplicate packets
                    self.log_debug(
                        f"HYTERA->MMDVM Got duplicate IPSC packet {packet.slot_type}, not translating"
                    )
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
                        self.log_info(
                            "HYTERA->MMDVM *%s CALL START* FROM: %s TO: %s TS: %s"
                            % (
                                "PRIVATE"
                                if packet.call_type
                                == IpSiteConnectProtocol.CallTypes.private_call
                                else "GROUP",
                                packet.source_radio_id,
                                packet.destination_radio_id,
                                # timeslot
                                "1"
                                if packet.timeslot_raw
                                == IpSiteConnectProtocol.Timeslots.timeslot_1
                                else "2",
                            )
                        )
                        self.hytera_last_started_stream_id_out = self.hytera_stream_id
                if (
                    packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc
                ):
                    self.log_info(
                        "HYTERA->MMDVM *%s CALL  END * FROM: %s TO: %s TS: %s"
                        % (
                            "PRIVATE"
                            if packet.call_type
                            == IpSiteConnectProtocol.CallTypes.private_call
                            else "GROUP",
                            packet.source_radio_id,
                            packet.destination_radio_id,
                            # timeslot
                            "1"
                            if packet.timeslot_raw
                            == IpSiteConnectProtocol.Timeslots.timeslot_1
                            else "2",
                        )
                    )

                bitflags = bitarray(
                    [
                        # 0 => TS1, 1 => TS2
                        packet.timeslot_raw
                        == IpSiteConnectProtocol.Timeslots.timeslot_2,
                        # 0 => group call, 1 => private call
                        packet.call_type
                        == IpSiteConnectProtocol.CallTypes.private_call,
                        # 2b = frame type => extended below
                        # 4b = data type / voice seq => extended below
                    ]
                )
                # frame type
                if (
                    packet.frame_type
                    == IpSiteConnectProtocol.FrameTypes.frame_type_voice_sync
                ):
                    bitflags.extend("01")
                elif (
                    packet.frame_type
                    == IpSiteConnectProtocol.FrameTypes.frame_type_data_sync_or_csbk
                    or packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_rate_34_data
                    or packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_rate_12_data
                    or packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_data_header
                    or packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_csbk
                    or packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header
                    or packet.slot_type
                    == IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc
                ):
                    bitflags.extend("10")
                else:
                    bitflags.extend("00")
                # data type
                bitflags.extend(
                    self.hytera_to_mmdvm_datatype.get(packet.slot_type) or "0000"
                )

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

                # Update last timestamp, because receiving from Hytera means it's already woken up
                self.hytera_last_sent_timestamp = time()
                # Notify queue about finished task
                self.queue_hytera_to_translate.task_done()

    async def translate_from_mmdvm(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            try:
                packet: Mmdvm = await self.queue_mmdvm_to_translate.get()
            except RuntimeError as e:
                self.log_error("MMDVM->HYTERA Could not get MMDVM packet from queue")
                self.log_exception(e)
                continue

            if not isinstance(packet.command_data, Mmdvm.TypeDmrData):
                self.log_info(
                    f"MMDVM->HYTERA Received packet not DMRD, not translating {packet.command_data.__class__.__name__}"
                )
                continue

            self.log_debug(
                f"MMDVM->HYTERA Timeslot {packet.command_data.slot_no} CallType {packet.command_data.call_type} "
                f"FrameType {packet.command_data.frame_type} DataType {packet.command_data.data_type}"
            )

            self.up_mmdvm_sequence_number()

            swapped_bytes: bytes = byteswap_bytes(packet.command_data.dmr_data)

            slot_type: IpSiteConnectProtocol.SlotTypes
            if packet.command_data.frame_type == 2:
                if packet.command_data.data_type == 1:
                    # voice lc header
                    slot_type = (
                        IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header
                    )
                    self.mmdvm_sequence_number = 0
                    self.log_info(
                        "MMDVM->HYTERA *%s CALL START* FROM: %s TO: %s TS: %s"
                        % (
                            "PRIVATE"
                            if packet.command_data.call_type == 1
                            else "GROUP",
                            packet.command_data.source_id,
                            packet.command_data.target_id,
                            "2" if packet.command_data.slot_no == 1 else "1",
                        )
                    )
                    if self.hytera_last_sent_timestamp < (time() - 5):
                        self.log_info("Waking up repeater, both timeslots")
                        for TS in (True, False):
                            # send wakeup packet
                            hytera_ipsc_packet: bytes = (
                                assemble_hytera_ipsc_wakeup_packet(
                                    timeslot_is_ts1=TS,
                                    target_id=packet.command_data.target_id,
                                    source_id=packet.command_data.source_id,
                                    color_code=self.settings.hb_color_code,
                                )
                            )
                            await self.queue_hytera_output.put(hytera_ipsc_packet)
                            # wait roughly 400ms after waking up the repeater
                            await asyncio.sleep(0.4)
                else:
                    # terminator with lc
                    slot_type = (
                        IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc
                    )
                    self.log_info(
                        "MMDVM->HYTERA *%s CALL  END * FROM: %s TO: %s TS: %s"
                        % (
                            "PRIVATE"
                            if packet.command_data.call_type == 1
                            else "GROUP",
                            packet.command_data.source_id,
                            packet.command_data.target_id,
                            "2" if packet.command_data.slot_no == 1 else "1",
                        )
                    )
            else:
                slot_type = self.mmdvm_to_hytera_slottype.get(
                    packet.command_data.data_type
                )

            hytera_ipsc_packet: bytes = assemble_hytera_ipsc_packet(
                udp_port=self.settings.dmr_port,
                sequence_number=self.mmdvm_sequence_number,
                timeslot_is_ts1=(packet.command_data.slot_no == 0),
                hytera_slot_type=int(slot_type.__getattribute__("value")),
                dmr_payload=swapped_bytes,
                is_private_call=(packet.command_data.call_type == 1),
                target_id=packet.command_data.target_id,
                source_id=packet.command_data.source_id,
                color_code=self.settings.hb_color_code,
            )

            await self.queue_hytera_output.put(hytera_ipsc_packet)
            if slot_type == IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header:
                self.up_mmdvm_sequence_number()
                await self.queue_hytera_output.put(
                    b"\x5a\x5a\x5a\x5a"
                    + self.mmdvm_sequence_number.to_bytes(1, byteorder="little")
                    + hytera_ipsc_packet[5:]
                )
                self.up_mmdvm_sequence_number()
                await self.queue_hytera_output.put(
                    b"\x5a\x5a\x5a\x5a"
                    + self.mmdvm_sequence_number.to_bytes(1, byteorder="little")
                    + hytera_ipsc_packet[5:]
                )

            if slot_type == IpSiteConnectProtocol.SlotTypes.slot_type_data_f:
                self.up_mmdvm_sequence_number()
                # send sync packet
                hytera_ipsc_packet: bytes = assemble_hytera_ipsc_sync_packet(
                    timeslot_is_ts1=(packet.command_data.slot_no == 0),
                    is_private_call=(packet.command_data.call_type == 1),
                    target_id=packet.command_data.target_id,
                    source_id=packet.command_data.source_id,
                    color_code=self.settings.hb_color_code,
                    sequence_number=self.mmdvm_sequence_number,
                )
                #  self.log_info(f"Sending ipsc sync to repeater {hytera_ipsc_packet.hex()}")
                await self.queue_hytera_output.put(hytera_ipsc_packet)

            self.hytera_last_sent_timestamp = time()
            self.queue_mmdvm_to_translate.task_done()
