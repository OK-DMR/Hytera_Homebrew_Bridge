# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version("0.7"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s"
        % (ks_version)
    )


class RealTimeTransportProtocol(KaitaiStruct):
    """each packet should contain 60ms of voice data for AMBE compatibility
    """

    class RtpPayloadTypes(Enum):
        mu_law = 0
        a_law = 8

    class CallTypes(Enum):
        private_call = 0
        group_call = 1
        all_call = 2

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.fixed_header = self._root.FixedHeader(self._io, self, self._root)
        if int(self.fixed_header.extension) == 1:
            self.header_extension = self._root.HeaderExtension(
                self._io, self, self._root
            )

        self.audio_data = self._io.read_bytes_full()

    class RadioId(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.radio_id_1 = self._io.read_u1()
            self.radio_id_2 = self._io.read_u1()
            self.radio_id_3 = self._io.read_u1()

        @property
        def id(self):
            if hasattr(self, "_m_id"):
                return self._m_id if hasattr(self, "_m_id") else None

            self._m_id = (
                str(self.radio_id_1) + str(self.radio_id_2) + str(self.radio_id_3)
            )
            return self._m_id if hasattr(self, "_m_id") else None

    class FixedHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.version = self._io.read_bits_int(2)
            self.padding = self._io.read_bits_int(1) != 0
            self.extension = self._io.read_bits_int(1) != 0
            self.csrc_count = self._io.read_bits_int(4)
            self.marker = self._io.read_bits_int(1) != 0
            self.payload_type = self._io.read_bits_int(7)
            self._io.align_to_byte()
            self.sequence_number = self._io.read_u2be()
            self.timestamp = self._io.read_u4be()
            self.ssrc = self._io.read_u4be()
            self.csrc = [None] * (self.csrc_count)
            for i in range(self.csrc_count):
                self.csrc[i] = self._io.read_u4be()

    class HeaderExtension(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header_identifier = self._io.read_u2be()
            self.length = self._io.read_u2be()
            self.slot = self._io.read_bits_int(7)
            self.last_flag = self._io.read_bits_int(1) != 0
            self._io.align_to_byte()
            self.source_id = self._root.RadioId(self._io, self, self._root)
            self.destination_id = self._root.RadioId(self._io, self, self._root)
            self.call_type = KaitaiStream.resolve_enum(
                self._root.CallTypes, self._io.read_u1()
            )
            self.reserved = self._io.read_bytes(4)
