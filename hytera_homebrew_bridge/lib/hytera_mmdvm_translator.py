#!/usr/bin/env python3
import asyncio
from asyncio import Queue, CancelledError
from typing import Optional

from kaitaistruct import KaitaiStruct
from okdmr.kaitai.homebrew.mmdvm2020 import Mmdvm2020
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol

from hytera_homebrew_bridge.dmrlib.mmdvm_utils import (
    get_mmdvm_bitflags,
    get_ipsc_frame_type,
    get_ipsc_slot_type,
)
from hytera_homebrew_bridge.dmrlib.terminal import BurstInfo
from hytera_homebrew_bridge.dmrlib.transmission_watcher import TransmissionWatcher
from hytera_homebrew_bridge.lib.logging_trait import LoggingTrait
from hytera_homebrew_bridge.lib.settings import BridgeSettings
from hytera_homebrew_bridge.lib.utils import byteswap_bytes, assemble_hytera_ipsc_packet
from hytera_homebrew_bridge.tests.prettyprint import prettyprint


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

    async def translate_from_hytera(self):
        loop = asyncio.get_running_loop()
        while loop.is_running():
            try:
                packet: KaitaiStruct = await self.queue_hytera_to_translate.get()
                if not isinstance(packet, IpSiteConnectProtocol):
                    continue
                elif isinstance(packet, IpSiteConnectProtocol) and packet.slot_type in [
                    IpSiteConnectProtocol.SlotTypes.slot_type_wakeup_request,
                    IpSiteConnectProtocol.SlotTypes.slot_type_sync,
                ]:
                    print(
                        "Slot Type", packet.slot_type, "Frame Type", packet.frame_type
                    )
                    burst: BurstInfo = BurstInfo(
                        data=byteswap_bytes(packet.ipsc_payload)
                    )
                    burst.debug()
                    continue

                burst: Optional[BurstInfo] = self.transmission_watcher.process_packet(
                    packet, do_debug=False
                )
                if burst:
                    burst.debug()
                    mmdvm_out = (
                        b"DMRD"
                        + burst.sequence_no.to_bytes(1, byteorder="big")
                        + packet.source_radio_id.to_bytes(3, byteorder="big")
                        + packet.destination_radio_id.to_bytes(3, byteorder="big")
                        + self.settings.get_repeater_dmrid().to_bytes(
                            4, byteorder="big"
                        )
                        + get_mmdvm_bitflags(burst, packet)
                        + burst.stream_no[:4]
                        # ipsc payload is 34 bytes (little endian), expected mmdvm payload is 33 bytes (big endian)
                        + byteswap_bytes(packet.ipsc_payload)[0:-1]
                    )

                    await self.queue_mmdvm_output.put(mmdvm_out)
                else:
                    print(
                        "Hytera BurstInfo not available",
                        type(burst),
                        "packet",
                        type(packet),
                        packet.__class__.__name__,
                        prettyprint(packet),
                    )
            except CancelledError:
                return
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
                packet: Mmdvm2020 = await self.queue_mmdvm_to_translate.get()
                if not isinstance(packet.command_data, Mmdvm2020.TypeDmrData):
                    continue

                burst: Optional[BurstInfo] = self.transmission_watcher.process_packet(
                    packet, do_debug=False
                )
                if burst:
                    burst.debug()

                    hytera_out_packet: bytes = assemble_hytera_ipsc_packet(
                        timeslot_is_ts1=(packet.command_data.slot_no == 0),
                        is_private_call=(packet.command_data.call_type == 1),
                        target_id=packet.command_data.target_id,
                        source_id=packet.command_data.source_id,
                        color_code=self.settings.hb_color_code,
                        sequence_number=burst.sequence_no,
                        dmr_payload=byteswap_bytes(packet.command_data.dmr_data),
                        frame_type=get_ipsc_frame_type(burst),
                        hytera_slot_type=get_ipsc_slot_type(burst),
                    )
                    await self.queue_hytera_output.put(hytera_out_packet)
                else:
                    print(
                        f"MMDVM BurstInfo not available",
                        type(burst),
                        "packet",
                        type(packet),
                    )
            except CancelledError:
                return
            except RuntimeError as e:
                self.log_error("MMDVM->HHB Could not get MMDVM packet from queue")
                self.log_exception(e)
                continue
            except BaseException as e:
                self.log_error("MMDVM->HHB unhandled exception")
                self.log_exception(e)
                continue

            # Notify queue about finished task
            self.queue_mmdvm_to_translate.task_done()
