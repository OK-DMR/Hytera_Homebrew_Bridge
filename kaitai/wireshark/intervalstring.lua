-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.1

local class = require("class")
require("kaitaistruct")
local str_decode = require("string_decode")

-- 
-- interval in format ddhhmmss, eg. “00010000” means every 1 hour
Intervalstring = class.class(KaitaiStruct)

function Intervalstring:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Intervalstring:_read()
  self.interval = str_decode.decode(self._io:read_bytes(8), "UTF-8")
end


