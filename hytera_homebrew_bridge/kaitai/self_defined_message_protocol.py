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


class SelfDefinedMessageProtocol(KaitaiStruct):
    class ServiceTypes(Enum):
        private_work_order = 172
        private_work_order_ack = 173
        private_short_data = 174
        private_short_data_ack = 175
        group_work_order = 188
        group_work_order_ack = 189
        group_short_data = 190
        group_short_data_ack = 191

    class WorkStates(Enum):
        new = 0
        delete = 1
        decline = 16
        state_1 = 32
        state_2 = 33
        state_3 = 34
        state_4 = 35
        state_5 = 36

    class AckFlags(Enum):
        ack_required = 0
        ack_not_required = 1

    class OptionFlags(Enum):
        option_len_and_field_disabled = 0
        option_len_and_field_enabled = 1

    class ResultCodes(Enum):
        ok = 0
        fail = 1
        invalid_params = 3
        channel_busy = 4
        rx_only = 5
        low_battery = 6
        pll_unlock = 7
        private_call_no_ack = 8
        repeater_wakeup_fail = 9
        no_contact = 10
        tx_deny = 11
        tx_interrupted = 12

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ack_flag = KaitaiStream.resolve_enum(
            SelfDefinedMessageProtocol.AckFlags, self._io.read_bits_int_be(1)
        )
        self.option_flag = KaitaiStream.resolve_enum(
            SelfDefinedMessageProtocol.OptionFlags, self._io.read_bits_int_be(1)
        )
        self.reserved = self._io.read_bits_int_be(6)
        self._io.align_to_byte()
        self.service_type = KaitaiStream.resolve_enum(
            SelfDefinedMessageProtocol.ServiceTypes, self._io.read_u1()
        )
        self.message_length = self._io.read_u2be()
        if self.option_flag.value == 1:
            self.option_field_len = self._io.read_u2be()

        self.request_id = self._io.read_u4be()
        self.destination_ip = radio_ip.RadioIp(self._io)
        if self.is_ack_service != True:
            self.source_ip = radio_ip.RadioIp(self._io)

        if self.is_ack_service == True:
            self.result = KaitaiStream.resolve_enum(
                SelfDefinedMessageProtocol.ResultCodes, self._io.read_u1()
            )

        if (self.is_ack_service == False) and (self.is_work_order == True):
            self.work_order = SelfDefinedMessageProtocol.WorkOrder(
                self._io, self, self._root
            )

        if (self.is_ack_service == False) and (self.is_short_data == True):
            self.short_data = (self._io.read_bytes_term(0, False, True, True)).decode(
                u"UTF16-LE"
            )

        if self.option_flag.value == 1:
            self.option_field = (self._io.read_bytes(self.option_field_len)).decode(
                u"UTF16-LE"
            )

    class Date(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.year = self._io.read_u2be()
            self.month = self._io.read_u1()
            self.day = self._io.read_u1()

    class WorkOrder(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.work_order_header = self._io.read_bytes(4)
            if not self.work_order_header == b"\xFF\xFF\xFF\xFF":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\xFF\xFF\xFF\xFF",
                    self.work_order_header,
                    self._io,
                    u"/types/work_order/seq/0",
                )
            self.date = SelfDefinedMessageProtocol.Date(self._io, self, self._root)
            self.sequence_number = self._io.read_u4be()
            self.work_state = KaitaiStream.resolve_enum(
                SelfDefinedMessageProtocol.WorkStates, self._io.read_u2be()
            )
            self.reserved = self._io.read_bytes(38)
            self.contents = (self._io.read_bytes_term(0, False, True, True)).decode(
                u"UTF16-LE"
            )

    @property
    def is_ack_service(self):
        if hasattr(self, "_m_is_ack_service"):
            return (
                self._m_is_ack_service if hasattr(self, "_m_is_ack_service") else None
            )

        self._m_is_ack_service = (
            (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.private_work_order_ack
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.group_work_order_ack
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.private_short_data_ack
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.group_short_data_ack
            )
        )
        return self._m_is_ack_service if hasattr(self, "_m_is_ack_service") else None

    @property
    def is_work_order(self):
        if hasattr(self, "_m_is_work_order"):
            return self._m_is_work_order if hasattr(self, "_m_is_work_order") else None

        self._m_is_work_order = (
            (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.private_work_order
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.private_work_order_ack
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.group_work_order
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.group_work_order_ack
            )
        )
        return self._m_is_work_order if hasattr(self, "_m_is_work_order") else None

    @property
    def is_short_data(self):
        if hasattr(self, "_m_is_short_data"):
            return self._m_is_short_data if hasattr(self, "_m_is_short_data") else None

        self._m_is_short_data = (
            (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.private_short_data
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.private_short_data_ack
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.group_short_data
            )
            or (
                self.service_type
                == SelfDefinedMessageProtocol.ServiceTypes.group_short_data_ack
            )
        )
        return self._m_is_short_data if hasattr(self, "_m_is_short_data") else None
