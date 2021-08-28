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


class LinkControl(KaitaiStruct):
    """ETSI TS 102 361-2 V2.4.1 (2017-10), Section 7.1.1"""

    class Flcos(Enum):
        group_voice = 0
        unit_to_unit_voice = 3
        talker_alias_header = 4
        talker_alias_block1 = 5
        talker_alias_block2 = 6
        talker_alias_block3 = 7
        gps_info = 8

    class PositionErrors(Enum):
        less_than_2m = 0
        less_than_20m = 1
        less_than_200m = 2
        less_than_2km = 3
        less_than_20km = 4
        less_than_or_equal_200km = 5
        more_than_200km = 6
        position_error_unknown_or_invalid = 7

    class TalkerDataFormats(Enum):
        coding_7bit = 0
        coding_8bit = 1
        unicode_utf8 = 2
        unicode_utf16 = 3

    class FeatureSetIds(Enum):
        standardized_ts_102_361_2 = 0
        reserved1 = 1
        reserved2 = 2
        reserved3 = 3
        mfid_start = 4
        mfid_end = 127
        mfid_reserved_start = 128
        mfid_reserved_end = 255

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.protect_flag = self._io.read_bits_int_be(1) != 0
        self.reserved = self._io.read_bits_int_be(1) != 0
        self.full_link_control_opcode = KaitaiStream.resolve_enum(
            LinkControl.Flcos, self._io.read_bits_int_be(6)
        )
        self.feature_set_id = KaitaiStream.resolve_enum(
            LinkControl.FeatureSetIds, self._io.read_bits_int_be(8)
        )
        self._io.align_to_byte()
        _on = self.full_link_control_opcode
        if _on == LinkControl.Flcos.talker_alias_header:
            self.specific_data = LinkControl.TalkerAliasHeader(
                self._io, self, self._root
            )
        elif _on == LinkControl.Flcos.unit_to_unit_voice:
            self.specific_data = LinkControl.UnitToUnitVoiceChannelUser(
                self._io, self, self._root
            )
        elif _on == LinkControl.Flcos.group_voice:
            self.specific_data = LinkControl.GroupVoiceChannelUser(
                self._io, self, self._root
            )
        elif _on == LinkControl.Flcos.talker_alias_block3:
            self.specific_data = LinkControl.TalkerAliasContinuation(
                self._io, self, self._root
            )
        elif _on == LinkControl.Flcos.talker_alias_block1:
            self.specific_data = LinkControl.TalkerAliasContinuation(
                self._io, self, self._root
            )
        elif _on == LinkControl.Flcos.talker_alias_block2:
            self.specific_data = LinkControl.TalkerAliasContinuation(
                self._io, self, self._root
            )
        elif _on == LinkControl.Flcos.gps_info:
            self.specific_data = LinkControl.GpsInfoLcPdu(self._io, self, self._root)

    class GpsInfoLcPdu(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved = self._io.read_bits_int_be(4)
            self.position_error = KaitaiStream.resolve_enum(
                LinkControl.PositionErrors, self._io.read_bits_int_be(3)
            )
            self.longitude = self._io.read_bits_int_be(25)
            self.latitude = self._io.read_bits_int_be(24)

    class GroupVoiceChannelUser(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.service_options = self._io.read_bits_int_be(8)
            self.group_address = self._io.read_bits_int_be(24)
            self.source_address = self._io.read_bits_int_be(24)

    class UnitToUnitVoiceChannelUser(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.service_options = self._io.read_bits_int_be(8)
            self.target_address = self._io.read_bits_int_be(24)
            self.source_address = self._io.read_bits_int_be(24)

    class TalkerAliasHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.talker_alias_data_format = KaitaiStream.resolve_enum(
                LinkControl.TalkerDataFormats, self._io.read_bits_int_be(2)
            )
            self.talker_alias_data_length = self._io.read_bits_int_be(5)
            self.talker_alias_data = self._io.read_bits_int_be(49)

    class TalkerAliasContinuation(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.talker_alias_data = self._io.read_bits_int_be(56)
