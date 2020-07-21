# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version("0.7"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s"
        % (ks_version)
    )


class HyteraRadioNetworkProtocol(KaitaiStruct):
    class Opcodes(Enum):
        data = 0
        data_ack = 16
        close_ack = 250
        close = 251
        reject = 252
        accept = 253
        connect = 254

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header_identifier = self._io.ensure_fixed_contents(b"\x7E")
        self.version = self._io.read_u1()
        self.block = self._io.read_u1()
        self.opcode = self._io.read_u1()
        self.source_id = self._io.read_u1()
        self.destination_id = self._io.read_u1()
        self.packet_number = self._io.read_u2be()
        self.hrnp_packet_length = self._io.read_u2be()
        self.checksum = self._io.read_u2be()
        self.data = self._io.read_bytes_full()
