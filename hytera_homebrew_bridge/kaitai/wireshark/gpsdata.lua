-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")

Gpsdata = class.class(KaitaiStruct)

function Gpsdata:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function Gpsdata:_read()
  self.gps_status = self._io:read_bytes(1)
  self.gps_time = self._io:read_bytes(6)
  self.gps_date = self._io:read_bytes(6)
  self.north_south = self._io:read_bytes(1)
  self.latitude = self._io:read_bytes(9)
  self.east_west = self._io:read_bytes(1)
  self.longitude = self._io:read_bytes(10)
  self.speed = self._io:read_bytes(2)
  self.direction = self._io:read_bytes(3)
end

-- 
-- A=gps available/locked, V=gps unavailable/no data.
-- 
-- GMT format HHMMSS.
-- 
-- format DDMMYY.
-- 
-- letter N or S.
-- 
-- DDMM.MMMM D=degree(0-90) M=minute(0-59.9999).
-- 
-- letters E or W.
-- 
-- DDDMM.MMMM D=degree(0-180) M=minute(0-59.9999).
-- 
-- speed in knots, eg. 0.2.
-- 
-- azimuth(0-359), 0=north, increase is clockwise.

