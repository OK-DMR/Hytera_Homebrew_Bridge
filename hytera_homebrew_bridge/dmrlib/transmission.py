import secrets
import traceback
from typing import List, Optional, Union

from kaitaistruct import KaitaiStruct
from kamene.layers.inet import IP
from okdmr.dmrlib.etsi.fec.trellis import Trellis34
from okdmr.kaitai.etsi.dmr_csbk import DmrCsbk
from okdmr.kaitai.etsi.dmr_data import DmrData
from okdmr.kaitai.etsi.dmr_data_header import DmrDataHeader
from okdmr.kaitai.etsi.dmr_ip_udp import DmrIpUdp
from okdmr.kaitai.etsi.full_link_control import FullLinkControl

from hytera_homebrew_bridge.dmrlib.burst_info import BurstInfo
from hytera_homebrew_bridge.dmrlib.data_type import DataType
from hytera_homebrew_bridge.dmrlib.decode import decode_complete_lc
from hytera_homebrew_bridge.dmrlib.transmission_type import TransmissionType
from hytera_homebrew_bridge.tests.prettyprint import prettyprint


class TransmissionObserverInterface:
    def transmission_started(self, transmission_type: TransmissionType):
        """
        Get notified about new transmission (data or voice) being started with voice/data header

        @param transmission_type:
        @return:
        """
        pass

    def data_transmission_ended(
        self, transmission_header: DmrDataHeader, blocks: List[KaitaiStruct]
    ):
        """
        Get notified about completed (or ended) data transmission and get all blocks that made up that transmission,
        including CSBKs and all the raw DMR packets

        @param transmission_header:
        @param blocks:
        @return:
        """
        pass

    def voice_transmission_ended(
        self, voice_header: FullLinkControl, blocks: List[KaitaiStruct]
    ):
        """
        Get notified about ended voice transmission
        @param voice_header:
        @param blocks:
        @return:
        """
        pass


class Transmission:
    def __init__(self, observer: TransmissionObserverInterface = None):
        self.type = TransmissionType.Idle
        self.blocks_expected: int = 0
        self.blocks_received: int = 0
        self.last_burst_data_type: DataType = DataType.UnknownDataType
        self.confirmed: bool = False
        self.finished: bool = False
        self.blocks: List[KaitaiStruct] = list()
        self.header: Optional[KaitaiStruct] = None
        self.stream_no: bytes = secrets.token_bytes(4)
        self.observers: List[TransmissionObserverInterface] = (
            [] if observer is None else [observer]
        )

    def add_transmission_observer(self, observer: TransmissionObserverInterface):
        self.observers.append(observer)

    def new_transmission(self, newtype: TransmissionType):
        if (
            newtype != TransmissionType.Idle
            and self.type == TransmissionType.DataTransmission
        ):
            print("New Transmission when old was not yet finished")
            self.end_data_transmission()
        self.type = newtype
        self.blocks_expected = 0
        self.blocks_received = 0
        self.confirmed = False
        self.finished = False
        self.blocks = list()
        self.header = None
        self.stream_no = secrets.token_bytes(4)

    def process_voice_header(self, voice_header: FullLinkControl):
        self.new_transmission(TransmissionType.VoiceTransmission)
        self.header = voice_header

        # header + terminator
        self.blocks_expected += 2
        self.blocks_received += 1

    def process_data_header(self, data_header: DmrDataHeader):
        if not self.type == TransmissionType.DataTransmission:
            self.new_transmission(TransmissionType.DataTransmission)
        if hasattr(data_header.data, "blocks_to_follow"):
            if self.blocks_expected == 0:
                self.blocks_expected = data_header.data.blocks_to_follow + 1
            elif self.blocks_expected != (
                self.blocks_received + data_header.data.blocks_to_follow + 1
            ):
                print(
                    f"[Blocks To Follow] Header block count mismatch {self.blocks_expected}-{self.blocks_received} != {data_header.data.blocks_to_follow}"
                )
        elif hasattr(data_header.data, "appended_blocks"):
            if self.blocks_expected == 0:
                self.blocks_expected = data_header.data.appended_blocks + 1
            elif self.blocks_expected != (
                self.blocks_expected + data_header.data.appended_blocks + 1
            ):
                print(
                    f"[Appended Blocks] Header block count mismatch {self.blocks_expected}+{self.blocks_received}+1 != {data_header.data.appended_blocks}"
                )

        self.header = data_header
        self.blocks_received += 1
        self.blocks.append(data_header)
        self.confirmed = data_header.data.response_requested
        print(
            f"[DATA HDR] received {self.blocks_received} / {self.blocks_expected} expected, {data_header.data.__class__.__name__}"
        )

    def process_csbk(self, csbk: DmrCsbk):
        if not self.type == TransmissionType.DataTransmission:
            self.new_transmission(TransmissionType.DataTransmission)
        if csbk.csbk_opcode == DmrCsbk.CsbkoTypes.preamble:
            if self.blocks_expected == 0:
                self.blocks_expected = csbk.preamble_csbk_blocks_to_follow + 1
            elif (
                self.blocks_expected - self.blocks_received
                != csbk.preamble_csbk_blocks_to_follow + 1
            ):
                print(
                    f"CSBK not setting expected to {self.blocks_expected} - {self.blocks_received} != {csbk.preamble_csbk_blocks_to_follow}"
                )

        self.blocks_received += 1
        self.blocks.append(csbk)
        print(
            f"[CSBK] received {self.blocks_received} / {self.blocks_expected} expected"
        )

    def process_rate_12_confirmed(
        self, data: Union[DmrData.Rate12Confirmed, DmrData.Rate12LastBlockConfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate12LastBlockConfirmed):
            print("rate1/2 last block confirmed", data)
            self.end_data_transmission()

    def process_rate_12_unconfirmed(
        self, data: Union[DmrData.Rate12Unconfirmed, DmrData.Rate12LastBlockUnconfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate12LastBlockUnconfirmed):
            print("rate1/2 last block unconfirmed", data.message_crc32.hex())
            self.end_data_transmission()

    def process_rate_34_confirmed(
        self, data: Union[DmrData.Rate34Confirmed, DmrData.Rate34LastBlockConfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate34LastBlockConfirmed):
            print(
                "3/4 last block dbsn:",
                data.data_block_serial_number,
                "data",
                data.user_data,
                "crc9",
                data.crc9,
                "crc32",
                data.message_crc32.hex(),
            )
            self.end_data_transmission()

    def process_rate_34_unconfirmed(
        self, data: Union[DmrData.Rate34Unconfirmed, DmrData.Rate34LastBlockUnconfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate34LastBlockUnconfirmed):
            self.end_data_transmission()

    def process_rate_1_confirmed(
        self, data: Union[DmrData.Rate1Confirmed, DmrData.Rate1LastBlockConfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate1LastBlockConfirmed):
            self.end_data_transmission()

    def process_rate_1_unconfirmed(
        self, data: Union[DmrData.Rate1Unconfirmed, DmrData.Rate1LastBlockUnconfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate1LastBlockUnconfirmed):
            self.end_data_transmission()

    def is_last_block(self, called_before_processing: bool = False):
        return self.blocks_expected != 0 and (
            self.blocks_expected
            == self.blocks_received + (1 if called_before_processing else 0)
        )

    def end_voice_transmission(self):
        if self.finished or self.type == TransmissionType.Idle:
            return
        print(f"[VOICE CALL END]")
        if isinstance(self.header, FullLinkControl):

            for observer in self.observers:
                # noinspection PyBroadException
                try:
                    observer.voice_transmission_ended(self.header, [])
                except:
                    traceback.print_exc()

            if isinstance(
                self.header.specific_data, FullLinkControl.GroupVoiceChannelUser
            ):
                print(
                    f"[GROUP] [{self.header.specific_data.source_address} -> "
                    f"{self.header.specific_data.group_address}]"
                )
            elif isinstance(
                self.header.specific_data, FullLinkControl.UnitToUnitVoiceChannelUser
            ):
                print(
                    f"[PRIVATE] [{self.header.specific_data.source_address} ->"
                    f" {self.header.specific_data.target_address}]"
                )
        else:
            print(
                f"end voice transmission unknown header type {self.header.__class__.__name__}"
            )
        self.new_transmission(TransmissionType.Idle)

    def end_data_transmission(self):
        if self.finished or self.type == TransmissionType.Idle:
            return
        if not isinstance(self.header, DmrDataHeader):
            print(f"Unexpected header type {self.header.__class__.__name__}")
            return
        print(
            f"\n[DATA CALL END] [CONFIRMED: {self.confirmed}] "
            f"[Packets {self.blocks_received}/{self.blocks_expected} ({len(self.blocks)})] "
        )

        for observer in self.observers:
            # noinspection PyBroadException
            try:
                observer.data_transmission_ended(self.header, self.blocks)
            except:
                traceback.print_exc()

        user_data: bytes = bytes()
        for packet in self.blocks:
            if isinstance(packet, DmrCsbk):
                print(
                    f"[CSBK] [{packet.preamble_source_address} -> {packet.preamble_target_address}] [{packet.preamble_group_or_individual}]"
                )
            elif isinstance(packet, DmrDataHeader):
                print(
                    f"[DATA HDR] [{packet.data_packet_format}] [{packet.data.__class__.__name__}]"
                )
            elif hasattr(packet, "user_data"):
                print(f"[DATA] [{packet.__class__.__name__}] [{packet.user_data}]")
                user_data += packet.user_data
            else:
                print(f"[UNUSED] [{packet.__class__.__name__}]")
        if (
            self.header.data.sap_identifier
            == DmrDataHeader.SapIdentifiers.udp_ip_header_compression
        ):
            if len(user_data) == 0:
                print("No user data to parse as UDP Header with data")
            else:
                udp_header_with_data = DmrIpUdp.UdpIpv4CompressedHeader.from_bytes(
                    user_data
                )
                prettyprint(udp_header_with_data)
                print(
                    "UDP DATA: "
                    + bytes(udp_header_with_data.user_data).decode("latin-1")
                )
        elif (
            self.header.data.sap_identifier
            == DmrDataHeader.SapIdentifiers.ip_based_packet_data
        ):
            print(user_data.hex())
            ip = IP(user_data)
            ip.display()
            print(
                "##",
                ip.getlayer("UDP").getfieldval("load").hex(),
                ip.getlayer("UDP").getfieldval("load").decode("utf-16-le"),
            )
        elif self.header.data.sap_identifier == DmrDataHeader.SapIdentifiers.short_data:
            if (
                hasattr(self.header.data, "defined_data")
                and self.header.data.defined_data
                == DmrDataHeader.DefinedDataFormats.bcd
            ):
                print("bcd", user_data.hex())
            else:
                prettyprint(self.header.data)
                print("user_data", user_data.hex())
                print(user_data)
        else:
            print("unhandled data", user_data.hex())

        self.new_transmission(TransmissionType.Idle)
        print("\n\n")

    def fix_voice_burst_type(self, burst: BurstInfo) -> BurstInfo:
        if not self.type == TransmissionType.VoiceTransmission:
            self.last_burst_data_type = burst.data_type
            return burst

        if burst.is_voice_superframe_start or (
            self.last_burst_data_type == DataType.VoiceBurstF
            and burst.data_type == DataType.UnknownDataType
        ):
            burst.data_type = DataType.VoiceBurstA
            self.last_burst_data_type = DataType.VoiceBurstA
        elif (
            burst.data_type == DataType.UnknownDataType
            and self.last_burst_data_type
            in [
                DataType.VoiceBurstA,
                DataType.VoiceBurstB,
                DataType.VoiceBurstC,
                DataType.VoiceBurstD,
                DataType.VoiceBurstE,
            ]
        ):
            burst.data_type = DataType(self.last_burst_data_type.value + 1)
            self.last_burst_data_type = burst.data_type
        else:
            self.last_burst_data_type = burst.data_type

        return burst

    def process_packet(self, burst: BurstInfo) -> BurstInfo:
        burst = self.fix_voice_burst_type(burst)

        lc_info_bits = decode_complete_lc(burst.data_bits[:98] + burst.data_bits[166:])
        if burst.data_type == DataType.VoiceLCHeader:
            print("voice header", lc_info_bits.tobytes().hex())
            self.process_voice_header(FullLinkControl.from_bytes(lc_info_bits))
        elif burst.data_type == DataType.DataHeader:
            self.process_data_header(DmrDataHeader.from_bytes(lc_info_bits))
        elif burst.data_type == DataType.CSBK:
            self.process_csbk(DmrCsbk.from_bytes(lc_info_bits))
        elif burst.data_type == DataType.TerminatorWithLC:
            print("voice terminator", lc_info_bits.tobytes().hex())
            self.blocks_received += 1
            self.end_voice_transmission()
        elif burst.data_type in [
            DataType.VoiceBurstA,
            DataType.VoiceBurstB,
            DataType.VoiceBurstC,
            DataType.VoiceBurstD,
            DataType.VoiceBurstE,
            DataType.VoiceBurstF,
        ]:
            if burst.data_type == DataType.VoiceBurstA:
                self.blocks_expected += 6
            self.blocks_received += 1
        elif burst.data_type == DataType.Rate12DataContinuation:
            if self.confirmed:
                if self.is_last_block(True):
                    self.process_rate_12_confirmed(
                        DmrData.Rate12LastBlockConfirmed.from_bytes(lc_info_bits)
                    )
                else:
                    self.process_rate_12_confirmed(
                        DmrData.Rate12Confirmed.from_bytes(lc_info_bits)
                    )
            else:
                if self.is_last_block(True):
                    self.process_rate_12_unconfirmed(
                        DmrData.Rate12LastBlockUnconfirmed.from_bytes(lc_info_bits)
                    )
                else:
                    self.process_rate_12_unconfirmed(
                        DmrData.Rate12Unconfirmed.from_bytes(lc_info_bits)
                    )
        elif burst.data_type == DataType.Rate34DataContinuation:
            lc_info_bits = Trellis34.decode(burst.info_bits, as_bytes=True)
            if self.confirmed:
                if self.is_last_block(True):
                    self.process_rate_34_confirmed(
                        DmrData.Rate34LastBlockConfirmed.from_bytes(lc_info_bits)
                    )
                else:
                    self.process_rate_34_confirmed(
                        DmrData.Rate34Confirmed.from_bytes(lc_info_bits)
                    )
            else:
                if self.is_last_block(True):
                    self.process_rate_34_unconfirmed(
                        DmrData.Rate34LastBlockUnconfirmed.from_bytes(lc_info_bits)
                    )
                else:
                    self.process_rate_34_unconfirmed(
                        DmrData.Rate34Unconfirmed.from_bytes(lc_info_bits)
                    )
        elif burst.data_type == DataType.Rate1DataContinuation:
            if self.confirmed:
                if self.is_last_block(True):
                    self.process_rate_1_confirmed(
                        DmrData.Rate1LastBlockConfirmed.from_bytes(lc_info_bits)
                    )
                else:
                    self.process_rate_1_confirmed(
                        DmrData.Rate1Confirmed.from_bytes(lc_info_bits)
                    )
            else:
                if self.is_last_block(True):
                    self.process_rate_1_unconfirmed(
                        DmrData.Rate1LastBlockUnconfirmed.from_bytes(lc_info_bits)
                    )
                else:
                    self.process_rate_1_unconfirmed(
                        DmrData.Rate1Unconfirmed.from_bytes(lc_info_bits)
                    )

        if self.is_last_block():
            self.end_transmissions()

        return burst

    def end_transmissions(self):
        if self.type == TransmissionType.DataTransmission:
            self.end_data_transmission()
        elif self.type == TransmissionType.VoiceTransmission:
            self.end_voice_transmission()
