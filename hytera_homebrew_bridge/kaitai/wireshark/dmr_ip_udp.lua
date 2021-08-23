-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

-- 
-- ETSI TS 102 361-3 V1.3.1, section 7, PDUs
DmrIpUdp = class.class(KaitaiStruct)

DmrIpUdp.SourceIpAddressIds = enum.Enum {
  radio_network = 0,
  usb_ethernet_interface_network = 1,
}

DmrIpUdp.DestinationIpAddressIds = enum.Enum {
  radio_network = 0,
  usb_ethernet_interface_network = 1,
  group_network = 2,
}

DmrIpUdp.UdpPortIds = enum.Enum {
  present_in_extended_header = 0,
  utf16be_text_message_port_5016 = 1,
  location_interface_protocol = 2,
}

function DmrIpUdp:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrIpUdp:_read()
end


-- 
-- 7.2.3 UDP/IPv4 Compressed Header, Table 7.14
DmrIpUdp.UdpIpv4CompressedHeader = class.class(KaitaiStruct)

function DmrIpUdp.UdpIpv4CompressedHeader:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DmrIpUdp.UdpIpv4CompressedHeader:_read()
  self.ipv4_identification = self._io:read_bytes(2)
  self.source_ip_address_id = self._io:read_bits_int_be(4)
  self.destination_ip_address_id = self._io:read_bits_int_be(4)
  self.header_compression_opcode_msb = self._io:read_bits_int_be(1)
  self.udp_source_port_id = self._io:read_bits_int_be(7)
  self.header_compression_opcode_lsb = self._io:read_bits_int_be(1)
  self.udp_destination_port_id = self._io:read_bits_int_be(7)
  self._io:align_to_byte()
  self.extended_header_1 = self._io:read_bytes(2)
  self.extended_header_2 = self._io:read_bytes(2)
end

-- 
-- SAID.
-- 
-- DAID.
-- 
-- SPID.
-- 
-- DPID.
-- 
-- in this order: source port (if SPID==0) or destination port (if SPID!=0) or data (if SPID!=0 and DPID!=0)
-- 
-- in this order: destination port (if SPID==0 and DPID==0) or data (if SPID!=0 and DPID!=0).

