-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local str_decode = require("string_decode")

-- 
-- MMDVM protocol structure (MMDVMHost/HBlink3/DMRGateway) based on reversing effort
Mmdvm = class.class(KaitaiStruct)

function Mmdvm:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm:_read()
  self.command_prefix = str_decode.decode(self._io:read_bytes(4), "UTF-8")
  local _on = self.command_prefix
  if _on == "RPTL" then
    self.command_data = Mmdvm.TypeRepeaterLoginRequest(self._io, self, self._root)
  elseif _on == "RPTA" then
    self.command_data = Mmdvm.TypeMasterRepeaterAck(self._io, self, self._root)
  elseif _on == "RPTK" then
    self.command_data = Mmdvm.TypeRepeaterLoginResponse(self._io, self, self._root)
  elseif _on == "RPTC" then
    self.command_data = Mmdvm.TypeRepeaterConfigurationOrClosing(self._io, self, self._root)
  elseif _on == "DMRD" then
    self.command_data = Mmdvm.TypeDmrData(self._io, self, self._root)
  elseif _on == "MSTC" then
    self.command_data = Mmdvm.TypeMasterClosing(self._io, self, self._root)
  elseif _on == "RPTP" then
    self.command_data = Mmdvm.TypeRepeaterPing(self._io, self, self._root)
  elseif _on == "RPTO" then
    self.command_data = Mmdvm.TypeRepeaterOptions(self._io, self, self._root)
  elseif _on == "MSTP" then
    self.command_data = Mmdvm.TypeMasterPong(self._io, self, self._root)
  elseif _on == "MSTN" then
    self.command_data = Mmdvm.TypeMasterNotAccept(self._io, self, self._root)
  elseif _on == "DMRA" then
    self.command_data = Mmdvm.TypeTalkerAlias(self._io, self, self._root)
  else
    self.command_data = Mmdvm.TypeUnknown(self._io, self, self._root)
  end
end

Mmdvm.property.fifth_letter = {}
function Mmdvm.property.fifth_letter:get()
  if self._m_fifth_letter ~= nil then
    return self._m_fifth_letter
  end

  local _pos = self._io:pos()
  self._io:seek(4)
  self._m_fifth_letter = str_decode.decode(self._io:read_bytes(1), "ASCII")
  self._io:seek(_pos)
  return self._m_fifth_letter
end


Mmdvm.TypeMasterPong = class.class(KaitaiStruct)

function Mmdvm.TypeMasterPong:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeMasterPong:_read()
  self.magic = self._io:read_bytes(3)
  if not(self.magic == "\079\078\071") then
    error("not equal, expected " ..  "\079\078\071" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


Mmdvm.TypeTalkerAlias = class.class(KaitaiStruct)

function Mmdvm.TypeTalkerAlias:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeTalkerAlias:_read()
  self.repeater_id = self._io:read_u4be()
  self.radio_id = self._io:read_bits_int_be(24)
  self._io:align_to_byte()
  self.talker_alias = str_decode.decode(self._io:read_bytes(8), "ASCII")
end


Mmdvm.TypeRepeaterConfigurationOrClosing = class.class(KaitaiStruct)

function Mmdvm.TypeRepeaterConfigurationOrClosing:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeRepeaterConfigurationOrClosing:_read()
  local _on = self._root.fifth_letter
  if _on == "L" then
    self.data = Mmdvm.TypeRepeaterClosing(self._io, self, self._root)
  else
    self.data = Mmdvm.TypeRepeaterConfiguration(self._io, self, self._root)
  end
end


Mmdvm.TypeRepeaterLoginResponse = class.class(KaitaiStruct)

function Mmdvm.TypeRepeaterLoginResponse:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeRepeaterLoginResponse:_read()
  self.repeater_id = self._io:read_u4be()
  self.sha256 = self._io:read_bytes(32)
end


Mmdvm.TypeRepeaterLoginRequest = class.class(KaitaiStruct)

function Mmdvm.TypeRepeaterLoginRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeRepeaterLoginRequest:_read()
  self.repeater_id = self._io:read_u4be()
end


Mmdvm.TypeMasterNotAccept = class.class(KaitaiStruct)

function Mmdvm.TypeMasterNotAccept:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeMasterNotAccept:_read()
  self.magic = self._io:read_bytes(2)
  if not(self.magic == "\065\075") then
    error("not equal, expected " ..  "\065\075" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


Mmdvm.TypeUnknown = class.class(KaitaiStruct)

function Mmdvm.TypeUnknown:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeUnknown:_read()
  self.unknown_data = self._io:read_bytes_full()
end


Mmdvm.TypeMasterRepeaterAck = class.class(KaitaiStruct)

function Mmdvm.TypeMasterRepeaterAck:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeMasterRepeaterAck:_read()
  self.magic = self._io:read_bytes(2)
  if not(self.magic == "\067\075") then
    error("not equal, expected " ..  "\067\075" .. ", but got " .. self.magic)
  end
  self.repeater_id_or_challenge = self._io:read_u4be()
end


Mmdvm.TypeMasterClosing = class.class(KaitaiStruct)

function Mmdvm.TypeMasterClosing:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeMasterClosing:_read()
  self.magic = self._io:read_bytes(1)
  if not(self.magic == "\076") then
    error("not equal, expected " ..  "\076" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


Mmdvm.TypeDmrData = class.class(KaitaiStruct)

function Mmdvm.TypeDmrData:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeDmrData:_read()
  self.sequence_no = self._io:read_u1()
  self.source_id = self._io:read_bits_int_be(24)
  self.target_id = self._io:read_bits_int_be(24)
  self._io:align_to_byte()
  self.repeater_id = self._io:read_u4be()
  self.slot_no = self._io:read_bits_int_be(1)
  self.call_type = self._io:read_bits_int_be(1)
  self.frame_type = self._io:read_bits_int_be(2)
  self.data_type = self._io:read_bits_int_be(4)
  self._io:align_to_byte()
  self.stream_id = self._io:read_u4be()
  self.dmr_data = self._io:read_bytes(33)
  if not(self._io:is_eof()) then
    self.bit_error_rate = self._io:read_u1()
  end
  if not(self._io:is_eof()) then
    self.rssi = self._io:read_u1()
  end
end


Mmdvm.TypeRepeaterOptions = class.class(KaitaiStruct)

function Mmdvm.TypeRepeaterOptions:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeRepeaterOptions:_read()
  self.repeater_id = self._io:read_u4be()
  self.options = str_decode.decode(self._io:read_bytes_full(), "ASCII")
end

-- 
-- structure probably key=value;key=value;...

Mmdvm.TypeRepeaterClosing = class.class(KaitaiStruct)

function Mmdvm.TypeRepeaterClosing:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeRepeaterClosing:_read()
  self.magic = self._io:read_bytes(1)
  if not(self.magic == "\076") then
    error("not equal, expected " ..  "\076" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


Mmdvm.TypeRepeaterConfiguration = class.class(KaitaiStruct)

function Mmdvm.TypeRepeaterConfiguration:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeRepeaterConfiguration:_read()
  self.repeater_id = self._io:read_u4be()
  self.call_sign = str_decode.decode(self._io:read_bytes(8), "ASCII")
  self.rx_freq = str_decode.decode(self._io:read_bytes(9), "ASCII")
  self.tx_freq = str_decode.decode(self._io:read_bytes(9), "ASCII")
  self.tx_power = str_decode.decode(self._io:read_bytes(2), "ASCII")
  self.color_code = str_decode.decode(self._io:read_bytes(2), "ASCII")
  self.latitude = str_decode.decode(self._io:read_bytes(8), "ASCII")
  self.longitude = str_decode.decode(self._io:read_bytes(9), "ASCII")
  self.antenna_height_above_ground = str_decode.decode(self._io:read_bytes(3), "ASCII")
  self.location = str_decode.decode(self._io:read_bytes(20), "ASCII")
  self.description = str_decode.decode(self._io:read_bytes(19), "ASCII")
  self.slots = str_decode.decode(self._io:read_bytes(1), "ASCII")
  self.url = str_decode.decode(self._io:read_bytes(124), "ASCII")
  self.software_id = str_decode.decode(self._io:read_bytes(40), "ASCII")
  self.package_id = str_decode.decode(self._io:read_bytes(40), "ASCII")
  self.unparsed_data = str_decode.decode(self._io:read_bytes_full(), "ASCII")
end

-- 
-- 1 = only slot 1, 2 = only slot 2, 3 = both slots.

Mmdvm.TypeRepeaterPing = class.class(KaitaiStruct)

function Mmdvm.TypeRepeaterPing:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Mmdvm.TypeRepeaterPing:_read()
  self.magic = self._io:read_bytes(3)
  if not(self.magic == "\073\078\071") then
    error("not equal, expected " ..  "\073\078\071" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


