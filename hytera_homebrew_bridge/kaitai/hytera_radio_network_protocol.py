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

from hytera_homebrew_bridge.kaitai import hytera_dmr_application_protocol


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
        self.header_identifier = self._io.read_bytes(1)
        if not self.header_identifier == b"\x7E":
            raise kaitaistruct.ValidationNotEqualError(
                b"\x7E", self.header_identifier, self._io, u"/seq/0"
            )
        self.version = self._io.read_u1()
        self.block = self._io.read_u1()
        self.opcode = KaitaiStream.resolve_enum(
            HyteraRadioNetworkProtocol.Opcodes, self._io.read_u1()
        )
        self.source_id = self._io.read_u1()
        self.destination_id = self._io.read_u1()
        self.packet_number = self._io.read_u2be()
        self.hrnp_packet_length = self._io.read_u2be()
        self.checksum = self._io.read_u2be()
        if self.opcode == HyteraRadioNetworkProtocol.Opcodes.data:
            self.data = hytera_dmr_application_protocol.HyteraDmrApplicationProtocol(
                self._io
            )
