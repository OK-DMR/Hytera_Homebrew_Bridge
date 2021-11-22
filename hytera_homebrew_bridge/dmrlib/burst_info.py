import datetime

from bitarray import bitarray
from bitarray.util import ba2int
from dmr_utils3.decode import to_bits
from dmr_utils3.golay import encode_2087
from dmr_utils3.qr import ENCODE_1676

from hytera_homebrew_bridge.dmrlib.data_type import DataType
from hytera_homebrew_bridge.dmrlib.sync_type import SyncType
from hytera_homebrew_bridge.lib.logging_trait import LoggingTrait


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
        status: str = f"{str(datetime.datetime.now())} [{self.sync_type.name}] [CC {self.color_code}] [DATA TYPE {self.data_type.name}]"
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
