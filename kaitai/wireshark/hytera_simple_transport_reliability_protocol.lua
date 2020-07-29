-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")
local str_decode = require("string_decode")

require("hytera_dmr_application_protocol")
HyteraSimpleTransportReliabilityProtocol = class.class(KaitaiStruct)

HyteraSimpleTransportReliabilityProtocol.OptionCommands = enum.Enum {
  realtime = 1,
  device_id = 3,
  channel_id = 4,
}

function HyteraSimpleTransportReliabilityProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function HyteraSimpleTransportReliabilityProtocol:_read()
  self.header = str_decode.decode(self._io:read_bytes(2), "UTF-8")
  self.version = self._io:read_u1()
  self.reserved = self._io:read_bits_int(2)
  self.has_option = self._io:read_bits_int(1)
  self.is_reject = self._io:read_bits_int(1)
  self.is_close = self._io:read_bits_int(1)
  self.is_connect = self._io:read_bits_int(1)
  self.is_heartbeat = self._io:read_bits_int(1)
  self.is_ack = self._io:read_bits_int(1)
  self._io:align_to_byte()
  self.sequence_number = self._io:read_u2be()
  if  ((not(self._io:is_eof())) and (not(self.is_heartbeat)))  then
    self.options = {}
    local i = 1
    while true do
      _ = HyteraSimpleTransportReliabilityProtocol.Option(self._io, self, self._root)
      self.options[i] = _
      if not(_.expect_more_options) then
        break
      end
      i = i + 1
    end
end
if  ((not(self._io:is_eof())) and (self.has_option == 1) and (not(self.is_reject)) and (not(self.is_close)) and (not(self.is_connect)))  then
  self.data = {}
  local i = 1
  while not self._io:is_eof() do
    self.data[i] = HyteraDmrApplicationProtocol(self._io)
    i = i + 1
  end
end
end

-- 
-- should be ascii 2B.
-- 
-- current version is 0x00.
-- 
-- number equal for ACK and retransmited messages, and raised for each reply/new message.

HyteraSimpleTransportReliabilityProtocol.Option = class.class(KaitaiStruct)

function HyteraSimpleTransportReliabilityProtocol.Option:_init(io, parent, root)
KaitaiStruct._init(self, io)
self._parent = parent
self._root = root or self
self:_read()
end

function HyteraSimpleTransportReliabilityProtocol.Option:_read()
self.expect_more_options = self._io:read_bits_int(1)
self.command = HyteraSimpleTransportReliabilityProtocol.OptionCommands(self._io:read_bits_int(7))
self._io:align_to_byte()
self.option_data_length = self._io:read_u1()
self.option_payload = self._io:read_bytes(self.option_data_length)
end


