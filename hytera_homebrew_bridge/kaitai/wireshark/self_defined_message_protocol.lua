-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")
local str_decode = require("string_decode")

require("radio_ip")
SelfDefinedMessageProtocol = class.class(KaitaiStruct)

SelfDefinedMessageProtocol.ServiceTypes = enum.Enum {
  private_work_order = 172,
  private_work_order_ack = 173,
  private_short_data = 174,
  private_short_data_ack = 175,
  group_work_order = 188,
  group_work_order_ack = 189,
  group_short_data = 190,
  group_short_data_ack = 191,
}

SelfDefinedMessageProtocol.WorkStates = enum.Enum {
  new = 0,
  delete = 1,
  decline = 16,
  state_1 = 32,
  state_2 = 33,
  state_3 = 34,
  state_4 = 35,
  state_5 = 36,
}

SelfDefinedMessageProtocol.AckFlags = enum.Enum {
  ack_required = 0,
  ack_not_required = 1,
}

SelfDefinedMessageProtocol.OptionFlags = enum.Enum {
  option_len_and_field_disabled = 0,
  option_len_and_field_enabled = 1,
}

SelfDefinedMessageProtocol.ResultCodes = enum.Enum {
  ok = 0,
  fail = 1,
  invalid_params = 3,
  channel_busy = 4,
  rx_only = 5,
  low_battery = 6,
  pll_unlock = 7,
  private_call_no_ack = 8,
  repeater_wakeup_fail = 9,
  no_contact = 10,
  tx_deny = 11,
  tx_interrupted = 12,
}

function SelfDefinedMessageProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function SelfDefinedMessageProtocol:_read()
  self.ack_flag = SelfDefinedMessageProtocol.AckFlags(self._io:read_bits_int_be(1))
  self.option_flag = SelfDefinedMessageProtocol.OptionFlags(self._io:read_bits_int_be(1))
  self.reserved = self._io:read_bits_int_be(6)
  self._io:align_to_byte()
  self.service_type = SelfDefinedMessageProtocol.ServiceTypes(self._io:read_u1())
  self.message_length = self._io:read_u2be()
  if self.option_flag.value == 1 then
    self.option_field_len = self._io:read_u2be()
  end
  self.request_id = self._io:read_u4be()
  self.destination_ip = RadioIp(self._io)
  if self.is_ack_service ~= 1 then
    self.source_ip = RadioIp(self._io)
  end
  if self.is_ack_service == 1 then
    self.result = SelfDefinedMessageProtocol.ResultCodes(self._io:read_u1())
  end
  if  ((self.is_ack_service == 0) and (self.is_work_order == 1))  then
    self.work_order = SelfDefinedMessageProtocol.WorkOrder(self._io, self, self._root)
  end
  if  ((self.is_ack_service == 0) and (self.is_short_data == 1))  then
    self.short_data = str_decode.decode(self._io:read_bytes_term(0, false, true, true), "UTF16-LE")
  end
  if self.option_flag.value == 1 then
    self.option_field = str_decode.decode(self._io:read_bytes(self.option_field_len), "UTF16-LE")
  end
end

SelfDefinedMessageProtocol.property.is_ack_service = {}
function SelfDefinedMessageProtocol.property.is_ack_service:get()
  if self._m_is_ack_service ~= nil then
    return self._m_is_ack_service
  end

  self._m_is_ack_service =  ((self.service_type == SelfDefinedMessageProtocol.ServiceTypes.private_work_order_ack) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.group_work_order_ack) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.private_short_data_ack) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.group_short_data_ack)) 
  return self._m_is_ack_service
end

SelfDefinedMessageProtocol.property.is_work_order = {}
function SelfDefinedMessageProtocol.property.is_work_order:get()
  if self._m_is_work_order ~= nil then
    return self._m_is_work_order
  end

  self._m_is_work_order =  ((self.service_type == SelfDefinedMessageProtocol.ServiceTypes.private_work_order) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.private_work_order_ack) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.group_work_order) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.group_work_order_ack)) 
  return self._m_is_work_order
end

SelfDefinedMessageProtocol.property.is_short_data = {}
function SelfDefinedMessageProtocol.property.is_short_data:get()
  if self._m_is_short_data ~= nil then
    return self._m_is_short_data
  end

  self._m_is_short_data =  ((self.service_type == SelfDefinedMessageProtocol.ServiceTypes.private_short_data) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.private_short_data_ack) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.group_short_data) or (self.service_type == SelfDefinedMessageProtocol.ServiceTypes.group_short_data_ack)) 
  return self._m_is_short_data
end

-- 
-- option fields might not be supported yet.
-- 
-- length of the message from next field to the end of SDMP message.
-- 
-- destination, either single or group ID in ipv4 format.

SelfDefinedMessageProtocol.Date = class.class(KaitaiStruct)

function SelfDefinedMessageProtocol.Date:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function SelfDefinedMessageProtocol.Date:_read()
  self.year = self._io:read_u2be()
  self.month = self._io:read_u1()
  self.day = self._io:read_u1()
end


SelfDefinedMessageProtocol.WorkOrder = class.class(KaitaiStruct)

function SelfDefinedMessageProtocol.WorkOrder:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function SelfDefinedMessageProtocol.WorkOrder:_read()
  self.work_order_header = self._io:read_bytes(4)
  if not(self.work_order_header == "\255\255\255\255") then
    error("not equal, expected " ..  "\255\255\255\255" .. ", but got " .. self.work_order_header)
  end
  self.date = SelfDefinedMessageProtocol.Date(self._io, self, self._root)
  self.sequence_number = self._io:read_u4be()
  self.work_state = SelfDefinedMessageProtocol.WorkStates(self._io:read_u2be())
  self.reserved = self._io:read_bytes(38)
  self.contents = str_decode.decode(self._io:read_bytes_term(0, false, true, true), "UTF16-LE")
end


