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

from kaitai import radio_id


class RealTimeTransportProtocol(KaitaiStruct):
    """each packet should contain 60ms of voice data for AMBE compatibility"""

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
        self.fixed_header = RealTimeTransportProtocol.FixedHeader(
            self._io, self, self._root
        )
        if int(self.fixed_header.extension) == 1:
            self.header_extension = RealTimeTransportProtocol.HeaderExtension(
                self._io, self, self._root
            )

        self.audio_data = self._io.read_bytes_full()

    class FixedHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.version = self._io.read_bits_int_be(2)
            self.padding = self._io.read_bits_int_be(1) != 0
            self.extension = self._io.read_bits_int_be(1) != 0
            self.csrc_count = self._io.read_bits_int_be(4)
            self.marker = self._io.read_bits_int_be(1) != 0
            self.payload_type = self._io.read_bits_int_be(7)
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
            self.slot = self._io.read_bits_int_be(7)
            self.last_flag = self._io.read_bits_int_be(1) != 0
            self._io.align_to_byte()
            self.source_id = radio_id.RadioId(self._io)
            self.destination_id = radio_id.RadioId(self._io)
            self.call_type = KaitaiStream.resolve_enum(
                RealTimeTransportProtocol.CallTypes, self._io.read_u1()
            )
            self.reserved = self._io.read_bytes(4)
