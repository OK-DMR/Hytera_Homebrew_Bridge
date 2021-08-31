# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version("0.9"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s"
        % (kaitaistruct.__version__)
    )


class IpSiteConnectProtocol(KaitaiStruct):
    """Hytera IP Multi-Site Protocol re-implementation from dmrshark original"""

    class PacketTypes(Enum):
        a = 65
        b = 66

    class FrameTypes(Enum):
        frame_type_data = 0
        frame_type_voice_sync = 4369
        frame_type_data_sync_or_csbk = 13107
        frame_type_data_header = 26214
        frame_type_voice = 48059
        frame_type_sync = 61166

    class CallTypes(Enum):
        private_call = 0
        group_call = 1

    class SlotTypes(Enum):
        slot_type_privacy_indicator = 0
        slot_type_voice_lc_header = 4369
        slot_type_terminator_with_lc = 8738
        slot_type_csbk = 13107
        slot_type_data_header = 17476
        slot_type_rate_12_data = 21845
        slot_type_rate_34_data = 26214
        slot_type_data_c = 30583
        slot_type_data_d = 34952
        slot_type_data_e = 39321
        slot_type_data_f = 43690
        slot_type_data_a = 48059
        slot_type_data_b = 52428
        slot_type_wakeup_request = 56797
        slot_type_sync = 61166

    class Timeslots(Enum):
        timeslot_1 = 4369
        timeslot_2 = 8738

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.source_port = self._io.read_bytes(2)
        self.fixed_header = self._io.read_bytes(2)
        self.sequence_number = self._io.read_u1()
        self.reserved_3 = self._io.read_bytes(3)
        self.packet_type = KaitaiStream.resolve_enum(
            IpSiteConnectProtocol.PacketTypes, self._io.read_u1()
        )
        self.reserved_7a = self._io.read_bytes(7)
        self.timeslot_raw = KaitaiStream.resolve_enum(
            IpSiteConnectProtocol.Timeslots, self._io.read_u2be()
        )
        self.slot_type = KaitaiStream.resolve_enum(
            IpSiteConnectProtocol.SlotTypes, self._io.read_u2be()
        )
        self.color_code_raw = self._io.read_u2le()
        self.frame_type = KaitaiStream.resolve_enum(
            IpSiteConnectProtocol.FrameTypes, self._io.read_u2be()
        )
        self.reserved_2a = self._io.read_bytes(2)
        self.ipsc_payload = self._io.read_bytes(34)
        self.reserved_2b = self._io.read_bytes(2)
        self.call_type = KaitaiStream.resolve_enum(
            IpSiteConnectProtocol.CallTypes, self._io.read_u1()
        )
        self.destination_radio_id_raw = self._io.read_u4le()
        self.source_radio_id_raw = self._io.read_u4le()
        self.reserved_1b = self._io.read_u1()
        if not (self._io.is_eof()):
            self.extra_data = self._io.read_bytes_full()

    @property
    def source_radio_id(self):
        if hasattr(self, "_m_source_radio_id"):
            return (
                self._m_source_radio_id if hasattr(self, "_m_source_radio_id") else None
            )

        self._m_source_radio_id = self.source_radio_id_raw >> 8
        return self._m_source_radio_id if hasattr(self, "_m_source_radio_id") else None

    @property
    def destination_radio_id(self):
        if hasattr(self, "_m_destination_radio_id"):
            return (
                self._m_destination_radio_id
                if hasattr(self, "_m_destination_radio_id")
                else None
            )

        self._m_destination_radio_id = self.destination_radio_id_raw >> 8
        return (
            self._m_destination_radio_id
            if hasattr(self, "_m_destination_radio_id")
            else None
        )

    @property
    def color_code(self):
        if hasattr(self, "_m_color_code"):
            return self._m_color_code if hasattr(self, "_m_color_code") else None

        self._m_color_code = self.color_code_raw & 15
        return self._m_color_code if hasattr(self, "_m_color_code") else None
