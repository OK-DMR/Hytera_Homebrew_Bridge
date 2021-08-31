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


class DmrDataHeader(KaitaiStruct):
    """TS 102 361-1 V2.5.1 Data Header"""

    class UdtFormats(Enum):
        binary = 0
        ms_or_tg_address = 1
        bcd_4bit = 2
        iso_7bit_coded_characters = 3
        iso_8bit_coded_characters = 4
        nmea_location_coded = 5
        ip_address = 6
        unicode_16bit_characters = 7
        manufacturer_specific = 8
        manufacturer_specific_2 = 9
        mixed_address_and_16bit_utf16be_characters = 10

    class CsbkMbcUdtOpcodes(Enum):
        c_aloha = 25
        c_udthd = 26
        c_udthu = 27
        c_or_p_ahoy = 28
        c_ackvit = 30
        c_rand = 31
        c_ackd = 32
        c_acku = 33
        p_ackd = 34
        p_acku = 35
        c_dgnahd = 36
        c_dgnahu = 37
        c_bcast = 40
        p_maint = 42
        p_clear = 46
        p_protect = 47
        pv_grant = 48
        tv_grant = 49
        btv_grant = 50
        pd_grant = 51
        td_grant = 52
        pv_grant_dx = 53
        pd_grant_dx = 54
        pd_grant_mi = 55
        td_grant_mi = 56
        c_move = 57

    class DataPacketFormats(Enum):
        unified_data_transport = 0
        response_packet = 1
        data_packet_unconfirmed = 2
        data_packet_confirmed = 3
        short_data_defined = 13
        short_data_raw_or_status_or_precoded = 14
        proprietary = 15

    class SapIdentifiers(Enum):
        unified_data_transport = 0
        tcp_ip_header_compression = 2
        udp_ip_header_compression = 3
        ip_based_packet_data = 4
        arp_address_resolution_protocol = 5
        proprietary_packet_data = 9
        short_data = 10

    class DefinedDataFormats(Enum):
        binary = 0
        bcd = 1
        coding_7bit = 2
        coding_8bit_8859_1 = 3
        coding_8bit_8859_2 = 4
        coding_8bit_8859_3 = 5
        coding_8bit_8859_4 = 6
        coding_8bit_8859_5 = 7
        coding_8bit_8859_6 = 8
        coding_8bit_8859_7 = 9
        coding_8bit_8859_8 = 10
        coding_8bit_8859_9 = 11
        coding_8bit_8859_10 = 12
        coding_8bit_8859_11 = 13
        coding_8bit_8859_13 = 14
        coding_8bit_8859_14 = 15
        coding_8bit_8859_15 = 16
        coding_8bit_8859_16 = 17
        unicode_utf8 = 18
        unicode_utf16 = 19
        unicode_utf16be = 20
        unicode_utf16le = 21
        unicode_utf32 = 22
        unicode_utf32be = 23
        unicode_utf32le = 24

    class ResponsePacketClasses(Enum):
        ack = 0
        nack = 1
        sack = 2

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.skip4 = self._io.read_bits_int_be(4)
        self.data_packet_format = KaitaiStream.resolve_enum(
            DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
        )

    class DataHeaderShortRaw(KaitaiStruct):
        """9.2.11 Raw short data packet Header (R_HEAD) PDU."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.llid_destination_is_group = self._io.read_bits_int_be(1) != 0
            self.response_requested = self._io.read_bits_int_be(1) != 0
            self.appended_blocks_msb = self._io.read_bits_int_be(2)
            self.format = KaitaiStream.resolve_enum(
                DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
            )
            self.sap_identifier = KaitaiStream.resolve_enum(
                DmrDataHeader.SapIdentifiers, self._io.read_bits_int_be(4)
            )
            self.appended_blocks_lsb = self._io.read_bits_int_be(4)
            self.llid_destination = self._io.read_bits_int_be(24)
            self.llid_source = self._io.read_bits_int_be(24)
            self.source_port = self._io.read_bits_int_be(3)
            self.destination_port = self._io.read_bits_int_be(3)
            self.selective_automatic_repeat_request = self._io.read_bits_int_be(1) != 0
            self.full_message_flag = self._io.read_bits_int_be(1) != 0
            self.bit_padding = self._io.read_bits_int_be(8)
            self._io.align_to_byte()
            self.crc = self._io.read_bytes(2)

    class DataHeaderProprietary(KaitaiStruct):
        """9.2.9 Proprietary Header (P_HEAD) PDU."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sap_identifier = KaitaiStream.resolve_enum(
                DmrDataHeader.SapIdentifiers, self._io.read_bits_int_be(4)
            )
            self.format = KaitaiStream.resolve_enum(
                DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
            )
            self.mfid = self._io.read_bits_int_be(8)
            self._io.align_to_byte()
            self.proprietary_data = self._io.read_bytes(8)
            self.crc = self._io.read_bytes(2)

    class DataHeaderUndefined(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.bytedata = self._io.read_bytes_full()

    class DataHeaderShortStatusPrecoded(KaitaiStruct):
        """9.2.10 Status/Precoded short data packet Header (SP_HEAD) PDU."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.llid_destination_is_group = self._io.read_bits_int_be(1) != 0
            self.response_requested = self._io.read_bits_int_be(1) != 0
            self.appended_blocks_msb = self._io.read_bits_int_be(2)
            self.format = KaitaiStream.resolve_enum(
                DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
            )
            self.sap_identifier = KaitaiStream.resolve_enum(
                DmrDataHeader.SapIdentifiers, self._io.read_bits_int_be(4)
            )
            self.appended_blocks_lsb = self._io.read_bits_int_be(4)
            self.llid_destination = self._io.read_bits_int_be(24)
            self.llid_source = self._io.read_bits_int_be(24)
            self.source_port = self._io.read_bits_int_be(3)
            self.destination_port = self._io.read_bits_int_be(3)
            self.status_precoded = self._io.read_bits_int_be(10)
            self._io.align_to_byte()
            self.crc = self._io.read_bytes(2)

    class DataHeaderResponse(KaitaiStruct):
        """9.2.4 Confirmed Response packet Header (C_RHEAD) PDU."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved1 = self._io.read_bits_int_be(1) != 0
            self.response_requested = self._io.read_bits_int_be(1) != 0
            self.reserved2 = self._io.read_bits_int_be(2)
            self.format = KaitaiStream.resolve_enum(
                DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
            )
            self.sap_identifier = KaitaiStream.resolve_enum(
                DmrDataHeader.SapIdentifiers, self._io.read_bits_int_be(4)
            )
            self.reserved3 = self._io.read_bits_int_be(4)
            self.llid_destination = self._io.read_bits_int_be(24)
            self.llid_source = self._io.read_bits_int_be(24)
            self.full_message_flag = self._io.read_bits_int_be(1) != 0
            self.blocks_to_follow = self._io.read_bits_int_be(7)
            self.response_class = KaitaiStream.resolve_enum(
                DmrDataHeader.ResponsePacketClasses, self._io.read_bits_int_be(2)
            )
            self.response_type = self._io.read_bits_int_be(3)
            self.response_status = self._io.read_bits_int_be(3)
            self._io.align_to_byte()
            self.crc = self._io.read_bytes(2)

    class DataHeaderConfirmed(KaitaiStruct):
        """9.2.1 Confirmed packet Header (C_HEAD) PDU."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.llid_destination_is_group = self._io.read_bits_int_be(1) != 0
            self.response_requested = self._io.read_bits_int_be(1) != 0
            self.reserved1 = self._io.read_bits_int_be(1) != 0
            self.pad_octet_count_msb = self._io.read_bits_int_be(1) != 0
            self.format = KaitaiStream.resolve_enum(
                DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
            )
            self.sap_identifier = KaitaiStream.resolve_enum(
                DmrDataHeader.SapIdentifiers, self._io.read_bits_int_be(4)
            )
            self.pad_octet_count = self._io.read_bits_int_be(4)
            self.llid_destination = self._io.read_bits_int_be(24)
            self.llid_source = self._io.read_bits_int_be(24)
            self.full_message_flag = self._io.read_bits_int_be(1) != 0
            self.blocks_to_follow = self._io.read_bits_int_be(7)
            self.resynchronize_flag = self._io.read_bits_int_be(1) != 0
            self.send_sequence_number = self._io.read_bits_int_be(3)
            self.fragment_sequence_number = self._io.read_bits_int_be(4)
            self._io.align_to_byte()
            self.crc = self._io.read_bytes(2)

    class DataHeaderUnconfirmed(KaitaiStruct):
        """9.2.6 Unconfirmed data packet Header (U_HEAD) PDU."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.llid_destination_is_group = self._io.read_bits_int_be(1) != 0
            self.response_requested = self._io.read_bits_int_be(1) != 0
            self.reserved1 = self._io.read_bits_int_be(1) != 0
            self.pad_octet_count_msb = self._io.read_bits_int_be(1) != 0
            self.format = KaitaiStream.resolve_enum(
                DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
            )
            self.sap_identifier = KaitaiStream.resolve_enum(
                DmrDataHeader.SapIdentifiers, self._io.read_bits_int_be(4)
            )
            self.pad_octet_count = self._io.read_bits_int_be(4)
            self.llid_destination = self._io.read_bits_int_be(24)
            self.llid_source = self._io.read_bits_int_be(24)
            self.full_message_flag = self._io.read_bits_int_be(1) != 0
            self.blocks_to_follow = self._io.read_bits_int_be(7)
            self.reserved2 = self._io.read_bits_int_be(4)
            self.fragment_sequence_number = self._io.read_bits_int_be(4)
            self._io.align_to_byte()
            self.crc = self._io.read_bytes(2)

    class DataHeaderShortDefined(KaitaiStruct):
        """9.2.12 Defined Data short data packet Header (DD_HEAD) PDU."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.llid_destination_is_group = self._io.read_bits_int_be(1) != 0
            self.response_requested = self._io.read_bits_int_be(1) != 0
            self.appended_blocks_msb = self._io.read_bits_int_be(2)
            self.format = KaitaiStream.resolve_enum(
                DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
            )
            self.sap_identifier = KaitaiStream.resolve_enum(
                DmrDataHeader.SapIdentifiers, self._io.read_bits_int_be(4)
            )
            self.appended_blocks_lsb = self._io.read_bits_int_be(4)
            self.llid_destination = self._io.read_bits_int_be(24)
            self.llid_source = self._io.read_bits_int_be(24)
            self.defined_data = KaitaiStream.resolve_enum(
                DmrDataHeader.DefinedDataFormats, self._io.read_bits_int_be(6)
            )
            self.selective_automatic_repeat_request = self._io.read_bits_int_be(1) != 0
            self.full_message_flag = self._io.read_bits_int_be(1) != 0
            self.bit_padding = self._io.read_bits_int_be(8)
            self._io.align_to_byte()
            self.crc = self._io.read_bytes(2)

    class DataHeaderUdt(KaitaiStruct):
        """9.2.13 Unified Data Transport Header (UDT_HEAD) PDU."""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.llid_destination_is_group = self._io.read_bits_int_be(1) != 0
            self.response_requested = self._io.read_bits_int_be(1) != 0
            self.reserved1 = self._io.read_bits_int_be(2)
            self.format = KaitaiStream.resolve_enum(
                DmrDataHeader.DataPacketFormats, self._io.read_bits_int_be(4)
            )
            self.sap_identifier = KaitaiStream.resolve_enum(
                DmrDataHeader.SapIdentifiers, self._io.read_bits_int_be(4)
            )
            self.udt_format = KaitaiStream.resolve_enum(
                DmrDataHeader.UdtFormats, self._io.read_bits_int_be(4)
            )
            self.llid_destination = self._io.read_bits_int_be(24)
            self.llid_source = self._io.read_bits_int_be(24)
            self.pad_nibble = self._io.read_bits_int_be(5)
            self.reserved2 = self._io.read_bits_int_be(1) != 0
            self.appended_blocks = self._io.read_bits_int_be(2)
            self.supplementary_flag = self._io.read_bits_int_be(1) != 0
            self.protect_flag = self._io.read_bits_int_be(1) != 0
            self.udt_opcode = KaitaiStream.resolve_enum(
                DmrDataHeader.CsbkMbcUdtOpcodes, self._io.read_bits_int_be(6)
            )
            self._io.align_to_byte()
            self.crc = self._io.read_bytes(2)

    @property
    def data(self):
        if hasattr(self, "_m_data"):
            return self._m_data if hasattr(self, "_m_data") else None

        io = self._root._io
        _pos = io.pos()
        io.seek(0)
        _on = self.data_packet_format
        if _on == DmrDataHeader.DataPacketFormats.proprietary:
            self._raw__m_data = io.read_bytes(12)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = DmrDataHeader.DataHeaderProprietary(
                _io__raw__m_data, self, self._root
            )
        elif _on == DmrDataHeader.DataPacketFormats.short_data_defined:
            self._raw__m_data = io.read_bytes(12)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = DmrDataHeader.DataHeaderShortDefined(
                _io__raw__m_data, self, self._root
            )
        elif _on == DmrDataHeader.DataPacketFormats.data_packet_unconfirmed:
            self._raw__m_data = io.read_bytes(12)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = DmrDataHeader.DataHeaderUnconfirmed(
                _io__raw__m_data, self, self._root
            )
        elif _on == DmrDataHeader.DataPacketFormats.data_packet_confirmed:
            self._raw__m_data = io.read_bytes(12)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = DmrDataHeader.DataHeaderConfirmed(
                _io__raw__m_data, self, self._root
            )
        elif _on == DmrDataHeader.DataPacketFormats.unified_data_transport:
            self._raw__m_data = io.read_bytes(12)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = DmrDataHeader.DataHeaderUdt(
                _io__raw__m_data, self, self._root
            )
        elif (
            _on == DmrDataHeader.DataPacketFormats.short_data_raw_or_status_or_precoded
        ):
            self._raw__m_data = io.read_bytes(12)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = DmrDataHeader.DataHeaderShortStatusPrecoded(
                _io__raw__m_data, self, self._root
            )
        elif _on == DmrDataHeader.DataPacketFormats.response_packet:
            self._raw__m_data = io.read_bytes(12)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = DmrDataHeader.DataHeaderResponse(
                _io__raw__m_data, self, self._root
            )
        else:
            self._raw__m_data = io.read_bytes(12)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = DmrDataHeader.DataHeaderUndefined(
                _io__raw__m_data, self, self._root
            )
        io.seek(_pos)
        return self._m_data if hasattr(self, "_m_data") else None
