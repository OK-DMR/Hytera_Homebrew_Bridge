# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version("0.7"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s"
        % (ks_version)
    )

from kaitai import radio_ip


class RadioRegistrationService(KaitaiStruct):
    class RrsTypes(Enum):
        de_registration = 1
        online_check = 2
        registration = 3
        registration_ack = 128
        online_check_ack = 130

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.opcode = self._io.ensure_fixed_contents(b"\x00")
        self.rrs_type = KaitaiStream.resolve_enum(
            self._root.RrsTypes, self._io.read_u1()
        )
        self.message_length = self._io.read_u2le()
        self.radio_ip = radio_ip.RadioIp(self._io)
        if (self.rrs_type == self._root.RrsTypes.registration_ack) or (
            self.rrs_type == self._root.RrsTypes.online_check_ack
        ):
            self.result = self._io.read_u1()

        if self.rrs_type == self._root.RrsTypes.registration_ack:
            self.valid_time = self._io.read_u4be()
