-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

require("radio_ip")
RadioRegistrationService = class.class(KaitaiStruct)

RadioRegistrationService.RrsTypes = enum.Enum {
  de_registration = 1,
  online_check = 2,
  registration = 3,
  registration_ack = 128,
  online_check_ack = 130,
}

function RadioRegistrationService:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RadioRegistrationService:_read()
  self.opcode = self._io:ensure_fixed_contents("\000")
  self.rrs_type = RadioRegistrationService.RrsTypes(self._io:read_u1())
  self.message_length = self._io:read_u2le()
  self.radio_ip = RadioIp(self._io)
  if  ((self.rrs_type == RadioRegistrationService.RrsTypes.registration_ack) or (self.rrs_type == RadioRegistrationService.RrsTypes.online_check_ack))  then
    self.result = self._io:read_u1()
  end
  if self.rrs_type == RadioRegistrationService.RrsTypes.registration_ack then
    self.valid_time = self._io:read_u4be()
  end
end

-- 
-- length of the message from next field to the end of RRS message.
-- 
-- number of seconds the online registration message shall be resended from terminal.

