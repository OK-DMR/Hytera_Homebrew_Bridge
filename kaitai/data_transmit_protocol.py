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


class DataTransmitProtocol(KaitaiStruct):
    class ServiceTypes(Enum):
        data_transmit_protocol = 160

    class ServiceSpecificTypes(Enum):
        dtp_request = 1
        data_slice_trasmit = 2
        last_data_slice = 3
        dtp_answer = 17
        data_slice_answer = 18
        last_data_slice_answer = 19

    class Results(Enum):
        success = 0
        failure = 1

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.service_type = KaitaiStream.resolve_enum(
            self._root.ServiceTypes, self._io.read_u1()
        )
        self.service_specific_type = KaitaiStream.resolve_enum(
            self._root.ServiceSpecificTypes, self._io.read_u1()
        )
        self.message_length = self._io.read_u2be()
        _on = self.service_specific_type
        if _on == self._root.ServiceSpecificTypes.dtp_request:
            self.data = self._root.DtpRequest(self._io, self, self._root)
        elif _on == self._root.ServiceSpecificTypes.data_slice_transmit:
            self.data = self._root.DataSliceTransmit(self._io, self, self._root)
        elif _on == self._root.ServiceSpecificTypes.data_slice_answer:
            self.data = self._root.DataSliceAnswer(self._io, self, self._root)
        elif _on == self._root.ServiceSpecificTypes.last_data_slice_answer:
            self.data = self._root.LastDataSliceAnswer(self._io, self, self._root)
        elif _on == self._root.ServiceSpecificTypes.dtp_answer:
            self.data = self._root.DtpAnswer(self._io, self, self._root)
        elif _on == self._root.ServiceSpecificTypes.last_data_slice:
            self.data = self._root.LastDataSlice(self._io, self, self._root)

    class LastDataSlice(KaitaiStruct):
        """sent by transmit source, requires answer from the destination."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.destination_ip = radio_ip.RadioIp(self._io)
            self.source_ip = radio_ip.RadioIp(self._io)

    class DtpRequest(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.destination_ip = radio_ip.RadioIp(self._io)
            self.source_ip = radio_ip.RadioIp(self._io)
            self.file_size = self._io.read_u2be()
            self.file_name = (
                self._io.read_bytes((self._parent.message_length - 10))
            ).decode(u"UTF16-LE")

    class DataSliceAnswer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.destination_ip = radio_ip.RadioIp(self._io)
            self.source_ip = radio_ip.RadioIp(self._io)
            self.block_number = self._io.read_u2be()
            self.result = KaitaiStream.resolve_enum(
                self._root.Results, self._io.read_u1()
            )

    class DataSliceTransmit(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.destination_ip = radio_ip.RadioIp(self._io)
            self.source_ip = radio_ip.RadioIp(self._io)
            self.block_number = self._io.read_u2be()
            self.file_data = self._io.read_bytes((self._parent.message_length - 10))

    class LastDataSliceAnswer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.destination_ip = radio_ip.RadioIp(self._io)
            self.source_ip = radio_ip.RadioIp(self._io)
            self.result = KaitaiStream.resolve_enum(
                self._root.Results, self._io.read_u1()
            )

    class DtpAnswer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.destination_ip = radio_ip.RadioIp(self._io)
            self.source_ip = radio_ip.RadioIp(self._io)
            self.result = KaitaiStream.resolve_enum(
                self._root.Results, self._io.read_u1()
            )
