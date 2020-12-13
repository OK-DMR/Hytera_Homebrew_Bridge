-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")
local str_decode = require("string_decode")

require("radio_ip")
TextMessageProtocol = class.class(KaitaiStruct)

TextMessageProtocol.AckFlags = enum.Enum {
  ack_required = 0,
  ack_not_required = 1,
}

TextMessageProtocol.OptionFlags = enum.Enum {
  option_len_and_field_disabled = 0,
  option_len_and_field_enabled = 1,
}

TextMessageProtocol.ServiceTypes = enum.Enum {
  send_private_message = 161,
  send_private_message_ack = 162,
  send_group_message = 177,
  send_group_message_ack = 178,
}

TextMessageProtocol.ResultCodes = enum.Enum {
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

function TextMessageProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function TextMessageProtocol:_read()
  self.ack_flag = TextMessageProtocol.AckFlags(self._io:read_bits_int_be(1))
  self.option_flag = TextMessageProtocol.OptionFlags(self._io:read_bits_int_be(1))
  self.reserved = self._io:read_bits_int_be(6)
  self._io:align_to_byte()
  self.service_type = TextMessageProtocol.ServiceTypes(self._io:read_u1())
  self.message_length = self._io:read_u2be()
  if self.option_flag.value == 1 then
    self.option_field_len = self._io:read_u2be()
  end
  self.request_id = self._io:read_u4be()
  self.destination_ip = RadioIp(self._io)
  if self.service_type ~= TextMessageProtocol.ServiceTypes.send_group_message_ack then
    self.source_ip = RadioIp(self._io)
  end
  if  ((self.service_type == TextMessageProtocol.ServiceTypes.send_private_message_ack) or (self.service_type == TextMessageProtocol.ServiceTypes.send_group_message_ack))  then
    self.result = TextMessageProtocol.ResultCodes(self._io:read_u1())
  end
  if  ((self.service_type == TextMessageProtocol.ServiceTypes.send_private_message) or (self.service_type == TextMessageProtocol.ServiceTypes.send_group_message))  then
    self.tmdata = str_decode.decode(self._io:read_bytes_term(0, false, true, true), "UTF16-LE")
  end
  if self.option_flag.value == 1 then
    self.option_field = str_decode.decode(self._io:read_bytes(self.option_field_len), "UTF16-LE")
  end
end

-- 
-- option fields might not be supported yet.
-- 
-- length of the message from next field to the end of TMP message.
-- 
-- single or group target in ipv4 format.
-- 
-- source of the message in ipv4 format.

