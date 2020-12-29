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


class DataDeliveryStates(KaitaiStruct):
    class StateTypes(Enum):
        location_protocol_state = 8
        radio_registration_service_state = 17
        telemetry_protocol_state = 18
        data_transmit_protocol_state = 19

    class Results(Enum):
        ok = 0
        fail = 1
        limited_timeout = 4
        no_ack = 5
        error_ack = 6
        repeater_wakeup_fail = 7
        tx_interrupted = 8
        tx_deny = 9
        invalid_params = 10

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.reserved = self._io.read_bytes(1)
        self.state_type = KaitaiStream.resolve_enum(
            DataDeliveryStates.StateTypes, self._io.read_u1()
        )
        self.message_length = self._io.read_u2be()
        self.radio_ip = radio_ip.RadioIp(self._io)
        self.protocol_opcode = self._io.read_u2be()
        self.result = KaitaiStream.resolve_enum(
            DataDeliveryStates.Results, self._io.read_u1()
        )
