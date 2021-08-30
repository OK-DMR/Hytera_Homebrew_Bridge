#!/usr/bin/env python3
import asyncio
from asyncio import Queue
from typing import Optional

from kaitaistruct import KaitaiStruct

from hytera_homebrew_bridge.dmrlib.mmdvm_utils import get_mmdvm_bitflags
from hytera_homebrew_bridge.dmrlib.terminal import BurstInfo
from hytera_homebrew_bridge.dmrlib.transmission_watcher import TransmissionWatcher
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.lib.logging_trait import LoggingTrait
from hytera_homebrew_bridge.lib.settings import BridgeSettings
from hytera_homebrew_bridge.lib.utils import byteswap_bytes


class HyteraMmdvmTranslator(LoggingTrait):
    def __init__(
        self,
        settings: BridgeSettings,
        hytera_incoming: Queue,
        hytera_outgoing: Queue,
        mmdvm_incoming: Queue,
        mmdvm_outgoing: Queue,
    ):
        self.transmission_watcher: TransmissionWatcher = TransmissionWatcher()
        self.settings = settings
        self.queue_hytera_to_translate = hytera_incoming
        self.queue_hytera_output = hytera_outgoing
        self.queue_mmdvm_to_translate = mmdvm_incoming
        self.queue_mmdvm_output = mmdvm_outgoing
        self.mmdvm_sequence_out = 0

    def get_mmdvm_sequence(self, increment: bool = True):
        if increment:
            self.mmdvm_sequence_out = (self.mmdvm_sequence_out + 1) & 255
        return self.mmdvm_sequence_out

    async def translate_from_hytera(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            try:
                packet: KaitaiStruct = await self.queue_hytera_to_translate.get()
                if not isinstance(
                    packet, IpSiteConnectProtocol
                ) or packet.slot_type in [
                    IpSiteConnectProtocol.SlotTypes.slot_type_wakeup_request,
                    IpSiteConnectProtocol.SlotTypes.slot_type_sync,
                ]:
                    continue

                burst: Optional[BurstInfo] = self.transmission_watcher.process_packet(
                    packet, do_debug=False
                )
                if burst:
                    mmdvm_out = (
                        b"DMRD"
                        + self.get_mmdvm_sequence().to_bytes(1, byteorder="big")
                        + packet.source_radio_id.to_bytes(3, byteorder="big")
                        + packet.destination_radio_id.to_bytes(3, byteorder="big")
                        + self.settings.get_repeater_dmrid().to_bytes(
                            4, byteorder="big"
                        )
                        + get_mmdvm_bitflags(burst, packet)
                        + b"\x00\x00\x00\x01"  # timeslot_info.mmdvm_stream_id[0:4]
                        + byteswap_bytes(packet.ipsc_payload)
                    )

                    await self.queue_mmdvm_output.put(mmdvm_out)
                else:
                    print(
                        "burst",
                        type(burst),
                        "packet",
                        type(packet),
                        packet.__class__.__name__,
                    )
            except RuntimeError as e:
                self.log_error("HYTER->HHB Could not get Hytera packet from queue")
                self.log_exception(e)
                continue
            except BaseException as e:
                self.log_error("HYTER->HHB unhandled exception")
                self.log_exception(e)
                continue

            # Notify queue about finished task
            self.queue_hytera_to_translate.task_done()

    async def translate_from_mmdvm(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            try:
                packet: Mmdvm = await self.queue_mmdvm_to_translate.get()
            except RuntimeError as e:
                self.log_error("MMDVM->HHB Could not get MMDVM packet from queue")
                self.log_exception(e)
                continue
            except BaseException as e:
                self.log_error("MMDVM->HHB unhandled exception")
                self.log_exception(e)
                continue

            burst: Optional[BurstInfo] = self.transmission_watcher.process_packet(
                packet, do_debug=False
            )
            if burst:
                print("translate from mmdvm")
                burst.debug()

            # hytera_ipsc_packet: bytes = assemble_hytera_ipsc_sync_packet(
            #     timeslot_is_ts1=(packet.command_data.slot_no == 0),
            #     is_private_call=(packet.command_data.call_type == 1),
            #     target_id=packet.command_data.target_id,
            #     source_id=packet.command_data.source_id,
            #     color_code=self.settings.hb_color_code,
            #     sequence_number=timeslot_info.hytera_last_sequence_out,
            # )
            # await self.queue_hytera_output.put(hytera_ipsc_packet)

            self.queue_mmdvm_to_translate.task_done()
