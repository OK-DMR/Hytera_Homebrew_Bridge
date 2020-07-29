-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

require("radio_ip")
DataDeliveryStates = class.class(KaitaiStruct)

DataDeliveryStates.StateTypes = enum.Enum {
  location_protocol_state = 8,
  radio_registration_service_state = 17,
  telemetry_protocol_state = 18,
  data_transmit_protocol_state = 19,
}

DataDeliveryStates.Results = enum.Enum {
  ok = 0,
  fail = 1,
  limited_timeout = 4,
  no_ack = 5,
  error_ack = 6,
  repeater_wakeup_fail = 7,
  tx_interrupted = 8,
  tx_deny = 9,
  invalid_params = 10,
}

function DataDeliveryStates:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DataDeliveryStates:_read()
  self.reserved = self._io:read_bytes(1)
  self.state_type = DataDeliveryStates.StateTypes(self._io:read_u1())
  self.message_length = self._io:read_u2be()
  self.radio_ip = RadioIp(self._io)
  self.protocol_opcode = self._io:read_u2be()
  self.result = DataDeliveryStates.Results(self._io:read_u1())
end

-- 
-- should be 0x00.
-- 
-- length of the message from next field to the end of DDS message.
-- 
-- state_type+protocol_opcode should correspond to sent message, that this status is about.

