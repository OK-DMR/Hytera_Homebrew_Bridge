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
            DataTransmitProtocol.ServiceTypes, self._io.read_u1()
        )
        self.service_specific_type = KaitaiStream.resolve_enum(
            DataTransmitProtocol.ServiceSpecificTypes, self._io.read_u1()
        )
        self.message_length = self._io.read_u2be()
        _on = self.service_specific_type
        if _on == DataTransmitProtocol.ServiceSpecificTypes.dtp_request:
            self.data = DataTransmitProtocol.DtpRequest(self._io, self, self._root)
        elif _on == DataTransmitProtocol.ServiceSpecificTypes.data_slice_transmit:
            self.data = DataTransmitProtocol.DataSliceTransmit(
                self._io, self, self._root
            )
        elif _on == DataTransmitProtocol.ServiceSpecificTypes.data_slice_answer:
            self.data = DataTransmitProtocol.DataSliceAnswer(self._io, self, self._root)
        elif _on == DataTransmitProtocol.ServiceSpecificTypes.last_data_slice_answer:
            self.data = DataTransmitProtocol.LastDataSliceAnswer(
                self._io, self, self._root
            )
        elif _on == DataTransmitProtocol.ServiceSpecificTypes.dtp_answer:
            self.data = DataTransmitProtocol.DtpAnswer(self._io, self, self._root)
        elif _on == DataTransmitProtocol.ServiceSpecificTypes.last_data_slice:
            self.data = DataTransmitProtocol.LastDataSlice(self._io, self, self._root)

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
                DataTransmitProtocol.Results, self._io.read_u1()
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
                DataTransmitProtocol.Results, self._io.read_u1()
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
                DataTransmitProtocol.Results, self._io.read_u1()
            )
