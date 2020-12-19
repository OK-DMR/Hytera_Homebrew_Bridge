-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local str_decode = require("string_decode")

-- 
-- time in format yyyyMMddhhmmss, timezone GMT
Datetimestring = class.class(KaitaiStruct)

function Datetimestring:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Datetimestring:_read()
  self.datetime = str_decode.decode(self._io:read_bytes(14), "UTF-8")
end


