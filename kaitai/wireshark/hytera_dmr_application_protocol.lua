-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

require("telemetry_protocol")
require("location_protocol")
require("radio_control_protocol")
require("data_delivery_states")
require("text_message_protocol")
require("data_transmit_protocol")
require("radio_registration_service")
HyteraDmrApplicationProtocol = class.class(KaitaiStruct)

HyteraDmrApplicationProtocol.MessageHeaderTypes = enum.Enum {
  radio_control_protocol = 2,
  location_protocol = 8,
  text_message_protocol = 9,
  radio_registration = 17,
  telemetry_protocol = 18,
  data_transmit_protocol = 19,
  data_delivery_states = 20,
}

function HyteraDmrApplicationProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function HyteraDmrApplicationProtocol:_read()
  self.message_header = self._io:read_u1()
  local _on = self.message_type
  if _on == HyteraDmrApplicationProtocol.MessageHeaderTypes.radio_registration then
    self.data = RadioRegistrationService(self._io)
  elseif _on == HyteraDmrApplicationProtocol.MessageHeaderTypes.telemetry_protocol then
    self.data = TelemetryProtocol(self._io)
  elseif _on == HyteraDmrApplicationProtocol.MessageHeaderTypes.radio_control_protocol then
    self.data = RadioControlProtocol(self._io)
  elseif _on == HyteraDmrApplicationProtocol.MessageHeaderTypes.text_message_protocol then
    self.data = TextMessageProtocol(self._io)
  elseif _on == HyteraDmrApplicationProtocol.MessageHeaderTypes.data_delivery_states then
    self.data = DataDeliveryStates(self._io)
  elseif _on == HyteraDmrApplicationProtocol.MessageHeaderTypes.location_protocol then
    self.data = LocationProtocol(self._io)
  elseif _on == HyteraDmrApplicationProtocol.MessageHeaderTypes.data_transmit_protocol then
    self.data = DataTransmitProtocol(self._io)
  end
  self.checksum = self._io:read_u1()
  self.message_footer = self._io:ensure_fixed_contents("\003")
end

HyteraDmrApplicationProtocol.property.is_reliable_message = {}
function HyteraDmrApplicationProtocol.property.is_reliable_message:get()
  if self._m_is_reliable_message ~= nil then
    return self._m_is_reliable_message
  end

  local _pos = self._io:pos()
  self._io:seek(0)
  self._m_is_reliable_message = self._io:read_bits_int(1)
  self._io:seek(_pos)
  return self._m_is_reliable_message
end

HyteraDmrApplicationProtocol.property.message_type = {}
function HyteraDmrApplicationProtocol.property.message_type:get()
  if self._m_message_type ~= nil then
    return self._m_message_type
  end

  self._m_message_type = HyteraDmrApplicationProtocol.MessageHeaderTypes(bit.band(self.message_header, 143))
  return self._m_message_type
end

-- 
-- contains opcode (2 bytes), payload length (2 bytes) and payload (if length > 0)

