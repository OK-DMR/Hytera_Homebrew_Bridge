-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.1

local class = require("class")
require("kaitaistruct")

-- 
-- represented as 3 bytes, each byte interpreted as number (0-255)
RadioId = class.class(KaitaiStruct)

function RadioId:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RadioId:_read()
  self.radio_id_raw = self._io:read_u4le()
end

RadioId.property.radio_id = {}
function RadioId.property.radio_id:get()
  if self._m_radio_id ~= nil then
    return self._m_radio_id
  end

  self._m_radio_id = bit.rshift(self.radio_id_raw, 8)
  return self._m_radio_id
end


