# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version("0.9"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s"
        % (kaitaistruct.__version__)
    )


class DmrData(KaitaiStruct):
    """ETSI TS 102 361-1 V2.5.1, section 9.2, Data PDUs"""

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass

    class Rate1LastBlockUnconfirmed(KaitaiStruct):
        """9.2.16 Rate 1 coded Last Data block (R_1_LDATA) PDU, Table 9.18C: R_1_LDATA PDU content for unconfirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.user_data = self._io.read_bytes(20)
            self.message_crc32 = self._io.read_bytes(4)

    class Rate12LastBlockConfirmed(KaitaiStruct):
        """9.2.8 Rate ½ coded Last Data block (R_1_2_LDATA) PDU, Table 9.15B: R_1_2_LDATA PDU content for confirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_block_serial_number = self._io.read_bits_int_be(7)
            self.crc9 = self._io.read_bits_int_be(9)
            self._io.align_to_byte()
            self.user_data = self._io.read_bytes(6)
            self.message_crc32 = self._io.read_bytes(4)

    class Rate12Confirmed(KaitaiStruct):
        """9.2.7 Rate ½ coded packet Data (R_1_2_DATA) PDU, Table 9.15A: R_1_2_DATA PDU content for confirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_block_serial_number = self._io.read_bits_int_be(7)
            self.crc9 = self._io.read_bits_int_be(9)
            self._io.align_to_byte()
            self.user_data = self._io.read_bytes(10)

    class Rate34LastBlockUnconfirmed(KaitaiStruct):
        """9.2.3 Rate ¾ coded Last Data block (R_3_4_LDATA) PDU, Table 9.12A: R_3_4_LDATA PDU content for unconfirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.user_data = self._io.read_bytes(14)
            self.message_crc32 = self._io.read_bytes(4)

    class Rate1LastBlockConfirmed(KaitaiStruct):
        """9.2.16 Rate 1 coded Last Data block (R_1_LDATA) PDU, Table 9.18B: R_1_LDATA PDU content for confirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_block_serial_number = self._io.read_bits_int_be(7)
            self.crc9 = self._io.read_bits_int_be(9)
            self._io.align_to_byte()
            self.user_data = self._io.read_bytes(18)
            self.message_crc32 = self._io.read_bytes(4)

    class Rate1Unconfirmed(KaitaiStruct):
        """9.2.15 Rate 1 coded packet Data (R_1_DATA) PDU, Table 9.18A: R_1_DATA PDU content for unconfirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.user_data = self._io.read_bytes(24)

    class UdtLastBlock(KaitaiStruct):
        """9.2.14 Unified Data Transport Last Data block (UDT_LDATA) PDU, Table 9.17E: UDT_LDATA PDU content"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.user_data = self._io.read_bytes(10)
            self.message_crc16 = self._io.read_bytes(2)

    class Rate34Confirmed(KaitaiStruct):
        """9.2.2 Rate ¾ coded packet Data (R_3_4_DATA) PDU, Table 9.11: R_3_4_DATA PDU content for confirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_block_serial_number = self._io.read_bits_int_be(7)
            self.crc9 = self._io.read_bits_int_be(9)
            self._io.align_to_byte()
            self.user_data = self._io.read_bytes(16)

    class Rate34LastBlockConfirmed(KaitaiStruct):
        """9.2.3 Rate ¾ coded Last Data block (R_3_4_LDATA) PDU, Table 9.12: R_3_4_LDATA PDU content for confirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_block_serial_number = self._io.read_bits_int_be(7)
            self.crc9 = self._io.read_bits_int_be(9)
            self._io.align_to_byte()
            self.user_data = self._io.read_bytes(12)
            self.message_crc32 = self._io.read_bytes(4)

    class Rate34Unconfirmed(KaitaiStruct):
        """9.2.2 Rate ¾ coded packet Data (R_3_4_DATA) PDU, Table 9.11A: R_3_4_DATA PDU content for unconfirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.user_data = self._io.read_bytes(18)

    class Rate12LastBlockUnconfirmed(KaitaiStruct):
        """9.2.8 Rate ½ coded Last Data block (R_1_2_LDATA) PDU, Table 9.15B: R_1_2_LDATA PDU content for confirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.user_data = self._io.read_bytes(8)
            self.message_crc32 = self._io.read_bytes(4)

    class Rate1Confirmed(KaitaiStruct):
        """9.2.15 Rate 1 coded packet Data (R_1_DATA) PDU, Table 9.18: R_1_DATA PDU content for confirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_block_serial_number = self._io.read_bits_int_be(7)
            self.crc9 = self._io.read_bits_int_be(9)
            self._io.align_to_byte()
            self.user_data = self._io.read_bytes(22)

    class Rate12Unconfirmed(KaitaiStruct):
        """9.2.7 Rate ½ coded packet Data (R_1_2_DATA) PDU, Table 9.15AA: R_1_2_DATA PDU content for unconfirmed data"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.user_data = self._io.read_bytes(12)
