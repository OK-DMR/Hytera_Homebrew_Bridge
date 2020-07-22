# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version("0.7"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s"
        % (ks_version)
    )

from kaitai import hytera_dmr_application_protocol


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
        self.header = (self._io.read_bytes(2)).decode(u"UTF-8")
        self.version = self._io.read_u1()
        self.reserved = self._io.read_bits_int(2)
        self.has_option = self._io.read_bits_int(1) != 0
        self.is_reject = self._io.read_bits_int(1) != 0
        self.is_close = self._io.read_bits_int(1) != 0
        self.is_connect = self._io.read_bits_int(1) != 0
        self.is_heartbeat = self._io.read_bits_int(1) != 0
        self.is_ack = self._io.read_bits_int(1) != 0
        self._io.align_to_byte()
        self.sequence_number = self._io.read_u2be()
        if (self.is_heartbeat == False) and (self.is_ack == False):
            self.options = []
            i = 0
            while True:
                _ = self._root.Option(self._io, self, self._root)
                self.options.append(_)
                if _.expect_more_options == False:
                    break
                i += 1

        if (self.has_option == True) or (self.is_ack == True):
            self.data = hytera_dmr_application_protocol.HyteraDmrApplicationProtocol(
                self._io
            )

    class Option(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.expect_more_options = self._io.read_bits_int(1) != 0
            self.command = KaitaiStream.resolve_enum(
                self._root.OptionCommands, self._io.read_bits_int(7)
            )
            self._io.align_to_byte()
            self.option_data_length = self._io.read_u1()
            self.option_payload = self._io.read_bytes(self.option_data_length)
