-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

-- 
-- ETSI TS 102 361-2 V2.4.1 (2017-10), Section 7.1.1
LinkControl = class.class(KaitaiStruct)

LinkControl.Flcos = enum.Enum {
  group_voice = 0,
  unit_to_unit_voice = 3,
  talker_alias_header = 4,
  talker_alias_block1 = 5,
  talker_alias_block2 = 6,
  talker_alias_block3 = 7,
  gps_info = 8,
}

LinkControl.PositionErrors = enum.Enum {
  less_than_2m = 0,
  less_than_20m = 1,
  less_than_200m = 2,
  less_than_2km = 3,
  less_than_20km = 4,
  less_than_or_equal_200km = 5,
  more_than_200km = 6,
  position_error_unknown_or_invalid = 7,
}

LinkControl.TalkerDataFormats = enum.Enum {
  coding_7bit = 0,
  coding_8bit = 1,
  unicode_utf8 = 2,
  unicode_utf16 = 3,
}

function LinkControl:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LinkControl:_read()
  self.protect_flag = self._io:read_bits_int_be(1)
  self.reserved = self._io:read_bits_int_be(1)
  self.full_link_control_opcode = LinkControl.Flcos(self._io:read_bits_int_be(6))
  self._io:align_to_byte()
  local _on = self.full_link_control_opcode
  if _on == LinkControl.Flcos.talker_alias_header then
    self.specific_data = LinkControl.TalkerAliasHeader(self._io, self, self._root)
  elseif _on == LinkControl.Flcos.unit_to_unit_voice then
    self.specific_data = LinkControl.UnitToUnitVoiceChannelUser(self._io, self, self._root)
  elseif _on == LinkControl.Flcos.group_voice then
    self.specific_data = LinkControl.GroupVoiceChannelUser(self._io, self, self._root)
  elseif _on == LinkControl.Flcos.talker_alias_block3 then
    self.specific_data = LinkControl.TalkerAliasContinuation(self._io, self, self._root)
  elseif _on == LinkControl.Flcos.talker_alias_block1 then
    self.specific_data = LinkControl.TalkerAliasContinuation(self._io, self, self._root)
  elseif _on == LinkControl.Flcos.talker_alias_block2 then
    self.specific_data = LinkControl.TalkerAliasContinuation(self._io, self, self._root)
  elseif _on == LinkControl.Flcos.gps_info then
    self.specific_data = LinkControl.GpsInfoLcPdu(self._io, self, self._root)
  end
end


LinkControl.GpsInfoLcPdu = class.class(KaitaiStruct)

function LinkControl.GpsInfoLcPdu:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LinkControl.GpsInfoLcPdu:_read()
  self.reserved = self._io:read_bits_int_be(4)
  self.position_error = LinkControl.PositionErrors(self._io:read_bits_int_be(3))
  self.longitude = self._io:read_bits_int_be(25)
  self.latitude = self._io:read_bits_int_be(24)
end


LinkControl.GroupVoiceChannelUser = class.class(KaitaiStruct)

function LinkControl.GroupVoiceChannelUser:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LinkControl.GroupVoiceChannelUser:_read()
  self.service_options = self._io:read_bits_int_be(8)
  self.group_address = self._io:read_bits_int_be(24)
  self.source_address = self._io:read_bits_int_be(24)
end


LinkControl.UnitToUnitVoiceChannelUser = class.class(KaitaiStruct)

function LinkControl.UnitToUnitVoiceChannelUser:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LinkControl.UnitToUnitVoiceChannelUser:_read()
  self.service_options = self._io:read_bits_int_be(8)
  self.target_address = self._io:read_bits_int_be(24)
  self.source_address = self._io:read_bits_int_be(24)
end


LinkControl.TalkerAliasHeader = class.class(KaitaiStruct)

function LinkControl.TalkerAliasHeader:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LinkControl.TalkerAliasHeader:_read()
  self.talker_alias_data_format = LinkControl.TalkerDataFormats(self._io:read_bits_int_be(2))
  self.talker_alias_data_length = self._io:read_bits_int_be(5)
  self.talker_alias_data = self._io:read_bits_int_be(49)
end

-- 
-- 8-bit/16-bit coded => 1st bit reserved (6 or 3 characters), 7-bit coded => all used (7 characters).

LinkControl.TalkerAliasContinuation = class.class(KaitaiStruct)

function LinkControl.TalkerAliasContinuation:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LinkControl.TalkerAliasContinuation:_read()
  self.talker_alias_data = self._io:read_bits_int_be(56)
end

-- 
-- 7-bit => 8 characters, 8-bit => 7 characters, 16-bit => 3 characters.

