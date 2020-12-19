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


class RadioControlProtocol(KaitaiStruct):
    class ServiceTypes(Enum):
        call_request = 2113
        call_reply = 34881

    class CallTypes(Enum):
        private_call = 0
        group_call = 1
        all_call = 2
        emergency_group_call = 3
        remote_monitor_call = 4
        reserved = 5
        priority_private_call = 6
        priority_group_call = 7
        priority_all_call = 8

    class CallReplyResults(Enum):
        success = 0
        failure = 1

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.service_type = KaitaiStream.resolve_enum(
            RadioControlProtocol.ServiceTypes, self._io.read_u2le()
        )
        self.message_length = self._io.read_u2le()
        _on = self.service_type
        if _on == RadioControlProtocol.ServiceTypes.call_request:
            self.data = RadioControlProtocol.CallRequest(self._io, self, self._root)
        elif _on == RadioControlProtocol.ServiceTypes.call_reply:
            self.data = RadioControlProtocol.CallReply(self._io, self, self._root)
        else:
            self.data = RadioControlProtocol.GenericData(self._io, self, self._root)

    class CallRequest(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.call_type = KaitaiStream.resolve_enum(
                RadioControlProtocol.CallTypes, self._io.read_u1()
            )
            self.target_id = self._io.read_u4le()

    class CallReply(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.result = KaitaiStream.resolve_enum(
                RadioControlProtocol.CallReplyResults, self._io.read_u1()
            )

    class GenericData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(self._parent.message_length)
