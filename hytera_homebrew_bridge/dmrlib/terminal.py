#!/usr/bin/env python3
import time
from binascii import hexlify
from datetime import datetime
from enum import Enum
from typing import Dict, List

from bitarray import bitarray
from bitarray.util import ba2int
from dmr_utils3.decode import to_bits


class TerminalStatus(Enum):
    Idle = 0
    VoiceCallActive = 1
    DataCallActive = 2


class TransmissionType(Enum):
    Unknown = 0
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
    PiHeader = 0
    VoiceLCHeader = 1
    TerminatorWithLC = 2
    CSBK = 3
    MBCHeader = 4
    MBCContinuation = 5
    DataHeader = 6
    Rate12DataContinuation = 7
    Rate34DataContinuation = 8
    Idle = 9
    UnifiedSingleBlockData = 10


class BurstInfo:
    def __init__(self, data: bytes):
        self.data_bits: bitarray = to_bits(data)
        self.payload_bits: bitarray = self.data_bits[:108] + self.data_bits[156:]
        self.sync_or_emb: bitarray = self.data_bits[108:156]
        self.sync_type: SyncType = SyncType.Reserved
        self.has_emb: bool = False
        self.is_voice_superframe_start: bool = False
        self.is_data_or_control: bool = False
        self.is_valid: bool = False
        self.color_code: int = 0
        self.data_type: int = 0
        self.fec_parity: int = 0
        self.emb_parity: int = 0
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
        self.color_code = ba2int(slot_type_bits[:4])
        self.data_type = ba2int(slot_type_bits[4:8])
        self.fec_parity = ba2int(slot_type_bits[8:])

    def parse_emb(self):
        if not self.has_emb:
            return
        """Section 9.1.2 Embedded signalling (EMB) PDU"""
        emb_bits = self.data_bits[108:116] + self.data_bits[148:156]
        self.color_code = ba2int(emb_bits[:4])
        self.pre_emption_and_power_control_indicator = ba2int(emb_bits[4:5])
        self.link_control_start_stop_lcss = ba2int(emb_bits[6:8])
        self.emb_parity = ba2int(emb_bits[8:])

    def debug(self, printout: bool = True) -> str:
        status: str = f"[{self.sync_type.name}] [CC {self.color_code}]"
        if self.is_data_or_control:
            status += (
                f" [FEC {self.fec_parity.to_bytes(2, byteorder='big').hex()}]"
                f" [DATA TYPE {DataType(self.data_type)}]"
            )
        if self.has_emb:
            status += (
                f" [PI {self.pre_emption_and_power_control_indicator}]"
                f" [LCSS {self.link_control_start_stop_lcss}]"
                f" [EMB Parity {self.emb_parity.to_bytes(2, byteorder='big').hex()}]"
            )
        if printout:
            print(status)
        return status


class DataBlock:
    def __init__(self):
        self.is_confirmed = False
        self.data_block_serial_number: int = 0
        self.crc9: int = 0
        self.ok: bool = False


class Transmission:
    def __init__(self):
        self.type = TransmissionType.Unknown
        self.blocks_expected: int = 0
        self.blocks_received: int = 0
        self.blocks: List[DataBlock] = list()


class Timeslot:
    def __init__(self, timeslot: int):
        self.timeslot = timeslot
        self.last_packet_received: float = 0
        self.rx_sequence: int = 0
        self.transmission: Transmission = Transmission()
        self.color_code: int = 1

    def process_burst(self, dmrdata: BurstInfo):
        self.last_packet_received = time.time()

    def debug(self, printout: bool = True) -> str:
        status: str = f"[TS {self.timeslot}] [LAST PACKET {datetime.fromtimestamp(self.last_packet_received)}]"
        if printout:
            print(status)
        return status


class Terminal:
    def __init__(self, dmrid: int, callsign: str = ""):
        self.status: TerminalStatus = TerminalStatus.Idle
        self.id: int = dmrid
        self.call: str = callsign
        self.timeslots: Dict[int, Timeslot] = {
            1: Timeslot(timeslot=1),
            2: Timeslot(timeslot=2),
        }

    def set_callsign_alias(self, newalias: str):
        self.call = newalias

    def process_dmr_data(self, dmrdata: bytes, timeslot: int):
        burst = BurstInfo(data=dmrdata)
        burst.debug()
        self.timeslots[timeslot].process_burst(burst)

    def debug(self, printout: bool = True) -> str:
        status: str = (
            f"[STATUS: {self.status.name}] [ID: {self.id}] [CALL: {self.call}]\n"
        )
        for ts in self.timeslots.values():
            status += "\t" + ts.debug(False) + "\n"

        if printout:
            print(status)
        return status
