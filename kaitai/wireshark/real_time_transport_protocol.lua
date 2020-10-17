-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.1

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

require("radio_id")
-- 
-- each packet should contain 60ms of voice data for AMBE compatibility
RealTimeTransportProtocol = class.class(KaitaiStruct)

RealTimeTransportProtocol.RtpPayloadTypes = enum.Enum {
  mu_law = 0,
  a_law = 8,
}

RealTimeTransportProtocol.CallTypes = enum.Enum {
  private_call = 0,
  group_call = 1,
  all_call = 2,
}

function RealTimeTransportProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RealTimeTransportProtocol:_read()
  self.fixed_header = RealTimeTransportProtocol.FixedHeader(self._io, self, self._root)
  if (self.fixed_header.extension and 1 or 0) == 1 then
    self.header_extension = RealTimeTransportProtocol.HeaderExtension(self._io, self, self._root)
  end
  self.audio_data = self._io:read_bytes_full()
end


RealTimeTransportProtocol.FixedHeader = class.class(KaitaiStruct)

function RealTimeTransportProtocol.FixedHeader:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RealTimeTransportProtocol.FixedHeader:_read()
  self.version = self._io:read_bits_int_be(2)
  self.padding = self._io:read_bits_int_be(1)
  self.extension = self._io:read_bits_int_be(1)
  self.csrc_count = self._io:read_bits_int_be(4)
  self.marker = self._io:read_bits_int_be(1)
  self.payload_type = self._io:read_bits_int_be(7)
  self._io:align_to_byte()
  self.sequence_number = self._io:read_u2be()
  self.timestamp = self._io:read_u4be()
  self.ssrc = self._io:read_u4be()
  self.csrc = {}
  for i = 0, self.csrc_count - 1 do
    self.csrc[i + 1] = self._io:read_u4be()
  end
end

-- 
-- if set, this packet contains padding bytes at the end.
-- 
-- if set, fixed header is followed by single header extension.
-- 
-- number of csrc identifiers that follow fixed header (val. 0-15).
-- 
-- marker meaning is defined by RTP profile, for HDAP should be always 0.
-- 
-- sequence does not start from 0, but from random number.
-- 
-- sampling instant of the first octet in this RTP packet.
-- 
-- synchronized source identifier.
-- 
-- contributing sources.

RealTimeTransportProtocol.HeaderExtension = class.class(KaitaiStruct)

function RealTimeTransportProtocol.HeaderExtension:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RealTimeTransportProtocol.HeaderExtension:_read()
  self.header_identifier = self._io:read_u2be()
  self.length = self._io:read_u2be()
  self.slot = self._io:read_bits_int_be(7)
  self.last_flag = self._io:read_bits_int_be(1)
  self._io:align_to_byte()
  self.source_id = RadioId(self._io)
  self.destination_id = RadioId(self._io)
  self.call_type = RealTimeTransportProtocol.CallTypes(self._io:read_u1())
  self.reserved = self._io:read_bytes(4)
end

-- 
-- number of 32bit words following the header+length fields.
-- 
-- slot number 1 or 2.
-- 
-- indicates end of voice call.
-- 
-- reserved 32bits.

