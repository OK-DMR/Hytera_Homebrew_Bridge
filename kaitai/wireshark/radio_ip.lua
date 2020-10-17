-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.1

local class = require("class")
require("kaitaistruct")

-- 
-- represented as 4 bytes, each byte interpreted as number (0-255)
-- 10.0.0.80 means the subnet is set to 10.x.x.x (C) and radio ID is 80
-- 10.22.0.0 means the subnet is set to 10.x.x.x (C) and radio ID is 2200
RadioIp = class.class(KaitaiStruct)

function RadioIp:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RadioIp:_read()
  self.subnet = self._io:read_u1()
  self.radio_id_1 = self._io:read_u1()
  self.radio_id_2 = self._io:read_u1()
  self.radio_id_3 = self._io:read_u1()
end

RadioIp.property.radio_id = {}
function RadioIp.property.radio_id:get()
  if self._m_radio_id ~= nil then
    return self._m_radio_id
  end

  self._m_radio_id = tostring(self.radio_id_1) .. tostring(self.radio_id_2) .. tostring(self.radio_id_3)
  return self._m_radio_id
end


