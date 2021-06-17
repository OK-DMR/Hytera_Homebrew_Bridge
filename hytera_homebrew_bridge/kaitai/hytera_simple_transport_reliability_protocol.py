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

from hytera_homebrew_bridge.kaitai import hytera_dmr_application_protocol


class HyteraSimpleTransportReliabilityProtocol(KaitaiStruct):
    class OptionCommands(Enum):
        realtime = 1
        device_id = 3
        channel_id = 4

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = self._io.read_bytes(2)
        if not self.header == b"\x32\x42":
            raise kaitaistruct.ValidationNotEqualError(
                b"\x32\x42", self.header, self._io, u"/seq/0"
            )
        self.version = self._io.read_u1()
        self.reserved = self._io.read_bits_int_be(2)
        self.has_option = self._io.read_bits_int_be(1) != 0
        self.is_reject = self._io.read_bits_int_be(1) != 0
        self.is_close = self._io.read_bits_int_be(1) != 0
        self.is_connect = self._io.read_bits_int_be(1) != 0
        self.is_heartbeat = self._io.read_bits_int_be(1) != 0
        self.is_ack = self._io.read_bits_int_be(1) != 0
        self._io.align_to_byte()
        self.sequence_number = self._io.read_u2be()
        if (not (self._io.is_eof())) and (not (self.is_heartbeat)):
            self.options = []
            i = 0
            while True:
                _ = HyteraSimpleTransportReliabilityProtocol.Option(
                    self._io, self, self._root
                )
                self.options.append(_)
                if not (_.expect_more_options):
                    break
                i += 1

        if (
            (not (self._io.is_eof()))
            and (self.has_option == True)
            and (not (self.is_reject))
            and (not (self.is_close))
            and (not (self.is_connect))
        ):
            self.data = []
            i = 0
            while not self._io.is_eof():
                self.data.append(
                    hytera_dmr_application_protocol.HyteraDmrApplicationProtocol(
                        self._io
                    )
                )
                i += 1

        if not (self._io.is_eof()):
            self.extra_data = self._io.read_bytes_full()

    class Option(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.expect_more_options = self._io.read_bits_int_be(1) != 0
            self.command = KaitaiStream.resolve_enum(
                HyteraSimpleTransportReliabilityProtocol.OptionCommands,
                self._io.read_bits_int_be(7),
            )
            self._io.align_to_byte()
            self.len_option_payload = self._io.read_u1()
            self.option_payload = self._io.read_bytes(self.len_option_payload)
