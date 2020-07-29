-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")
local str_decode = require("string_decode")

require("radio_ip")
TelemetryProtocol = class.class(KaitaiStruct)

TelemetryProtocol.ServiceTypes = enum.Enum {
  status_report_service = 160,
  remote_control_service = 176,
}

TelemetryProtocol.ResultTypes = enum.Enum {
  effective = 0,
  ineffective = 1,
}

TelemetryProtocol.CallTypes = enum.Enum {
  private_call = 0,
  group_call = 1,
  all_call = 2,
}

TelemetryProtocol.OperationTypes = enum.Enum {
  set_ineffective_level = 0,
  set_effective_level = 1,
  reverse_level = 2,
  output_one_pulse = 3,
}

TelemetryProtocol.PcFlagTypes = enum.Enum {
  controller_is_radio = 0,
  controller_is_telemetry_application = 1,
}

TelemetryProtocol.ServiceSpecificTypes = enum.Enum {
  standard_status_request = 40961,
  standard_status_report = 41089,
  extended_status_report = 41090,
  remote_control_request = 45057,
  remote_control_answer = 45185,
}

TelemetryProtocol.ControlResultTypes = enum.Enum {
  success = 0,
  failure = 1,
}

function TelemetryProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function TelemetryProtocol:_read()
  self.service_type_opcode = TelemetryProtocol.ServiceTypes(self._io:read_u1())
  self.specific_service_opcode = self._io:read_u1()
  self.message_length = self._io:read_u2be()
  local _on = self.specific_service
  if _on == TelemetryProtocol.ServiceSpecificTypes.standard_status_request then
    self.data = TelemetryProtocol.StandardStatusRequest(self._io, self, self._root)
  elseif _on == TelemetryProtocol.ServiceSpecificTypes.remote_control_answer then
    self.data = TelemetryProtocol.RemoteControlAnswer(self._io, self, self._root)
  elseif _on == TelemetryProtocol.ServiceSpecificTypes.extended_status_report then
    self.data = TelemetryProtocol.ExtendedStatusReport(self._io, self, self._root)
  elseif _on == TelemetryProtocol.ServiceSpecificTypes.remote_control_request then
    self.data = TelemetryProtocol.RemoteControlRequest(self._io, self, self._root)
  elseif _on == TelemetryProtocol.ServiceSpecificTypes.standard_status_report then
    self.data = TelemetryProtocol.StandardStatusReport(self._io, self, self._root)
  end
end

TelemetryProtocol.property.specific_service = {}
function TelemetryProtocol.property.specific_service:get()
  if self._m_specific_service ~= nil then
    return self._m_specific_service
  end

  local _pos = self._io:pos()
  self._io:seek(0)
  self._m_specific_service = TelemetryProtocol.ServiceSpecificTypes(self._io:read_u2be())
  self._io:seek(_pos)
  return self._m_specific_service
end

-- 
-- length of the message from next field to the end of TP message.

TelemetryProtocol.StandardStatusReport = class.class(KaitaiStruct)

function TelemetryProtocol.StandardStatusReport:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function TelemetryProtocol.StandardStatusReport:_read()
  self.source_ip = RadioIp(self._io)
  self.target_ip = RadioIp(self._io)
  self.pc_flag = TelemetryProtocol.PcFlagTypes(self._io:read_u1())
  self.call_type = TelemetryProtocol.CallTypes(self._io:read_u1())
  self.vio_select = self._io:read_bytes(1)
  self.result = TelemetryProtocol.ResultTypes(self._io:read_u1())
end

-- 
-- answer should be always of type private call for now.
-- 
-- reserved.

TelemetryProtocol.VioExtendedStatus = class.class(KaitaiStruct)

function TelemetryProtocol.VioExtendedStatus:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function TelemetryProtocol.VioExtendedStatus:_read()
  self.result = TelemetryProtocol.ResultTypes(self._io:read_u1())
  self.message_length = self._io:read_u2be()
  self.message = str_decode.decode(self._io:read_bytes(self.message_length), "UTF16-LE")
end


TelemetryProtocol.RemoteControlAnswer = class.class(KaitaiStruct)

function TelemetryProtocol.RemoteControlAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function TelemetryProtocol.RemoteControlAnswer:_read()
  self.source_ip = RadioIp(self._io)
  self.target_ip = RadioIp(self._io)
  self.pc_flag = TelemetryProtocol.PcFlagTypes(self._io:read_u1())
  self.call_type = TelemetryProtocol.CallTypes(self._io:read_u1())
  self.vio_select = self._io:read_bytes(1)
  self.result = TelemetryProtocol.ControlResultTypes(self._io:read_u1())
end

-- 
-- answer should be always of type private call for now.
-- 
-- Bit 0-5 correspond to VIO1-VIO6, 1=selected, 0=not selected, corresponds to request.

TelemetryProtocol.RemoteControlRequest = class.class(KaitaiStruct)

function TelemetryProtocol.RemoteControlRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function TelemetryProtocol.RemoteControlRequest:_read()
  self.source_ip = RadioIp(self._io)
  self.target_ip = RadioIp(self._io)
  self.pc_flag = TelemetryProtocol.PcFlagTypes(self._io:read_u1())
  self.call_type = TelemetryProtocol.CallTypes(self._io:read_u1())
  self.vio_select = self._io:read_bytes(1)
  self.operation = TelemetryProtocol.OperationTypes(self._io:read_u1())
end

-- 
-- answer should be always of type private call for now.
-- 
-- Bit 0-5 correspond to VIO1-VIO6, 1=selected, 0=not selected, only one can be selected in request.

TelemetryProtocol.ExtendedStatusReport = class.class(KaitaiStruct)

function TelemetryProtocol.ExtendedStatusReport:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function TelemetryProtocol.ExtendedStatusReport:_read()
  self.source_ip = RadioIp(self._io)
  self.target_ip = RadioIp(self._io)
  self.pc_flag = TelemetryProtocol.PcFlagTypes(self._io:read_u1())
  self.call_type = TelemetryProtocol.CallTypes(self._io:read_u1())
  self.vio_select = self._io:read_bytes(1)
  self.result_messages = TelemetryProtocol.VioExtendedStatus(self._io, self, self._root)
end

-- 
-- answer should be always of type private call for now.
-- 
-- reserved.

TelemetryProtocol.StandardStatusRequest = class.class(KaitaiStruct)

function TelemetryProtocol.StandardStatusRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function TelemetryProtocol.StandardStatusRequest:_read()
  self.source_ip = RadioIp(self._io)
  self.target_ip = RadioIp(self._io)
  self.pc_flag = TelemetryProtocol.PcFlagTypes(self._io:read_u1())
  self.call_type = TelemetryProtocol.CallTypes(self._io:read_u1())
  self.vio_select = self._io:read_bytes(1)
end

-- 
-- reserved.

