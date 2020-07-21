# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class HyteraDmrApplicationProtocol(KaitaiStruct):

    class MessageHeaderTypes(Enum):
        radio_control_protocol = 2
        location_protocol = 8
        text_message_protocol = 9
        radio_registration = 17
        telemetry_protocol = 18
        data_transmit_protocol = 19
        data_delivery_states = 20
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.message_header = self._io.read_u1()
        self.is_reliable_message = self._io.read_bits_int(1) != 0
        self._io.align_to_byte()
        _on = self.message_header
        if _on == 2:
            self.opcode = self._io.read_u2le()
        elif _on == 130:
            self.opcode = self._io.read_u2le()
        else:
            self.opcode = self._io.read_u2be()
        _on = self.message_header
        if _on == 2:
            self.payload_size = self._io.read_u2le()
        elif _on == 130:
            self.payload_size = self._io.read_u2le()
        else:
            self.payload_size = self._io.read_u2be()
        self.payload = self._io.read_bytes(self.payload_size)
        self.checksum = self._io.read_u1()
        self.message_footer = self._io.ensure_fixed_contents(b"\x03")


