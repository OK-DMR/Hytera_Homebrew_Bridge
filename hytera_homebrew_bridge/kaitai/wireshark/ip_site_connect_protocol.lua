-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

-- 
-- Hytera IP Multi-Site Protocol re-implementation from dmrshark original
IpSiteConnectProtocol = class.class(KaitaiStruct)

IpSiteConnectProtocol.PacketTypes = enum.Enum {
  a = 65,
  b = 66,
}

IpSiteConnectProtocol.FrameTypes = enum.Enum {
  frame_type_data = 0,
  frame_type_voice_sync = 4369,
  frame_type_data_sync_or_csbk = 13107,
  frame_type_data_header = 26214,
  frame_type_sync = 61166,
}

IpSiteConnectProtocol.CallTypes = enum.Enum {
  private_call = 0,
  group_call = 1,
}

IpSiteConnectProtocol.SlotTypes = enum.Enum {
  slot_type_privacy_indicator = 0,
  slot_type_voice_lc_header = 4369,
  slot_type_terminator_with_lc = 8738,
  slot_type_csbk = 13107,
  slot_type_data_header = 17476,
  slot_type_rate_12_data = 21845,
  slot_type_rate_34_data = 26214,
  slot_type_data_c = 30583,
  slot_type_data_d = 34952,
  slot_type_data_e = 39321,
  slot_type_data_f = 43690,
  slot_type_data_a = 48059,
  slot_type_data_b = 52428,
  slot_type_wakeup_request = 56797,
  slot_type_sync = 61166,
}

IpSiteConnectProtocol.Timeslots = enum.Enum {
  timeslot_1 = 4369,
  timeslot_2 = 8738,
}

function IpSiteConnectProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function IpSiteConnectProtocol:_read()
  self.source_port = self._io:read_bytes(2)
  self.fixed_header = self._io:read_bytes(2)
  self.sequence_number = self._io:read_u1()
  self.reserved_3 = self._io:read_bytes(3)
  self.packet_type = IpSiteConnectProtocol.PacketTypes(self._io:read_u1())
  self.reserved_7a = self._io:read_bytes(7)
  self.timeslot_raw = IpSiteConnectProtocol.Timeslots(self._io:read_u2be())
  self.slot_type = IpSiteConnectProtocol.SlotTypes(self._io:read_u2be())
  self.color_code_raw = self._io:read_u2le()
  self.frame_type = IpSiteConnectProtocol.FrameTypes(self._io:read_u2be())
  self.reserved_2a = self._io:read_bytes(2)
  self.ipsc_payload = self._io:read_bytes(34)
  self.reserved_2b = self._io:read_bytes(2)
  self.call_type = IpSiteConnectProtocol.CallTypes(self._io:read_u1())
  self.destination_radio_id_raw = self._io:read_u4le()
  self.source_radio_id_raw = self._io:read_u4le()
  self.reserved_1b = self._io:read_u1()
  if not(self._io:is_eof()) then
    self.extra_data = self._io:read_bytes_full()
  end
end

IpSiteConnectProtocol.property.source_radio_id = {}
function IpSiteConnectProtocol.property.source_radio_id:get()
  if self._m_source_radio_id ~= nil then
    return self._m_source_radio_id
  end

  self._m_source_radio_id = (self.source_radio_id_raw >> 8)
  return self._m_source_radio_id
end

IpSiteConnectProtocol.property.destination_radio_id = {}
function IpSiteConnectProtocol.property.destination_radio_id:get()
  if self._m_destination_radio_id ~= nil then
    return self._m_destination_radio_id
  end

  self._m_destination_radio_id = (self.destination_radio_id_raw >> 8)
  return self._m_destination_radio_id
end

IpSiteConnectProtocol.property.color_code = {}
function IpSiteConnectProtocol.property.color_code:get()
  if self._m_color_code ~= nil then
    return self._m_color_code
  end

  self._m_color_code = (self.color_code_raw & 15)
  return self._m_color_code
end

-- 
-- UDP source port of IPSC packet
-- 
-- will be color code repeated, ie. cc=5 means two incoming bytes [0x55, 0x55].

