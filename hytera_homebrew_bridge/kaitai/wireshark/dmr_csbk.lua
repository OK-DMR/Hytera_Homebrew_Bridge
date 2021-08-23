-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

-- 
-- TS 102 361-2 V2.3.1 CSBK decoding
DmrCsbk = class.class(KaitaiStruct)

DmrCsbk.CsbkoTypes = enum.Enum {
  unit_to_unit_voice_service_request = 4,
  unit_to_unit_voice_service_answer_response = 5,
  channel_timing = 7,
  negative_acknowledge_response = 38,
  bs_outbound_activation_csbk_pdu = 56,
  preamble = 61,
}

DmrCsbk.CsbkDataOrCsbk = enum.Enum {
  csbk_content_follows_preambles = 0,
  data_content_follows_preambles = 1,
}

DmrCsbk.CsbkGroupOrIndividual = enum.Enum {
  target_address_is_an_individual = 0,
  target_address_is_a_group = 1,
}

function DmrCsbk:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrCsbk:_read()
  self.last_block = self._io:read_bits_int_be(1)
  self.protect_flag = self._io:read_bits_int_be(1)
  self.csbk_opcode = DmrCsbk.CsbkoTypes(self._io:read_bits_int_be(6))
  self.feature_set_id = self._io:read_bits_int_be(8)
  if self.csbk_opcode == DmrCsbk.CsbkoTypes.preamble then
    self.preamble_data_or_csbk = DmrCsbk.CsbkDataOrCsbk(self._io:read_bits_int_be(1))
  end
  if self.csbk_opcode == DmrCsbk.CsbkoTypes.preamble then
    self.preamble_group_or_individual = DmrCsbk.CsbkGroupOrIndividual(self._io:read_bits_int_be(1))
  end
  self.preamble_reserved_1 = self._io:read_bits_int_be(6)
  self.preamble_csbk_blocks_to_follow = self._io:read_bits_int_be(8)
  self.preamble_target_address = self._io:read_bits_int_be(24)
  self.preamble_source_address = self._io:read_bits_int_be(24)
end

-- 
-- LB.
-- 
-- PF.
-- 
-- CSBKO.
-- 
-- FID.

