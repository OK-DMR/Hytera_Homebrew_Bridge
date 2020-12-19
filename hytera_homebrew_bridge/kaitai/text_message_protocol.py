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


class TextMessageProtocol(KaitaiStruct):
    class AckFlags(Enum):
        ack_required = 0
        ack_not_required = 1

    class OptionFlags(Enum):
        option_len_and_field_disabled = 0
        option_len_and_field_enabled = 1

    class ServiceTypes(Enum):
        send_private_message = 161
        send_private_message_ack = 162
        send_group_message = 177
        send_group_message_ack = 178

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
            TextMessageProtocol.AckFlags, self._io.read_bits_int_be(1)
        )
        self.option_flag = KaitaiStream.resolve_enum(
            TextMessageProtocol.OptionFlags, self._io.read_bits_int_be(1)
        )
        self.reserved = self._io.read_bits_int_be(6)
        self._io.align_to_byte()
        self.service_type = KaitaiStream.resolve_enum(
            TextMessageProtocol.ServiceTypes, self._io.read_u1()
        )
        self.message_length = self._io.read_u2be()
        if self.option_flag.value == 1:
            self.option_field_len = self._io.read_u2be()

        self.request_id = self._io.read_u4be()
        self.destination_ip = radio_ip.RadioIp(self._io)
        if self.service_type != TextMessageProtocol.ServiceTypes.send_group_message_ack:
            self.source_ip = radio_ip.RadioIp(self._io)

        if (
            self.service_type
            == TextMessageProtocol.ServiceTypes.send_private_message_ack
        ) or (
            self.service_type == TextMessageProtocol.ServiceTypes.send_group_message_ack
        ):
            self.result = KaitaiStream.resolve_enum(
                TextMessageProtocol.ResultCodes, self._io.read_u1()
            )

        if (
            self.service_type == TextMessageProtocol.ServiceTypes.send_private_message
        ) or (self.service_type == TextMessageProtocol.ServiceTypes.send_group_message):
            self.tmdata = (self._io.read_bytes_term(0, False, True, True)).decode(
                u"UTF16-LE"
            )

        if self.option_flag.value == 1:
            self.option_field = (self._io.read_bytes(self.option_field_len)).decode(
                u"UTF16-LE"
            )
