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

from hytera_homebrew_bridge.kaitai import radio_ip


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
        self.opcode = self._io.read_bytes(1)
        if not self.opcode == b"\x00":
            raise kaitaistruct.ValidationNotEqualError(
                b"\x00", self.opcode, self._io, u"/seq/0"
            )
        self.rrs_type = KaitaiStream.resolve_enum(
            RadioRegistrationService.RrsTypes, self._io.read_u1()
        )
        self.message_length = self._io.read_u2le()
        self.radio_ip = radio_ip.RadioIp(self._io)
        if (self.rrs_type == RadioRegistrationService.RrsTypes.registration_ack) or (
            self.rrs_type == RadioRegistrationService.RrsTypes.online_check_ack
        ):
            self.result = self._io.read_u1()

        if self.rrs_type == RadioRegistrationService.RrsTypes.registration_ack:
            self.valid_time = self._io.read_u4be()
