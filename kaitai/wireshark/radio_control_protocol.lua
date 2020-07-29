-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")

RadioControlProtocol = class.class(KaitaiStruct)

RadioControlProtocol.ServiceTypes = enum.Enum {
  call_request = 2113,
  call_reply = 34881,
}

RadioControlProtocol.CallTypes = enum.Enum {
  private_call = 0,
  group_call = 1,
  all_call = 2,
  emergency_group_call = 3,
  remote_monitor_call = 4,
  reserved = 5,
  priority_private_call = 6,
  priority_group_call = 7,
  priority_all_call = 8,
}

RadioControlProtocol.CallReplyResults = enum.Enum {
  success = 0,
  failure = 1,
}

function RadioControlProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RadioControlProtocol:_read()
  self.service_type = RadioControlProtocol.ServiceTypes(self._io:read_u2le())
  self.message_length = self._io:read_u2le()
  local _on = self.service_type
  if _on == RadioControlProtocol.ServiceTypes.call_request then
    self.data = RadioControlProtocol.CallRequest(self._io, self, self._root)
  elseif _on == RadioControlProtocol.ServiceTypes.call_reply then
    self.data = RadioControlProtocol.CallReply(self._io, self, self._root)
  else
    self.data = RadioControlProtocol.GenericData(self._io, self, self._root)
  end
end

-- 
-- length of the message from next field to the end of RCP message.

RadioControlProtocol.CallRequest = class.class(KaitaiStruct)

function RadioControlProtocol.CallRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RadioControlProtocol.CallRequest:_read()
  self.call_type = RadioControlProtocol.CallTypes(self._io:read_u1())
  self.target_id = self._io:read_u4le()
end

-- 
-- ignored for all_call.

RadioControlProtocol.CallReply = class.class(KaitaiStruct)

function RadioControlProtocol.CallReply:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RadioControlProtocol.CallReply:_read()
  self.result = RadioControlProtocol.CallReplyResults(self._io:read_u1())
end


RadioControlProtocol.GenericData = class.class(KaitaiStruct)

function RadioControlProtocol.GenericData:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function RadioControlProtocol.GenericData:_read()
  self.data = self._io:read_bytes(self._parent.message_length)
end


