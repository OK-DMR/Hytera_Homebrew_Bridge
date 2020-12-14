-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local str_decode = require("string_decode")

-- 
-- Homebrew / MMDVM protocol structure, based on both PDF (DL5DI, G4KLX, DG1HT 2015) and MMDVMHost/HBlink3/DMRGateway
-- reversing effort
Homebrew = class.class(KaitaiStruct)

function Homebrew:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew:_read()
  self.command_prefix = str_decode.decode(self._io:read_bytes(4), "UTF-8")
  local _on = self.command_prefix
  if _on == "RPTL" then
    self.command_data = Homebrew.TypeRepeaterLoginRequest(self._io, self, self._root)
  elseif _on == "RPTA" then
    self.command_data = Homebrew.TypeMasterRepeaterAck(self._io, self, self._root)
  elseif _on == "RPTK" then
    self.command_data = Homebrew.TypeRepeaterLoginResponse(self._io, self, self._root)
  elseif _on == "RPTC" then
    self.command_data = Homebrew.TypeRepeaterConfigurationOrClosing(self._io, self, self._root)
  elseif _on == "DMRD" then
    self.command_data = Homebrew.TypeDmrData(self._io, self, self._root)
  elseif _on == "MSTC" then
    self.command_data = Homebrew.TypeMasterClosing(self._io, self, self._root)
  elseif _on == "RPTP" then
    self.command_data = Homebrew.TypeRepeaterPing(self._io, self, self._root)
  elseif _on == "RPTO" then
    self.command_data = Homebrew.TypeRepeaterOptions(self._io, self, self._root)
  elseif _on == "MSTP" then
    self.command_data = Homebrew.TypeMasterPong(self._io, self, self._root)
  elseif _on == "MSTN" then
    self.command_data = Homebrew.TypeMasterNotAccept(self._io, self, self._root)
  elseif _on == "DMRA" then
    self.command_data = Homebrew.TypeTalkerAlias(self._io, self, self._root)
  else
    self.command_data = Homebrew.TypeUnknown(self._io, self, self._root)
  end
end

Homebrew.property.fifth_letter = {}
function Homebrew.property.fifth_letter:get()
  if self._m_fifth_letter ~= nil then
    return self._m_fifth_letter
  end

  local _pos = self._io:pos()
  self._io:seek(4)
  self._m_fifth_letter = str_decode.decode(self._io:read_bytes(1), "ASCII")
  self._io:seek(_pos)
  return self._m_fifth_letter
end


Homebrew.TypeMasterPong = class.class(KaitaiStruct)

function Homebrew.TypeMasterPong:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeMasterPong:_read()
  self.magic = self._io:read_bytes(3)
  if not(self.magic == "\079\078\071") then
    error("not equal, expected " ..  "\079\078\071" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


Homebrew.TypeTalkerAlias = class.class(KaitaiStruct)

function Homebrew.TypeTalkerAlias:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeTalkerAlias:_read()
  self.repeater_id = self._io:read_u4be()
  self.radio_id = self._io:read_bits_int_be(24)
  self._io:align_to_byte()
  self.talker_alias = str_decode.decode(self._io:read_bytes(8), "ASCII")
end


Homebrew.TypeRepeaterConfigurationOrClosing = class.class(KaitaiStruct)

function Homebrew.TypeRepeaterConfigurationOrClosing:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeRepeaterConfigurationOrClosing:_read()
  local _on = self._root.fifth_letter
  if _on == "L" then
    self.data = Homebrew.TypeRepeaterClosing(self._io, self, self._root)
  else
    self.data = Homebrew.TypeRepeaterConfiguration(self._io, self, self._root)
  end
end


Homebrew.TypeRepeaterLoginResponse = class.class(KaitaiStruct)

function Homebrew.TypeRepeaterLoginResponse:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeRepeaterLoginResponse:_read()
  self.repeater_id = self._io:read_u4be()
  self.sha256 = self._io:read_bytes(32)
end


Homebrew.TypeRepeaterLoginRequest = class.class(KaitaiStruct)

function Homebrew.TypeRepeaterLoginRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeRepeaterLoginRequest:_read()
  self.repeater_id = self._io:read_u4be()
end


Homebrew.TypeMasterNotAccept = class.class(KaitaiStruct)

function Homebrew.TypeMasterNotAccept:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeMasterNotAccept:_read()
  self.magic = self._io:read_bytes(2)
  if not(self.magic == "\065\075") then
    error("not equal, expected " ..  "\065\075" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


Homebrew.TypeUnknown = class.class(KaitaiStruct)

function Homebrew.TypeUnknown:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeUnknown:_read()
  self.unknown_data = self._io:read_bytes_full()
end


Homebrew.TypeMasterRepeaterAck = class.class(KaitaiStruct)

function Homebrew.TypeMasterRepeaterAck:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeMasterRepeaterAck:_read()
  self.magic = self._io:read_bytes(2)
  if not(self.magic == "\067\075") then
    error("not equal, expected " ..  "\067\075" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
  if not(self._io:is_eof()) then
    self.random_number = self._io:read_u4be()
  end
end


Homebrew.TypeMasterClosing = class.class(KaitaiStruct)

function Homebrew.TypeMasterClosing:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeMasterClosing:_read()
  self.magic = self._io:read_bytes(1)
  if not(self.magic == "\076") then
    error("not equal, expected " ..  "\076" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


Homebrew.TypeDmrData = class.class(KaitaiStruct)

function Homebrew.TypeDmrData:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeDmrData:_read()
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


Homebrew.TypeRepeaterOptions = class.class(KaitaiStruct)

function Homebrew.TypeRepeaterOptions:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeRepeaterOptions:_read()
  self.repeater_id = self._io:read_u4be()
  self.options = str_decode.decode(self._io:read_bytes_full(), "ASCII")
end

-- 
-- structure probably key=value;key=value;...

Homebrew.TypeRepeaterClosing = class.class(KaitaiStruct)

function Homebrew.TypeRepeaterClosing:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeRepeaterClosing:_read()
  self.magic = self._io:read_bytes(1)
  if not(self.magic == "\076") then
    error("not equal, expected " ..  "\076" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


Homebrew.TypeRepeaterConfiguration = class.class(KaitaiStruct)

function Homebrew.TypeRepeaterConfiguration:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeRepeaterConfiguration:_read()
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
  self.description = str_decode.decode(self._io:read_bytes(20), "ASCII")
  self.url = str_decode.decode(self._io:read_bytes(124), "ASCII")
  self.software_id = str_decode.decode(self._io:read_bytes(40), "ASCII")
  self.package_id = str_decode.decode(self._io:read_bytes(40), "ASCII")
  self.unparsed_data = str_decode.decode(self._io:read_bytes_full(), "ASCII")
end


Homebrew.TypeRepeaterPing = class.class(KaitaiStruct)

function Homebrew.TypeRepeaterPing:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Homebrew.TypeRepeaterPing:_read()
  self.magic = self._io:read_bytes(3)
  if not(self.magic == "\073\078\071") then
    error("not equal, expected " ..  "\073\078\071" .. ", but got " .. self.magic)
  end
  self.repeater_id = self._io:read_u4be()
end


