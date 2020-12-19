-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

require("datetimestring")
require("gpsdata")
require("radio_ip")
require("intervalstring")
LocationProtocol = class.class(KaitaiStruct)

LocationProtocol.CmdTypes = enum.Enum {
  cancel_request = 0,
  start_request = 1,
}

LocationProtocol.LpSpecificTypes = enum.Enum {
  standard_request = 40961,
  standard_answer = 40962,
  emergency_report_stop_request = 45057,
  emergency_report_stop_answer = 45058,
  emergency_report = 45059,
  triggered_report_request = 49153,
  triggered_report_answer = 49154,
  triggered_report = 49155,
  triggered_report_stop_request = 49156,
  triggered_report_stop_answer = 49157,
  condition_report_request = 53249,
  condition_report_answer = 53250,
  condition_report = 53251,
  condition_quick_gps_request = 53265,
  condition_quick_gps_answer = 53266,
}

LocationProtocol.LpGeneralTypes = enum.Enum {
  standard_location_immediate_service = 160,
  emergency_location_reporting_service = 176,
  triggered_location_reporting_service = 192,
  condition_triggered_reporting_service = 208,
}

LocationProtocol.TriggerTypes = enum.Enum {
  cancel_request = 0,
  distance = 1,
  time = 2,
  distance_and_time = 3,
  distance_or_time = 4,
}

LocationProtocol.ResultCodes = enum.Enum {
  ok = 0,
  position_method_failure = 6,
  request_format_error = 105,
}

function LocationProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol:_read()
  self.opcode_header = self._io:read_bytes(2)
  self.message_length = self._io:read_u2be()
  local _on = self.opcode_header_int
  if _on == LocationProtocol.LpSpecificTypes.triggered_report_answer then
    self.data = LocationProtocol.TriggeredReportAnswer(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.emergency_report_stop_request then
    self.data = LocationProtocol.EmergencyReportStopRequest(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.condition_quick_gps_request then
    self.data = LocationProtocol.ConditionQuickGpsRequest(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.condition_report then
    self.data = LocationProtocol.ConditionReport(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.emergency_report_stop_answer then
    self.data = LocationProtocol.EmergencyReportStopAnswer(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.condition_report_answer then
    self.data = LocationProtocol.ConditionReportAnswer(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.standard_answer then
    self.data = LocationProtocol.StandardAnswer(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.standard_request then
    self.data = LocationProtocol.StandardRequest(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.triggered_report then
    self.data = LocationProtocol.TriggeredReport(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.triggered_report_stop_answer then
    self.data = LocationProtocol.TriggeredReportStopAnswer(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.triggered_report_stop_request then
    self.data = LocationProtocol.TriggeredReportStopRequest(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.emergency_report then
    self.data = LocationProtocol.EmergencyReport(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.condition_report_request then
    self.data = LocationProtocol.ConditionReportRequest(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.triggered_report_request then
    self.data = LocationProtocol.TriggeredReportRequest(self._io, self, self._root)
  elseif _on == LocationProtocol.LpSpecificTypes.condition_quick_gps_answer then
    self.data = LocationProtocol.ConditionQuickGpsAnswer(self._io, self, self._root)
  end
end

LocationProtocol.property.opcode = {}
function LocationProtocol.property.opcode:get()
  if self._m_opcode ~= nil then
    return self._m_opcode
  end

  local _pos = self._io:pos()
  self._io:seek(0)
  self._m_opcode = LocationProtocol.LpGeneralTypes(self._io:read_u1())
  self._io:seek(_pos)
  return self._m_opcode
end

LocationProtocol.property.opcode_header_int = {}
function LocationProtocol.property.opcode_header_int:get()
  if self._m_opcode_header_int ~= nil then
    return self._m_opcode_header_int
  end

  local _pos = self._io:pos()
  self._io:seek(0)
  self._m_opcode_header_int = LocationProtocol.LpSpecificTypes(self._io:read_u2be())
  self._io:seek(_pos)
  return self._m_opcode_header_int
end

-- 
-- length of the message from next field to the end of LP message.

LocationProtocol.TriggeredReportStopAnswer = class.class(KaitaiStruct)

function LocationProtocol.TriggeredReportStopAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.TriggeredReportStopAnswer:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.result = LocationProtocol.ResultCodes(self._io:read_u2be())
end


LocationProtocol.ConditionReportRequest = class.class(KaitaiStruct)

function LocationProtocol.ConditionReportRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.ConditionReportRequest:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.trigger_type = self._io:read_u1()
  self.distance = self._io:read_u4be()
  self.start_time = Datetimestring(self._io)
  self.stop_time = Datetimestring(self._io)
  self.interval = Intervalstring(self._io)
  self.max_interval = Intervalstring(self._io)
end


LocationProtocol.ConditionQuickGpsRequest = class.class(KaitaiStruct)

function LocationProtocol.ConditionQuickGpsRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.ConditionQuickGpsRequest:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.cmd_type = LocationProtocol.CmdTypes(self._io:read_u1())
  if self.cmd_type == LocationProtocol.CmdTypes.start_request then
    self.quick_gps_payload = LocationProtocol.QuickGpsPayload(self._io, self, self._root)
  end
end


LocationProtocol.ConditionReport = class.class(KaitaiStruct)

function LocationProtocol.ConditionReport:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.ConditionReport:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.gpsdata = Gpsdata(self._io)
end


LocationProtocol.EmergencyReport = class.class(KaitaiStruct)

function LocationProtocol.EmergencyReport:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.EmergencyReport:_read()
  self.radio_ip = RadioIp(self._io)
  self.emergency_type = self._io:read_u1()
  self.gpsdata = Gpsdata(self._io)
end


LocationProtocol.TriggeredReportAnswer = class.class(KaitaiStruct)

function LocationProtocol.TriggeredReportAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.TriggeredReportAnswer:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.result = LocationProtocol.ResultCodes(self._io:read_u2be())
end


LocationProtocol.QuickGpsPayload = class.class(KaitaiStruct)

function LocationProtocol.QuickGpsPayload:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.QuickGpsPayload:_read()
  self.start_time = Datetimestring(self._io)
  self.stop_time = Datetimestring(self._io)
  self.interval = Intervalstring(self._io)
  self.send_step = self._io:read_u2be()
  self.channel_use_percentage = self._io:read_u1()
  self.send_order = self._io:read_u2be()
end

-- 
-- milliseconds.
-- 
-- sequence number, ie. n-th radio to report position once the interval time is up.

LocationProtocol.StandardRequest = class.class(KaitaiStruct)

function LocationProtocol.StandardRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.StandardRequest:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
end


LocationProtocol.TriggeredReportRequest = class.class(KaitaiStruct)

function LocationProtocol.TriggeredReportRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.TriggeredReportRequest:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.start_time = Datetimestring(self._io)
  self.stop_time = Datetimestring(self._io)
  self.interval = Intervalstring(self._io)
end


LocationProtocol.StandardAnswer = class.class(KaitaiStruct)

function LocationProtocol.StandardAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.StandardAnswer:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.result = LocationProtocol.ResultCodes(self._io:read_u2be())
  self.gpsdata = Gpsdata(self._io)
end


LocationProtocol.ConditionReportAnswer = class.class(KaitaiStruct)

function LocationProtocol.ConditionReportAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.ConditionReportAnswer:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.trigger_type = LocationProtocol.TriggerTypes(self._io:read_u1())
  self.result = LocationProtocol.ResultCodes(self._io:read_u2be())
end


LocationProtocol.EmergencyReportStopRequest = class.class(KaitaiStruct)

function LocationProtocol.EmergencyReportStopRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.EmergencyReportStopRequest:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
end


LocationProtocol.ConditionQuickGpsAnswer = class.class(KaitaiStruct)

function LocationProtocol.ConditionQuickGpsAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.ConditionQuickGpsAnswer:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.cmd_type = LocationProtocol.CmdTypes(self._io:read_u1())
  self.result = LocationProtocol.ResultCodes(self._io:read_u2be())
end


LocationProtocol.TriggeredReport = class.class(KaitaiStruct)

function LocationProtocol.TriggeredReport:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.TriggeredReport:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.time_remaining = Intervalstring(self._io)
  self.gpsdata = Gpsdata(self._io)
end


LocationProtocol.EmergencyReportStopAnswer = class.class(KaitaiStruct)

function LocationProtocol.EmergencyReportStopAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.EmergencyReportStopAnswer:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
  self.result = LocationProtocol.ResultCodes(self._io:read_u2be())
end


LocationProtocol.TriggeredReportStopRequest = class.class(KaitaiStruct)

function LocationProtocol.TriggeredReportStopRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function LocationProtocol.TriggeredReportStopRequest:_read()
  self.request_id = self._io:read_u4be()
  self.radio_ip = RadioIp(self._io)
end


