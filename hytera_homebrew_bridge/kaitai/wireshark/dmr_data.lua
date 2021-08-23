-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")

-- 
-- ETSI TS 102 361-1 V2.5.1, section 9.2, Data PDUs
DmrData = class.class(KaitaiStruct)

function DmrData:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData:_read()
end


-- 
-- 9.2.16 Rate 1 coded Last Data block (R_1_LDATA) PDU, Table 9.18C: R_1_LDATA PDU content for unconfirmed data
DmrData.Rate1LastBlockUnconfirmed = class.class(KaitaiStruct)

function DmrData.Rate1LastBlockUnconfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate1LastBlockUnconfirmed:_read()
  self.user_data = self._io:read_bytes(20)
  self.message_crc32 = self._io:read_bytes(4)
end


-- 
-- 9.2.8 Rate ½ coded Last Data block (R_1_2_LDATA) PDU, Table 9.15B: R_1_2_LDATA PDU content for confirmed data
DmrData.Rate12LastBlockConfirmed = class.class(KaitaiStruct)

function DmrData.Rate12LastBlockConfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate12LastBlockConfirmed:_read()
  self.data_block_serial_number = self._io:read_bits_int_be(7)
  self.crc9 = self._io:read_bits_int_be(9)
  self._io:align_to_byte()
  self.user_data = self._io:read_bytes(6)
  self.message_crc32 = self._io:read_bytes(4)
end


-- 
-- 9.2.7 Rate ½ coded packet Data (R_1_2_DATA) PDU, Table 9.15A: R_1_2_DATA PDU content for confirmed data
DmrData.Rate12Confirmed = class.class(KaitaiStruct)

function DmrData.Rate12Confirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate12Confirmed:_read()
  self.data_block_serial_number = self._io:read_bits_int_be(7)
  self.crc9 = self._io:read_bits_int_be(9)
  self._io:align_to_byte()
  self.user_data = self._io:read_bytes(10)
end


-- 
-- 9.2.3 Rate ¾ coded Last Data block (R_3_4_LDATA) PDU, Table 9.12A: R_3_4_LDATA PDU content for unconfirmed data
DmrData.Rate34LastBlockUnconfirmed = class.class(KaitaiStruct)

function DmrData.Rate34LastBlockUnconfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate34LastBlockUnconfirmed:_read()
  self.user_data = self._io:read_bytes(14)
  self.message_crc32 = self._io:read_bytes(4)
end


-- 
-- 9.2.16 Rate 1 coded Last Data block (R_1_LDATA) PDU, Table 9.18B: R_1_LDATA PDU content for confirmed data
DmrData.Rate1LastBlockConfirmed = class.class(KaitaiStruct)

function DmrData.Rate1LastBlockConfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate1LastBlockConfirmed:_read()
  self.data_block_serial_number = self._io:read_bits_int_be(7)
  self.crc9 = self._io:read_bits_int_be(9)
  self._io:align_to_byte()
  self.user_data = self._io:read_bytes(18)
  self.message_crc32 = self._io:read_bytes(4)
end


-- 
-- 9.2.15 Rate 1 coded packet Data (R_1_DATA) PDU, Table 9.18A: R_1_DATA PDU content for unconfirmed data
DmrData.Rate1Unconfirmed = class.class(KaitaiStruct)

function DmrData.Rate1Unconfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate1Unconfirmed:_read()
  self.user_data = self._io:read_bytes(24)
end


-- 
-- 9.2.14 Unified Data Transport Last Data block (UDT_LDATA) PDU, Table 9.17E: UDT_LDATA PDU content
DmrData.UdtLastBlock = class.class(KaitaiStruct)

function DmrData.UdtLastBlock:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.UdtLastBlock:_read()
  self.user_data = self._io:read_bytes(10)
  self.message_crc16 = self._io:read_bytes(2)
end


-- 
-- 9.2.2 Rate ¾ coded packet Data (R_3_4_DATA) PDU, Table 9.11: R_3_4_DATA PDU content for confirmed data
DmrData.Rate34Confirmed = class.class(KaitaiStruct)

function DmrData.Rate34Confirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate34Confirmed:_read()
  self.data_block_serial_number = self._io:read_bits_int_be(7)
  self.crc9 = self._io:read_bits_int_be(9)
  self._io:align_to_byte()
  self.user_data = self._io:read_bytes(16)
end


-- 
-- 9.2.3 Rate ¾ coded Last Data block (R_3_4_LDATA) PDU, Table 9.12: R_3_4_LDATA PDU content for confirmed data
DmrData.Rate34LastBlockConfirmed = class.class(KaitaiStruct)

function DmrData.Rate34LastBlockConfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate34LastBlockConfirmed:_read()
  self.data_block_serial_number = self._io:read_bits_int_be(7)
  self.crc9 = self._io:read_bits_int_be(9)
  self._io:align_to_byte()
  self.user_data = self._io:read_bytes(12)
  self.message_crc32 = self._io:read_bytes(4)
end


-- 
-- 9.2.2 Rate ¾ coded packet Data (R_3_4_DATA) PDU, Table 9.11A: R_3_4_DATA PDU content for unconfirmed data
DmrData.Rate34Unconfirmed = class.class(KaitaiStruct)

function DmrData.Rate34Unconfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate34Unconfirmed:_read()
  self.user_data = self._io:read_bytes(18)
end


-- 
-- 9.2.8 Rate ½ coded Last Data block (R_1_2_LDATA) PDU, Table 9.15B: R_1_2_LDATA PDU content for confirmed data
DmrData.Rate12LastBlockUnconfirmed = class.class(KaitaiStruct)

function DmrData.Rate12LastBlockUnconfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate12LastBlockUnconfirmed:_read()
  self.user_data = self._io:read_bytes(8)
  self.message_crc32 = self._io:read_bytes(4)
end


-- 
-- 9.2.15 Rate 1 coded packet Data (R_1_DATA) PDU, Table 9.18: R_1_DATA PDU content for confirmed data
DmrData.Rate1Confirmed = class.class(KaitaiStruct)

function DmrData.Rate1Confirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate1Confirmed:_read()
  self.data_block_serial_number = self._io:read_bits_int_be(7)
  self.crc9 = self._io:read_bits_int_be(9)
  self._io:align_to_byte()
  self.user_data = self._io:read_bytes(22)
end


-- 
-- 9.2.7 Rate ½ coded packet Data (R_1_2_DATA) PDU, Table 9.15AA: R_1_2_DATA PDU content for unconfirmed data
DmrData.Rate12Unconfirmed = class.class(KaitaiStruct)

function DmrData.Rate12Unconfirmed:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrData.Rate12Unconfirmed:_read()
  self.user_data = self._io:read_bytes(12)
end


