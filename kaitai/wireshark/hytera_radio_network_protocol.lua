-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

require("hytera_dmr_application_protocol")
HyteraRadioNetworkProtocol = class.class(KaitaiStruct)

HyteraRadioNetworkProtocol.Opcodes = enum.Enum {
  data = 0,
  data_ack = 16,
  close_ack = 250,
  close = 251,
  reject = 252,
  accept = 253,
  connect = 254,
}

function HyteraRadioNetworkProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function HyteraRadioNetworkProtocol:_read()
  self.header_identifier = self._io:ensure_fixed_contents("\126")
  self.version = self._io:read_u1()
  self.block = self._io:read_u1()
  self.opcode = HyteraRadioNetworkProtocol.Opcodes(self._io:read_u1())
  self.source_id = self._io:read_u1()
  self.destination_id = self._io:read_u1()
  self.packet_number = self._io:read_u2be()
  self.hrnp_packet_length = self._io:read_u2be()
  self.checksum = self._io:read_u2be()
  if self.opcode == HyteraRadioNetworkProtocol.Opcodes.data then
    self.data = HyteraDmrApplicationProtocol(self._io)
  end
end


