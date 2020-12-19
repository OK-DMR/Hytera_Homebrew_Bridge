# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version("0.9"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s"
        % (kaitaistruct.__version__)
    )


class Homebrew(KaitaiStruct):
    """Homebrew DMR protocol, based on PDF (DL5DI, G4KLX, DG1HT 2015) specification"""

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.command_prefix = (self._io.read_bytes(4)).decode(u"UTF-8")
        _on = self.command_prefix
        if _on == u"RPTL":
            self.command_data = Homebrew.TypeRepeaterLoginRequest(
                self._io, self, self._root
            )
        elif _on == u"MSTA":
            self.command_data = Homebrew.TypeMasterRepeaterAck(
                self._io, self, self._root
            )
        elif _on == u"RPTK":
            self.command_data = Homebrew.TypeRepeaterLoginResponse(
                self._io, self, self._root
            )
        elif _on == u"RPTC":
            self.command_data = Homebrew.TypeRepeaterConfigurationOrClosing(
                self._io, self, self._root
            )
        elif _on == u"DMRD":
            self.command_data = Homebrew.TypeDmrData(self._io, self, self._root)
        elif _on == u"MSTC":
            self.command_data = Homebrew.TypeMasterClosing(self._io, self, self._root)
        elif _on == u"RPTP":
            self.command_data = Homebrew.TypeRepeaterPong(self._io, self, self._root)
        elif _on == u"MSTP":
            self.command_data = Homebrew.TypeMasterPing(self._io, self, self._root)
        elif _on == u"MSTN":
            self.command_data = Homebrew.TypeMasterNotAccept(self._io, self, self._root)

    class TypeMasterPing(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(3)
            if not self.magic == b"\x49\x4E\x47":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x49\x4E\x47",
                    self.magic,
                    self._io,
                    u"/types/type_master_ping/seq/0",
                )
            self.repeater_id = self._io.read_u4be()

    class TypeRepeaterPong(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(3)
            if not self.magic == b"\x4F\x4E\x47":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x4F\x4E\x47",
                    self.magic,
                    self._io,
                    u"/types/type_repeater_pong/seq/0",
                )
            self.repeater_id = self._io.read_u4be()

    class TypeRepeaterConfigurationOrClosing(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self._root.fifth_letter
            if _on == u"L":
                self.data = Homebrew.TypeRepeaterClosing(self._io, self, self._root)
            else:
                self.data = Homebrew.TypeRepeaterConfiguration(
                    self._io, self, self._root
                )

    class TypeRepeaterLoginResponse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.repeater_id = self._io.read_u4be()
            self.sha256 = self._io.read_bytes(32)

    class TypeRepeaterLoginRequest(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.repeater_id = self._io.read_u4be()

    class TypeMasterNotAccept(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(2)
            if not self.magic == b"\x41\x4B":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x41\x4B",
                    self.magic,
                    self._io,
                    u"/types/type_master_not_accept/seq/0",
                )
            self.repeater_id = self._io.read_u4be()

    class TypeMasterRepeaterAck(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magictype_master_repeater_ack = self._io.read_bytes(2)
            if not self.magictype_master_repeater_ack == b"\x43\x4B":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x43\x4B",
                    self.magictype_master_repeater_ack,
                    self._io,
                    u"/types/type_master_repeater_ack/seq/0",
                )
            self.repeater_id = self._io.read_u4be()
            if not (self._io.is_eof()):
                self.random_number = self._io.read_u4be()

    class TypeMasterClosing(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(1)
            if not self.magic == b"\x4C":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x4C", self.magic, self._io, u"/types/type_master_closing/seq/0"
                )
            self.repeater_id = self._io.read_u4be()

    class TypeDmrData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sequence_no = self._io.read_u1()
            self.source_id = self._io.read_bits_int_be(24)
            self.target_id = self._io.read_bits_int_be(24)
            self._io.align_to_byte()
            self.repeater_id = self._io.read_u4be()
            self.slot_no = self._io.read_bits_int_be(1) != 0
            self.call_type = self._io.read_bits_int_be(1) != 0
            self.frame_type = self._io.read_bits_int_be(2)
            self.data_type = self._io.read_bits_int_be(4)
            self._io.align_to_byte()
            self.stream_id = self._io.read_u4be()
            self.dmr_data = self._io.read_bytes(33)
            if not (self._io.is_eof()):
                self.bit_error_rate = self._io.read_u1()

            if not (self._io.is_eof()):
                self.rssi = self._io.read_u1()

    class TypeRepeaterOptions(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.repeater_id = self._io.read_u4be()
            self.options = (self._io.read_bytes_full()).decode(u"ASCII")

    class TypeRepeaterClosing(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(1)
            if not self.magic == b"\x4C":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x4C", self.magic, self._io, u"/types/type_repeater_closing/seq/0"
                )
            self.repeater_id = self._io.read_u4be()

    class TypeRepeaterConfiguration(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.repeater_id = self._io.read_u4be()
            self.call_sign = (self._io.read_bytes(8)).decode(u"ASCII")
            self.rx_freq = (self._io.read_bytes(9)).decode(u"ASCII")
            self.tx_freq = (self._io.read_bytes(9)).decode(u"ASCII")
            self.tx_power = (self._io.read_bytes(2)).decode(u"ASCII")
            self.color_code = (self._io.read_bytes(2)).decode(u"ASCII")
            self.latitude = (self._io.read_bytes(8)).decode(u"ASCII")
            self.longitude = (self._io.read_bytes(9)).decode(u"ASCII")
            self.antenna_height_above_ground = (self._io.read_bytes(3)).decode(u"ASCII")
            self.location = (self._io.read_bytes(20)).decode(u"ASCII")
            self.description = (self._io.read_bytes(20)).decode(u"ASCII")
            self.url = (self._io.read_bytes(124)).decode(u"ASCII")
            self.software_id = (self._io.read_bytes(40)).decode(u"ASCII")
            self.package_id = (self._io.read_bytes(40)).decode(u"ASCII")
            self.unparsed_data = (self._io.read_bytes_full()).decode(u"ASCII")

    @property
    def fifth_letter(self):
        if hasattr(self, "_m_fifth_letter"):
            return self._m_fifth_letter if hasattr(self, "_m_fifth_letter") else None

        _pos = self._io.pos()
        self._io.seek(4)
        self._m_fifth_letter = (self._io.read_bytes(1)).decode(u"ASCII")
        self._io.seek(_pos)
        return self._m_fifth_letter if hasattr(self, "_m_fifth_letter") else None
