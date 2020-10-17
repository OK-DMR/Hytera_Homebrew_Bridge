# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version("0.7"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s"
        % (ks_version)
    )


class IpSiteConnectProtocol(KaitaiStruct):
    """Hytera IP Multi-Site Protocol re-implementation from dmrshark original"""

    class SlotTypes(Enum):
        slot_type_unknown = 0
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
        slot_type_ipsc_sync = 61166

    class PacketTypes(Enum):
        a = 65
        b = 66

    class Timeslots(Enum):
        timeslot_1 = 4369
        timeslot_2 = 8738

    class CallTypes(Enum):
        private_call = 0
        group_call = 1

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.fixed_header = self._io.read_bytes(4)
        self.sequence_number = self._io.read_u1()
        self.reserved_3 = self._io.read_bytes(3)
        self.packet_type = KaitaiStream.resolve_enum(
            self._root.PacketTypes, self._io.read_u1()
        )
        self.reserved_7a = self._io.read_bytes(7)
        self.timeslot_raw = KaitaiStream.resolve_enum(
            self._root.Timeslots, self._io.read_u2be()
        )
        self.slot_type = KaitaiStream.resolve_enum(
            self._root.SlotTypes, self._io.read_u2be()
        )
        self.delimiter = self._io.ensure_fixed_contents(b"\x11\x11")
        self.frame_type = self._io.read_u2be()
        self.reserved_2a = self._io.read_bytes(2)
        self.ipsc_payload = self._io.read_bytes(34)
        self.reserved_2b = self._io.read_bytes(2)
        self.call_type = KaitaiStream.resolve_enum(
            self._root.CallTypes, self._io.read_u1()
        )
        self.destination_radio_id_raw = self._io.read_u4le()
        self.source_radio_id_raw = self._io.read_u4le()
        self.reserved_1b = self._io.read_u1()

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
