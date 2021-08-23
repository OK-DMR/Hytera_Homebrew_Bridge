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

DmrDataHeader.UdtOpcodes = enum.Enum {
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
    self._m_data = DmrDataHeader.DataProprietary(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.short_data_defined then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataShortDefined(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.data_packet_unconfirmed then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataUnconfirmed(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.data_packet_confirmed then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataConfirmed(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.unified_data_transport then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataUdt(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.short_data_raw_or_status_precoded then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataShortStatusPrecoded(_io, self, self._root)
  elseif _on == DmrDataHeader.DataPacketFormats.response_packet then
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataResponse(_io, self, self._root)
  else
    self._raw__m_data = _io:read_bytes(12)
    local _io = KaitaiStream(stringstream(self._raw__m_data))
    self._m_data = DmrDataHeader.DataUndefined(_io, self, self._root)
  end
  _io:seek(_pos)
  return self._m_data
end

-- 
-- Data packet format / identification, section 9.3.17.

-- 
-- 9.2.4 Confirmed Response packet Header (C_RHEAD) PDU.
DmrDataHeader.DataResponse = class.class(KaitaiStruct)

function DmrDataHeader.DataResponse:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataResponse:_read()
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
  self.response_class = self._io:read_bits_int_be(2)
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
-- 9.2.9 Proprietary Header (P_HEAD) PDU.
DmrDataHeader.DataProprietary = class.class(KaitaiStruct)

function DmrDataHeader.DataProprietary:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataProprietary:_read()
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

-- 
-- 9.2.10 Status/Precoded short data packet Header (SP_HEAD) PDU.
DmrDataHeader.DataShortStatusPrecoded = class.class(KaitaiStruct)

function DmrDataHeader.DataShortStatusPrecoded:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataShortStatusPrecoded:_read()
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
-- 0b00 expected.
-- 
-- 0b0000 expected.

-- 
-- 9.2.1 Confirmed packet Header (C_HEAD) PDU.
DmrDataHeader.DataConfirmed = class.class(KaitaiStruct)

function DmrDataHeader.DataConfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataConfirmed:_read()
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
-- 0b0 expected.

DmrDataHeader.DataUndefined = class.class(KaitaiStruct)

function DmrDataHeader.DataUndefined:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataUndefined:_read()
  self.bytedata = self._io:read_bytes_full()
end


-- 
-- 9.2.6 Unconfirmed data packet Header (U_HEAD) PDU.
DmrDataHeader.DataUnconfirmed = class.class(KaitaiStruct)

function DmrDataHeader.DataUnconfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataUnconfirmed:_read()
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
-- 9.2.13 Unified Data Transport Header (UDT_HEAD) PDU.
DmrDataHeader.DataUdt = class.class(KaitaiStruct)

function DmrDataHeader.DataUdt:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataUdt:_read()
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
  self.udt_opcode = DmrDataHeader.UdtOpcodes(self._io:read_bits_int_be(6))
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
-- ETSI TS 102 361-4 V1.2.1, Annex B, B.1 CSBK/MBC/UDT Opcode List.

-- 
-- 9.2.11 Raw short data packet Header (R_HEAD) PDU.
DmrDataHeader.DataShortRaw = class.class(KaitaiStruct)

function DmrDataHeader.DataShortRaw:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataShortRaw:_read()
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
-- 0b00 expected.
-- 
-- 0b0000 expected.
-- 
-- SARQ.
-- 
-- 0b00000000 expected.

-- 
-- 9.2.12 Defined Data short data packet Header (DD_HEAD) PDU.
DmrDataHeader.DataShortDefined = class.class(KaitaiStruct)

function DmrDataHeader.DataShortDefined:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrDataHeader.DataShortDefined:_read()
  self.llid_destination_is_group = self._io:read_bits_int_be(1)
  self.response_requested = self._io:read_bits_int_be(1)
  self.appended_blocks_msb = self._io:read_bits_int_be(2)
  self.format = DmrDataHeader.DataPacketFormats(self._io:read_bits_int_be(4))
  self.sap_identifier = DmrDataHeader.SapIdentifiers(self._io:read_bits_int_be(4))
  self.appended_blocks_lsb = self._io:read_bits_int_be(4)
  self.llid_destination = self._io:read_bits_int_be(24)
  self.llid_source = self._io:read_bits_int_be(24)
  self.defined_data = self._io:read_bits_int_be(6)
  self.selective_automatic_repeat_request = self._io:read_bits_int_be(1)
  self.full_message_flag = self._io:read_bits_int_be(1)
  self.bit_padding = self._io:read_bits_int_be(8)
  self._io:align_to_byte()
  self.crc = self._io:read_bytes(2)
end

-- 
-- 0b00 expected.
-- 
-- 0b0000 expected.
-- 
-- data format.
-- 
-- SARQ.

