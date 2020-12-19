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


class TelemetryProtocol(KaitaiStruct):
    class ServiceTypes(Enum):
        status_report_service = 160
        remote_control_service = 176

    class ResultTypes(Enum):
        effective = 0
        ineffective = 1

    class CallTypes(Enum):
        private_call = 0
        group_call = 1
        all_call = 2

    class OperationTypes(Enum):
        set_ineffective_level = 0
        set_effective_level = 1
        reverse_level = 2
        output_one_pulse = 3

    class PcFlagTypes(Enum):
        controller_is_radio = 0
        controller_is_telemetry_application = 1

    class ServiceSpecificTypes(Enum):
        standard_status_request = 40961
        standard_status_report = 41089
        extended_status_report = 41090
        remote_control_request = 45057
        remote_control_answer = 45185

    class ControlResultTypes(Enum):
        success = 0
        failure = 1

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.service_type_opcode = KaitaiStream.resolve_enum(
            TelemetryProtocol.ServiceTypes, self._io.read_u1()
        )
        self.specific_service_opcode = self._io.read_u1()
        self.message_length = self._io.read_u2be()
        _on = self.specific_service
        if _on == TelemetryProtocol.ServiceSpecificTypes.standard_status_request:
            self.data = TelemetryProtocol.StandardStatusRequest(
                self._io, self, self._root
            )
        elif _on == TelemetryProtocol.ServiceSpecificTypes.remote_control_answer:
            self.data = TelemetryProtocol.RemoteControlAnswer(
                self._io, self, self._root
            )
        elif _on == TelemetryProtocol.ServiceSpecificTypes.extended_status_report:
            self.data = TelemetryProtocol.ExtendedStatusReport(
                self._io, self, self._root
            )
        elif _on == TelemetryProtocol.ServiceSpecificTypes.remote_control_request:
            self.data = TelemetryProtocol.RemoteControlRequest(
                self._io, self, self._root
            )
        elif _on == TelemetryProtocol.ServiceSpecificTypes.standard_status_report:
            self.data = TelemetryProtocol.StandardStatusReport(
                self._io, self, self._root
            )

    class StandardStatusReport(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.source_ip = radio_ip.RadioIp(self._io)
            self.target_ip = radio_ip.RadioIp(self._io)
            self.pc_flag = KaitaiStream.resolve_enum(
                TelemetryProtocol.PcFlagTypes, self._io.read_u1()
            )
            self.call_type = KaitaiStream.resolve_enum(
                TelemetryProtocol.CallTypes, self._io.read_u1()
            )
            self.vio_select = self._io.read_bytes(1)
            self.result = KaitaiStream.resolve_enum(
                TelemetryProtocol.ResultTypes, self._io.read_u1()
            )

    class VioExtendedStatus(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.result = KaitaiStream.resolve_enum(
                TelemetryProtocol.ResultTypes, self._io.read_u1()
            )
            self.message_length = self._io.read_u2be()
            self.message = (self._io.read_bytes(self.message_length)).decode(
                u"UTF16-LE"
            )

    class RemoteControlAnswer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.source_ip = radio_ip.RadioIp(self._io)
            self.target_ip = radio_ip.RadioIp(self._io)
            self.pc_flag = KaitaiStream.resolve_enum(
                TelemetryProtocol.PcFlagTypes, self._io.read_u1()
            )
            self.call_type = KaitaiStream.resolve_enum(
                TelemetryProtocol.CallTypes, self._io.read_u1()
            )
            self.vio_select = self._io.read_bytes(1)
            self.result = KaitaiStream.resolve_enum(
                TelemetryProtocol.ControlResultTypes, self._io.read_u1()
            )

    class RemoteControlRequest(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.source_ip = radio_ip.RadioIp(self._io)
            self.target_ip = radio_ip.RadioIp(self._io)
            self.pc_flag = KaitaiStream.resolve_enum(
                TelemetryProtocol.PcFlagTypes, self._io.read_u1()
            )
            self.call_type = KaitaiStream.resolve_enum(
                TelemetryProtocol.CallTypes, self._io.read_u1()
            )
            self.vio_select = self._io.read_bytes(1)
            self.operation = KaitaiStream.resolve_enum(
                TelemetryProtocol.OperationTypes, self._io.read_u1()
            )

    class ExtendedStatusReport(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.source_ip = radio_ip.RadioIp(self._io)
            self.target_ip = radio_ip.RadioIp(self._io)
            self.pc_flag = KaitaiStream.resolve_enum(
                TelemetryProtocol.PcFlagTypes, self._io.read_u1()
            )
            self.call_type = KaitaiStream.resolve_enum(
                TelemetryProtocol.CallTypes, self._io.read_u1()
            )
            self.vio_select = self._io.read_bytes(1)
            self.result_messages = TelemetryProtocol.VioExtendedStatus(
                self._io, self, self._root
            )

    class StandardStatusRequest(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.source_ip = radio_ip.RadioIp(self._io)
            self.target_ip = radio_ip.RadioIp(self._io)
            self.pc_flag = KaitaiStream.resolve_enum(
                TelemetryProtocol.PcFlagTypes, self._io.read_u1()
            )
            self.call_type = KaitaiStream.resolve_enum(
                TelemetryProtocol.CallTypes, self._io.read_u1()
            )
            self.vio_select = self._io.read_bytes(1)

    @property
    def specific_service(self):
        if hasattr(self, "_m_specific_service"):
            return (
                self._m_specific_service
                if hasattr(self, "_m_specific_service")
                else None
            )

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_specific_service = KaitaiStream.resolve_enum(
            TelemetryProtocol.ServiceSpecificTypes, self._io.read_u2be()
        )
        self._io.seek(_pos)
        return (
            self._m_specific_service if hasattr(self, "_m_specific_service") else None
        )
