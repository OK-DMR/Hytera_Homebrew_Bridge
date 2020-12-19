-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")

-- 
-- Hytera IP Multi-Site Connect Protocol heartbeat packet, either simple KEEPALIVE/UP or PING/PONG
IpSiteConnectHeartbeat = class.class(KaitaiStruct)

function IpSiteConnectHeartbeat:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function IpSiteConnectHeartbeat:_read()
  local _on = self._io:size()
  if _on == 1 then
    self.data = IpSiteConnectHeartbeat.Keepalive(self._io, self, self._root)
  elseif _on == 20 then
    self.data = IpSiteConnectHeartbeat.PingPong(self._io, self, self._root)
  else
    self.data = IpSiteConnectHeartbeat.Unknown(self._io, self, self._root)
  end
end


IpSiteConnectHeartbeat.Keepalive = class.class(KaitaiStruct)

function IpSiteConnectHeartbeat.Keepalive:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function IpSiteConnectHeartbeat.Keepalive:_read()
  self.nullbyte = self._io:read_bytes(1)
  if not(self.nullbyte == "\000") then
    error("not equal, expected " ..  "\000" .. ", but got " .. self.nullbyte)
  end
end


IpSiteConnectHeartbeat.PingPong = class.class(KaitaiStruct)

function IpSiteConnectHeartbeat.PingPong:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function IpSiteConnectHeartbeat.PingPong:_read()
  self.header = self._io:read_bytes(4)
  if not(self.header == "\090\090\090\090") then
    error("not equal, expected " ..  "\090\090\090\090" .. ", but got " .. self.header)
  end
  self.heartbeat_identitier = self._io:read_bytes(5)
  if not(self.heartbeat_identitier == "\010\000\000\000\020") then
    error("not equal, expected " ..  "\010\000\000\000\020" .. ", but got " .. self.heartbeat_identitier)
  end
  self.nullbytes = self._io:read_bytes(3)
  if not(self.nullbytes == "\000\000\000") then
    error("not equal, expected " ..  "\000\000\000" .. ", but got " .. self.nullbytes)
  end
  self.heartbeat_seq = self._io:read_u1()
  self.tail = self._io:read_bytes(7)
  if not(self.tail == "\090\089\090\000\000\000\000") then
    error("not equal, expected " ..  "\090\089\090\000\000\000\000" .. ", but got " .. self.tail)
  end
end

-- 
-- raise this byte by one on response

IpSiteConnectHeartbeat.Unknown = class.class(KaitaiStruct)

function IpSiteConnectHeartbeat.Unknown:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function IpSiteConnectHeartbeat.Unknown:_read()
  self.data = self._io:read_bytes_full()
end


