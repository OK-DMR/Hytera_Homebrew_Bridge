-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")
local stringstream = require("string_stream")

-- 
-- TS 102 361-1 V2.5.1 Data Header
DmrDataHeader = class.class(KaitaiStruct)

DmrDataHeader.UdtFormats = enum.Enum {
  binary = 0,
  ms_or_tg_address = 1,
  bcd_4bit = 2,
  iso_7bit_coded_characters = 3,
  iso_8bit_coded_characters = 4,
  nmea_location_coded = 5,
  ip_address = 6,
  unicode_16bit_characters = 7,
  manufacturer_specific = 8,
  manufacturer_specific_2 = 9,
  mixed_address_and_16bit_utf16be_characters = 10,
}

DmrDataHeader.CsbkMbcUdtOpcodes = enum.Enum {
  c_aloha = 25,
  c_udthd = 26,
  c_udthu = 27,
  c_or_p_ahoy = 28,
  c_ackvit = 30,
  c_rand = 31,
  c_ackd = 32,
  c_acku = 33,
  p_ackd = 34,
  p_acku = 35,
  c_dgnahd = 36,
  c_dgnahu = 37,
  c_bcast = 40,
  p_maint = 42,
  p_clear = 46,
  p_protect = 47,
  pv_grant = 48,
  tv_grant = 49,
  btv_grant = 50,
  pd_grant = 51,
  td_grant = 52,
  pv_grant_dx = 53,
  pd_grant_dx = 54,
  pd_grant_mi = 55,
  td_grant_mi = 56,
  c_move = 57,
}

DmrDataHeader.DataPacketFormats = enum.Enum {
  unified_data_transport = 0,
  response_packet = 1,
  data_packet_unconfirmed = 2,
  data_packet_confirmed = 3,
  short_data_defined = 13,
  short_data_raw_or_status_or_precoded = 14,
  proprietary = 15,
}

DmrDataHeader.SapIdentifiers = enum.Enum {
  unified_data_transport = 0,
  tcp_ip_header_compression = 2,
  udp_ip_header_compression = 3,
  ip_based_packet_data = 4,
  arp_address_resolution_protocol = 5,
  proprietary_packet_data = 9,
  short_data = 10,
}

DmrDataHeader.DefinedDataFormats = enum.Enum {
  binary = 0,
  bcd = 1,
  coding_7bit = 2,
  coding_8bit_8859_1 = 3,
  coding_8bit_8859_2 = 4,
  coding_8bit_8859_3 = 5,
  coding_8bit_8859_4 = 6,
  coding_8bit_8859_5 = 7,
  coding_8bit_8859_6 = 8,
  coding_8bit_8859_7 = 9,
  coding_8bit_8859_8 = 10,
  coding_8bit_8859_9 = 11,
  coding_8bit_8859_10 = 12,
  coding_8bit_8859_11 = 13,
  coding_8bit_8859_13 = 14,
  coding_8bit_8859_14 = 15,
  coding_8bit_8859_15 = 16,
  coding_8bit_8859_16 = 17,
  unicode_utf8 = 18,
  unicode_utf16 = 19,
  unicode_utf16be = 20,
  unicode_utf16le = 21,
  unicode_utf32 = 22,
  unicode_utf32be = 23,
  unicode_utf32le = 24,
}

DmrDataHeader.ResponsePacketClasses = enum.Enum {
  ack = 0,
  nack = 1,
  sack = 2,
}

function DmrDataHeader:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader:_read()
  self.skip4 = self._io:read_bits_int_be(4)
  self.data_packet_format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
end

DmrDataHeader.property.data = {}
function DmrDataHeader.property.data:get()
  if self._m_data ~= nil then
    return self._m_data
  end

  local _io = self._root._io
  local _pos = _io:pos()
  _io:seek(0)
  local _on = self.data_packet_format
  if _on == DmrDataHeader.DataPacketFormats.proprietary then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataHeaderProprietary(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.short_data_defined then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataHeaderShortDefined(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.data_packet_unconfirmed then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataHeaderUnconfirmed(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.data_packet_confirmed then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataHeaderConfirmed(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.unified_data_transport then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataHeaderUdt(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.short_data_raw_or_status_precoded then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataHeaderShortStatusPrecoded(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.response_packet then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataHeaderResponse(_io, self, self._root)
  else
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataHeaderUndefined(_io, self, self._root)
  end
  _io:seek(_pos)
  return self._m_data
end

-- 
-- Data packet format / identification, section 9.3.17.

-- 
-- 9.2.11 Raw short data packet Header (R_HEAD) PDU.
DmrDataHeader.DataHeaderShortRaw = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderShortRaw:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderShortRaw:_read()
  self.llid_destination_is_group = self._io:read_bits_int_be(1)
  self.response_requested = self._io:read_bits_int_be(1)
  self.appended_blocks_msb = self._io:read_bits_int_be(2)
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.appended_blocks_lsb = self._io:read_bits_int_be(4)
  self.llid_destination = self._io:read_bits_int_be(24)
  self.llid_source = self._io:read_bits_int_be(24)
  self.source_port = self._io:read_bits_int_be(3)
  self.destination_port = self._io:read_bits_int_be(3)
  self.selective_automatic_repeat_request = self._io:read_bits_int_be(1)
  self.full_message_flag = self._io:read_bits_int_be(1)
  self.bit_padding = self._io:read_bits_int_be(8)
  self._io:align_to_byte()
  self.crc = self._io:read_bytes(2)
end

-- 
-- response demanded if destination is individual MS.
-- 
-- 0b00 expected.
-- 
-- 0b0000 expected.
-- 
-- flag whether source requires SARQ.
-- 
-- 0b00000000 expected.

-- 
-- 9.2.9 Proprietary Header (P_HEAD) PDU.
DmrDataHeader.DataHeaderProprietary = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderProprietary:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderProprietary:_read()
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.mfid = self._io:read_bits_int_be(8)
  self._io:align_to_byte()
  self.proprietary_data = self._io:read_bytes(8)
  self.crc = self._io:read_bytes(2)
end

-- 
-- manufacturer's id.
-- 
-- 64bits / 8bytes of proprietary data.

DmrDataHeader.DataHeaderUndefined = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderUndefined:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderUndefined:_read()
  self.bytedata = self._io:read_bytes_full()
end


-- 
-- 9.2.10 Status/Precoded short data packet Header (SP_HEAD) PDU.
DmrDataHeader.DataHeaderShortStatusPrecoded = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderShortStatusPrecoded:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderShortStatusPrecoded:_read()
  self.llid_destination_is_group = self._io:read_bits_int_be(1)
  self.response_requested = self._io:read_bits_int_be(1)
  self.appended_blocks_msb = self._io:read_bits_int_be(2)
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.appended_blocks_lsb = self._io:read_bits_int_be(4)
  self.llid_destination = self._io:read_bits_int_be(24)
  self.llid_source = self._io:read_bits_int_be(24)
  self.source_port = self._io:read_bits_int_be(3)
  self.destination_port = self._io:read_bits_int_be(3)
  self.status_precoded = self._io:read_bits_int_be(10)
  self._io:align_to_byte()
  self.crc = self._io:read_bytes(2)
end

-- 
-- response demanded if destination is individual MS.
-- 
-- 0b00 expected.
-- 
-- 0b0000 expected.

-- 
-- 9.2.4 Confirmed Response packet Header (C_RHEAD) PDU.
DmrDataHeader.DataHeaderResponse = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderResponse:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderResponse:_read()
  self.reserved1 = self._io:read_bits_int_be(1)
  self.response_requested = self._io:read_bits_int_be(1)
  self.reserved2 = self._io:read_bits_int_be(2)
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.reserved3 = self._io:read_bits_int_be(4)
  self.llid_destination = self._io:read_bits_int_be(24)
  self.llid_source = self._io:read_bits_int_be(24)
  self.full_message_flag = self._io:read_bits_int_be(1)
  self.blocks_to_follow = self._io:read_bits_int_be(7)
  self.response_class = DmrDataHeader.ResponsePacketClasses(self._io:read_bits_int_be(2))
  self.response_type = self._io:read_bits_int_be(3)
  self.response_status = self._io:read_bits_int_be(3)
  self._io:align_to_byte()
  self.crc = self._io:read_bytes(2)
end

-- 
-- 0b0 expected.
-- 
-- 0b0 expected.
-- 
-- 0b00 expected.
-- 
-- 0b0000 expected.
-- 
-- 0b0 expected.
-- 
-- NI/VI/FSN per ETSI TS 102 361-1 V2.5.1, Table 8.3 (page 87), Response Packet Class, Type, and Status definitions.

-- 
-- 9.2.1 Confirmed packet Header (C_HEAD) PDU.
DmrDataHeader.DataHeaderConfirmed = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderConfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderConfirmed:_read()
  self.llid_destination_is_group = self._io:read_bits_int_be(1)
  self.response_requested = self._io:read_bits_int_be(1)
  self.reserved1 = self._io:read_bits_int_be(1)
  self.pad_octet_count_msb = self._io:read_bits_int_be(1)
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.pad_octet_count = self._io:read_bits_int_be(4)
  self.llid_destination = self._io:read_bits_int_be(24)
  self.llid_source = self._io:read_bits_int_be(24)
  self.full_message_flag = self._io:read_bits_int_be(1)
  self.blocks_to_follow = self._io:read_bits_int_be(7)
  self.resynchronize_flag = self._io:read_bits_int_be(1)
  self.send_sequence_number = self._io:read_bits_int_be(3)
  self.fragment_sequence_number = self._io:read_bits_int_be(4)
  self._io:align_to_byte()
  self.crc = self._io:read_bytes(2)
end

-- 
-- response demanded if destination is individual MS.
-- 
-- 0b0 expected.

-- 
-- 9.2.6 Unconfirmed data packet Header (U_HEAD) PDU.
DmrDataHeader.DataHeaderUnconfirmed = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderUnconfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderUnconfirmed:_read()
  self.llid_destination_is_group = self._io:read_bits_int_be(1)
  self.response_requested = self._io:read_bits_int_be(1)
  self.reserved1 = self._io:read_bits_int_be(1)
  self.pad_octet_count_msb = self._io:read_bits_int_be(1)
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.pad_octet_count = self._io:read_bits_int_be(4)
  self.llid_destination = self._io:read_bits_int_be(24)
  self.llid_source = self._io:read_bits_int_be(24)
  self.full_message_flag = self._io:read_bits_int_be(1)
  self.blocks_to_follow = self._io:read_bits_int_be(7)
  self.reserved2 = self._io:read_bits_int_be(4)
  self.fragment_sequence_number = self._io:read_bits_int_be(4)
  self._io:align_to_byte()
  self.crc = self._io:read_bytes(2)
end

-- 
-- 0b0 expected.
-- 
-- 0b0 expected.
-- 
-- 0b0000 expected.

-- 
-- 9.2.12 Defined Data short data packet Header (DD_HEAD) PDU.
DmrDataHeader.DataHeaderShortDefined = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderShortDefined:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderShortDefined:_read()
  self.llid_destination_is_group = self._io:read_bits_int_be(1)
  self.response_requested = self._io:read_bits_int_be(1)
  self.appended_blocks_msb = self._io:read_bits_int_be(2)
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.appended_blocks_lsb = self._io:read_bits_int_be(4)
  self.llid_destination = self._io:read_bits_int_be(24)
  self.llid_source = self._io:read_bits_int_be(24)
  self.defined_data = DmrDataHeader.DefinedDataFormats(self._io:read_bits_int_be(6))
  self.selective_automatic_repeat_request = self._io:read_bits_int_be(1)
  self.full_message_flag = self._io:read_bits_int_be(1)
  self.bit_padding = self._io:read_bits_int_be(8)
  self._io:align_to_byte()
  self.crc = self._io:read_bytes(2)
end

-- 
-- response demanded if destination is individual MS.
-- 
-- 0b00 expected.
-- 
-- 0b0000 expected.
-- 
-- ETSI TS 102 361-1 V2.5.1, Table 9.50, DD information element content.
-- 
-- SARQ.

-- 
-- 9.2.13 Unified Data Transport Header (UDT_HEAD) PDU.
DmrDataHeader.DataHeaderUdt = class.class(KaitaiStruct)

function DmrDataHeader.DataHeaderUdt:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataHeaderUdt:_read()
  self.llid_destination_is_group = self._io:read_bits_int_be(1)
  self.response_requested = self._io:read_bits_int_be(1)
  self.reserved1 = self._io:read_bits_int_be(2)
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.udt_format = DmrDataHeader.UdtFormats(self._io:read_bits_int_be(4))
  self.llid_destination = self._io:read_bits_int_be(24)
  self.llid_source = self._io:read_bits_int_be(24)
  self.pad_nibble = self._io:read_bits_int_be(5)
  self.reserved2 = self._io:read_bits_int_be(1)
  self.appended_blocks = self._io:read_bits_int_be(2)
  self.supplementary_flag = self._io:read_bits_int_be(1)
  self.protect_flag = self._io:read_bits_int_be(1)
  self.udt_opcode = DmrDataHeader.CsbkMbcUdtOpcodes(self._io:read_bits_int_be(6))
  self._io:align_to_byte()
  self.crc = self._io:read_bytes(2)
end

-- 
-- 0b0 expected.
-- 
-- See ETSI TS 102 361-4 [11] clause 7.1.1.1.8 and 7.1.1.2.4 for information elements and values.
-- 
-- ETSI TS 102 361-4 V1.9.1, 7.2.27 UDT Format.
-- 
-- Number of Blocks appended to this UDT Header.
-- 
-- 0=>short data, 1=>supplementary data, ETSI TS 102 361-1 V2.5.1, 9.3.41 Supplementary Flag (SF).
-- 
-- ETSI TS 102 361-4 V1.10.1, Annex B, B.1 CSBK/MBC/UDT Opcode List.

