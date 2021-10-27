#!/usr/bin/env python3
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from bitarray import bitarray
from bitarray.util import ba2int
from dmr_utils3.decode import to_bits
from dmr_utils3.golay import encode_2087
from dmr_utils3.qr import ENCODE_1676
from kaitaistruct import KaitaiStruct
from kamene.layers.inet import IP

from hytera_homebrew_bridge.dmrlib.decode import decode_complete_lc
from hytera_homebrew_bridge.dmrlib.trellis import trellis_34_decode_as_bytes
from hytera_homebrew_bridge.kaitai.dmr_csbk import DmrCsbk
from hytera_homebrew_bridge.kaitai.dmr_data import DmrData
from hytera_homebrew_bridge.kaitai.dmr_data_header import DmrDataHeader
from hytera_homebrew_bridge.kaitai.dmr_ip_udp import DmrIpUdp
from hytera_homebrew_bridge.kaitai.link_control import LinkControl
from hytera_homebrew_bridge.lib.logging_trait import LoggingTrait
from hytera_homebrew_bridge.tests.prettyprint import _prettyprint


class TransmissionType(Enum):
    Idle = 0
    VoiceTransmission = 1
    DataTransmission = 2


class SyncType(Enum):
    BsSourcedVoice = 0x755FD7DF75F7
    BsSourcedData = 0xDFF57D75DF5D
    MsSourcedVoice = 0x7F7D5DD57DFD
    MsSourcedData = 0xD5D7F77FD757
    MsSourcedRcSync = 0x77D55F7DFD77
    Tdma1Voice = 0x5D577F7757FF
    Tdma1Data = 0xF7FDD5DDFD55
    Tdma2Voice = 0x7DFFD5F55D5F
    Tdma2Data = 0xD7557F5FF7F5
    Reserved = 0xDD7FF5D757DD
    EmbeddedData = -1


class DataType(Enum):
    PrivacyIndicatorHeader = 0
    VoiceLCHeader = 1
    TerminatorWithLC = 2
    CSBK = 3
    MBCHeader = 4
    MBCContinuation = 5
    DataHeader = 6
    Rate12DataContinuation = 7
    Rate34DataContinuation = 8
    Idle = 9
    Rate1DataContinuation = 10
    UnifiedSingleBlockData = 11
    VoiceBurstA = 12
    VoiceBurstB = 13
    VoiceBurstC = 14
    VoiceBurstD = 15
    VoiceBurstE = 16
    VoiceBurstF = 17
    IPSCSync = 18
    UnknownDataType = 19


class BurstInfo(LoggingTrait):
    def __init__(self, data: bytes):
        self.data_bits: bitarray = to_bits(data)
        self.payload_bits: bitarray = self.data_bits[:108] + self.data_bits[156:]
        self.info_bits: bitarray = self.data_bits[:98] + self.data_bits[166:]
        self.sync_or_emb: bitarray = self.data_bits[108:156]
        self.sync_type: SyncType = SyncType.Reserved
        self.has_emb: bool = False
        self.is_voice_superframe_start: bool = False
        self.is_data_or_control: bool = False
        self.is_valid: bool = False
        self.color_code: int = 0
        self.sequence_no: int = 0
        self.stream_no: bytes = bytes(4)
        self.data_type: DataType = DataType.UnknownDataType
        """
        Parity for slot_type information
        """
        self.fec_parity: int = 0
        self.fec_parity_ok: bool = False
        """
        Parity for EMB metadata
        """
        self.emb_parity: int = 0
        self.emb_parity_ok: bool = False
        """
        0 =>    The embedded signalling carries information
                associated to the same logical channel or the Null
                embedded message (see note)
        1 =>    The embedded signalling carries RC information
                associated to the other logical channel (see note)
        """
        self.pre_emption_and_power_control_indicator: int = 0
        self.link_control_start_stop_lcss: int = 0

        self.detect_sync_type()
        self.parse_slot_type()
        self.parse_emb()

    def set_sequence_no(self, sequence_no: int) -> "BurstInfo":
        self.sequence_no = sequence_no
        return self

    def set_stream_no(self, stream_no: bytes) -> "BurstInfo":
        self.stream_no = stream_no
        return self

    def detect_sync_type(self):
        try:
            self.sync_type = SyncType(ba2int(self.sync_or_emb))
            self.is_voice_superframe_start = self.sync_type in [
                SyncType.Tdma2Voice,
                SyncType.Tdma1Voice,
                SyncType.MsSourcedVoice,
                SyncType.BsSourcedVoice,
            ]
            self.is_data_or_control = self.sync_type in [
                SyncType.Tdma1Data,
                SyncType.Tdma2Data,
                SyncType.BsSourcedData,
                SyncType.MsSourcedData,
            ]
        except:
            self.sync_type = SyncType.EmbeddedData
            self.has_emb = True

    def parse_slot_type(self):
        if not self.is_data_or_control:
            return
        """Section 6.2 Data and control"""
        slot_type_bits = self.data_bits[98:108] + self.data_bits[156:166]
        # Check FEC for SlotType
        calculated_fec = encode_2087(chr(ba2int(slot_type_bits[0:8])))
        self.fec_parity_ok = calculated_fec == ba2int(slot_type_bits)
        # Parse SlotType data
        self.color_code = ba2int(slot_type_bits[:4])
        self.data_type = DataType(ba2int(slot_type_bits[4:8]))
        self.fec_parity = ba2int(slot_type_bits[8:])

    def parse_emb(self):
        if not self.has_emb or self.is_voice_superframe_start:
            return
        """Section 9.1.2 Embedded signalling (EMB) PDU"""
        emb_bits = self.data_bits[108:116] + self.data_bits[148:156]
        # Check EMB Parity
        calculated_parity = ENCODE_1676[ba2int(emb_bits[:7])]
        # This does not work always
        self.emb_parity_ok = calculated_parity == ba2int(emb_bits)
        # Parse EMB data
        self.color_code = ba2int(emb_bits[:4])
        self.pre_emption_and_power_control_indicator = ba2int(emb_bits[4:5])
        self.link_control_start_stop_lcss = ba2int(emb_bits[6:8])
        self.emb_parity = ba2int(emb_bits[8:])

    def debug(self, printout: bool = True) -> str:
        status: str = f"[{self.sync_type.name}] [CC {self.color_code}] [DATA TYPE {self.data_type.name}]"
        if self.is_data_or_control:
            status += (
                f" [FEC {self.fec_parity.to_bytes(2, byteorder='big').hex()}"
                f"{' VERIFIED' if self.fec_parity_ok else ''}]"
            )
        if self.has_emb:
            status += (
                f" [PI {self.pre_emption_and_power_control_indicator}]"
                f" [LCSS {self.link_control_start_stop_lcss}]"
                f" [EMB Parity {self.emb_parity.to_bytes(2, byteorder='big').hex()}"
                f"{' VERIFIED' if self.emb_parity_ok else ''}]"
            )
        if printout:
            print(status)
        return status


class Transmission:
    def __init__(self):
        self.type = TransmissionType.Idle
        self.blocks_expected: int = 0
        self.blocks_received: int = 0
        self.last_burst_data_type: DataType = DataType.UnknownDataType
        self.confirmed: bool = False
        self.finished: bool = False
        self.blocks: List[KaitaiStruct] = list()
        self.header: Optional[KaitaiStruct] = None

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

    def process_voice_header(self, voice_header: LinkControl):
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
                self.blocks_received + data_header.data.blocks_to_follow
            ):
                print(
                    f"Header block count mismatch {self.blocks_expected}-{self.blocks_received} != {data_header.data.blocks_to_follow}"
                )

        print(_prettyprint(data_header.data))
        self.header = data_header
        self.blocks_received += 1
        self.blocks.append(data_header)
        self.confirmed = data_header.data.response_requested

    def process_csbk(self, csbk: DmrCsbk):
        if not self.type == TransmissionType.DataTransmission:
            self.new_transmission(TransmissionType.DataTransmission)
        if csbk.csbk_opcode == DmrCsbk.CsbkoTypes.preamble:
            if self.blocks_expected == 0:
                self.blocks_expected = csbk.preamble_csbk_blocks_to_follow + 1
            else:
                print(
                    f"CSBK not setting expected to {csbk.preamble_csbk_blocks_to_follow}"
                )

        self.blocks_received += 1
        self.blocks.append(csbk)
        print(_prettyprint(csbk))

    def process_rate_12_confirmed(
        self, data: Union[DmrData.Rate12Confirmed, DmrData.Rate12LastBlockConfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate12LastBlockConfirmed):
            self.end_data_transmission()

    def process_rate_12_unconfirmed(
        self, data: Union[DmrData.Rate12Unconfirmed, DmrData.Rate12LastBlockUnconfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate12LastBlockUnconfirmed):
            self.end_data_transmission()

    def process_rate_34_confirmed(
        self, data: Union[DmrData.Rate34Confirmed, DmrData.Rate34LastBlockConfirmed]
    ):
        self.blocks_received += 1
        self.blocks.append(data)
        if isinstance(data, DmrData.Rate34LastBlockConfirmed):
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
        if isinstance(self.header, LinkControl):
            if isinstance(self.header.specific_data, LinkControl.GroupVoiceChannelUser):
                print(
                    f"[GROUP] [{self.header.specific_data.source_address} -> "
                    f"{self.header.specific_data.group_address}]"
                )
            elif isinstance(
                self.header.specific_data, LinkControl.UnitToUnitVoiceChannelUser
            ):
                print(
                    f"[PRIVATE] [{self.header.specific_data.source_address} ->"
                    f" {self.header.specific_data.target_address}]"
                )

        self.new_transmission(TransmissionType.Idle)

    def end_data_transmission(self):
        if self.finished or self.type == TransmissionType.Idle:
            return
        if not isinstance(self.header, DmrDataHeader):
            print(f"Unexpected header type {self.header.__class__.__name__}")
            return
        print(
            f"[DATA CALL END] [CONFIRMED: {self.confirmed}] "
            f"[Packets {self.blocks_received}/{self.blocks_expected} ({len(self.blocks)})] "
        )
        user_data: bytes = bytes()
        for packet in self.blocks:
            if isinstance(packet, DmrCsbk):
                print(
                    f"[CSBK] [{packet.preamble_source_address} -> {packet.preamble_target_address}] [{packet.preamble_group_or_individual}]"
                )
                print(_prettyprint(packet))
            elif isinstance(packet, DmrDataHeader):
                print(
                    f"[DATA HDR] [{packet.data_packet_format}] [{packet.data.__class__.__name__}]"
                )
                print(_prettyprint(packet.data))
            elif hasattr(packet, "user_data"):
                print(f"[DATA] [{packet.__class__.__name__}] [{packet.user_data}]")
                print(_prettyprint(packet))
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
                print(_prettyprint(udp_header_with_data))
                print(
                    "UDP DATA: "
                    + bytes(udp_header_with_data.user_data).decode("latin-1")
                )
        elif (
            self.header.data.sap_identifier
            == DmrDataHeader.SapIdentifiers.ip_based_packet_data
        ):
            print(user_data)
            ip = IP(user_data)
            ip.display()
        elif self.header.data.sap_identifier == DmrDataHeader.SapIdentifiers.short_data:
            if (
                hasattr(self.header.data, "defined_data")
                and self.header.data.defined_data
                == DmrDataHeader.DefinedDataFormats.bcd
            ):
                print("bcd", user_data.hex())
                print("bcd latin", user_data.decode("latin1"))
        self.new_transmission(TransmissionType.Idle)

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
            self.process_voice_header(LinkControl.from_bytes(lc_info_bits))
        elif burst.data_type == DataType.DataHeader:
            self.process_data_header(DmrDataHeader.from_bytes(lc_info_bits))
        elif burst.data_type == DataType.CSBK:
            self.process_csbk(DmrCsbk.from_bytes(lc_info_bits))
        elif burst.data_type == DataType.TerminatorWithLC:
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
            lc_info_bits = trellis_34_decode_as_bytes(burst.info_bits)
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


class Timeslot:
    def __init__(self, timeslot: int):
        self.timeslot = timeslot
        self.last_packet_received: float = 0
        self.rx_sequence: int = 0
        self.transmission: Transmission = Transmission()
        self.color_code: int = 1

    def get_rx_sequence(self, increment: bool = True) -> int:
        if increment:
            self.rx_sequence = (self.rx_sequence + 1) & 255
        return self.rx_sequence

    def process_burst(self, dmrdata: BurstInfo) -> BurstInfo:
        self.last_packet_received = time.time()
        if dmrdata.color_code != 0:
            self.color_code = dmrdata.color_code
        return self.transmission.process_packet(dmrdata).set_sequence_no(
            self.get_rx_sequence()
        )

    def debug(self, printout: bool = True) -> str:
        status: str = (
            f"[TS {self.timeslot}] "
            f"[STATUS {self.transmission.type.name}] "
            f"[LAST PACKET {datetime.fromtimestamp(self.last_packet_received)} {self.transmission.last_burst_data_type.name}] "
            f"[COLOR CODE {self.color_code}]"
        )
        if printout:
            print(status)
        return status


class Terminal:
    def __init__(self, dmrid: int, callsign: str = ""):
        self.id: int = dmrid
        self.call: str = callsign
        self.timeslots: Dict[int, Timeslot] = {
            1: Timeslot(timeslot=1),
            2: Timeslot(timeslot=2),
        }

    def set_callsign_alias(self, newalias: str):
        self.call = newalias

    def process_dmr_data(self, dmrdata: bytes, timeslot: int) -> BurstInfo:
        burst = BurstInfo(data=dmrdata)
        return self.timeslots[timeslot].process_burst(burst)

    def get_status(self) -> TransmissionType:
        for tsdata in self.timeslots.values():
            return tsdata.transmission.type
        return TransmissionType.Idle

    def debug(self, printout: bool = True) -> str:
        status: str = f"[ID: {self.id}] [CALL: {self.call}]\n"
        for ts in self.timeslots.values():
            status += "\t" + ts.debug(False) + "\n"

        if printout:
            print(status)
        return status
