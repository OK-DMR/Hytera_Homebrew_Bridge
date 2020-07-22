# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from kaitai import location_protocol
from kaitai import radio_registration_service
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
        _on = self.message_type
        if _on == self._root.MessageHeaderTypes.location_protocol:
            self.data = location_protocol.LocationProtocol(self._io)
        elif _on == self._root.MessageHeaderTypes.radio_registration:
            self.data = radio_registration_service.RadioRegistrationService(self._io)
        self.checksum = self._io.read_u1()
        self.message_footer = self._io.ensure_fixed_contents(b"\x03")

    @property
    def is_reliable_message(self):
        if hasattr(self, '_m_is_reliable_message'):
            return self._m_is_reliable_message if hasattr(self, '_m_is_reliable_message') else None

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_is_reliable_message = self._io.read_u1()
        self._io.seek(_pos)
        return self._m_is_reliable_message if hasattr(self, '_m_is_reliable_message') else None

    @property
    def message_type(self):
        if hasattr(self, '_m_message_type'):
            return self._m_message_type if hasattr(self, '_m_message_type') else None

        self._m_message_type = KaitaiStream.resolve_enum(self._root.MessageHeaderTypes, (self.message_header ^ 128))
        return self._m_message_type if hasattr(self, '_m_message_type') else None


