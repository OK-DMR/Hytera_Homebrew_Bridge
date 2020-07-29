-- This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
--
-- This file is compatible with Lua 5.3

local class = require("class")
require("kaitaistruct")
local enum = require("enum")
local str_decode = require("string_decode")

require("radio_ip")
DataTransmitProtocol = class.class(KaitaiStruct)

DataTransmitProtocol.ServiceTypes = enum.Enum {
  data_transmit_protocol = 160,
}

DataTransmitProtocol.ServiceSpecificTypes = enum.Enum {
  dtp_request = 1,
  data_slice_trasmit = 2,
  last_data_slice = 3,
  dtp_answer = 17,
  data_slice_answer = 18,
  last_data_slice_answer = 19,
}

DataTransmitProtocol.Results = enum.Enum {
  success = 0,
  failure = 1,
}

function DataTransmitProtocol:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DataTransmitProtocol:_read()
  self.service_type = DataTransmitProtocol.ServiceTypes(self._io:read_u1())
  self.service_specific_type = DataTransmitProtocol.ServiceSpecificTypes(self._io:read_u1())
  self.message_length = self._io:read_u2be()
  local _on = self.service_specific_type
  if _on == DataTransmitProtocol.ServiceSpecificTypes.dtp_request then
    self.data = DataTransmitProtocol.DtpRequest(self._io, self, self._root)
  elseif _on == DataTransmitProtocol.ServiceSpecificTypes.data_slice_transmit then
    self.data = DataTransmitProtocol.DataSliceTransmit(self._io, self, self._root)
  elseif _on == DataTransmitProtocol.ServiceSpecificTypes.data_slice_answer then
    self.data = DataTransmitProtocol.DataSliceAnswer(self._io, self, self._root)
  elseif _on == DataTransmitProtocol.ServiceSpecificTypes.last_data_slice_answer then
    self.data = DataTransmitProtocol.LastDataSliceAnswer(self._io, self, self._root)
  elseif _on == DataTransmitProtocol.ServiceSpecificTypes.dtp_answer then
    self.data = DataTransmitProtocol.DtpAnswer(self._io, self, self._root)
  elseif _on == DataTransmitProtocol.ServiceSpecificTypes.last_data_slice then
    self.data = DataTransmitProtocol.LastDataSlice(self._io, self, self._root)
  end
end

-- 
-- should be always 0xA0 Data Transmit Protocol.
-- 
-- length of the message from next field to the end of DTP message.

-- 
-- sent by transmit source, requires answer from the destination.
DataTransmitProtocol.LastDataSlice = class.class(KaitaiStruct)

function DataTransmitProtocol.LastDataSlice:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DataTransmitProtocol.LastDataSlice:_read()
  self.destination_ip = RadioIp(self._io)
  self.source_ip = RadioIp(self._io)
end

-- 
-- transmit recipient ip.
-- 
-- transmit sender ip.

DataTransmitProtocol.DtpRequest = class.class(KaitaiStruct)

function DataTransmitProtocol.DtpRequest:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DataTransmitProtocol.DtpRequest:_read()
  self.destination_ip = RadioIp(self._io)
  self.source_ip = RadioIp(self._io)
  self.file_size = self._io:read_u2be()
  self.file_name = str_decode.decode(self._io:read_bytes((self._parent.message_length - 10)), "UTF16-LE")
end

-- 
-- size in bytes.
-- 
-- maximum of 256 bytes including file extension, if longer, recipient should refuse the transmission.

DataTransmitProtocol.DataSliceAnswer = class.class(KaitaiStruct)

function DataTransmitProtocol.DataSliceAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DataTransmitProtocol.DataSliceAnswer:_read()
  self.destination_ip = RadioIp(self._io)
  self.source_ip = RadioIp(self._io)
  self.block_number = self._io:read_u2be()
  self.result = DataTransmitProtocol.Results(self._io:read_u1())
end

-- 
-- sequence number in transfer, same as data_slice_transmit.block_number the response is for.
-- 
-- result of transmit from receiving end.

DataTransmitProtocol.DataSliceTransmit = class.class(KaitaiStruct)

function DataTransmitProtocol.DataSliceTransmit:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DataTransmitProtocol.DataSliceTransmit:_read()
  self.destination_ip = RadioIp(self._io)
  self.source_ip = RadioIp(self._io)
  self.block_number = self._io:read_u2be()
  self.file_data = self._io:read_bytes((self._parent.message_length - 10))
end

-- 
-- sequence number in transfer, starting with 1.
-- 
-- 448 bytes slice of transmitted file, or shorter if current slice is the last one.

DataTransmitProtocol.LastDataSliceAnswer = class.class(KaitaiStruct)

function DataTransmitProtocol.LastDataSliceAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DataTransmitProtocol.LastDataSliceAnswer:_read()
  self.destination_ip = RadioIp(self._io)
  self.source_ip = RadioIp(self._io)
  self.result = DataTransmitProtocol.Results(self._io:read_u1())
end

-- 
-- transmit sender ip.
-- 
-- transmit recipient ip.

DataTransmitProtocol.DtpAnswer = class.class(KaitaiStruct)

function DataTransmitProtocol.DtpAnswer:_init(io, parent, root)
  KaitaiStruct._init(self, io)
  self._parent = parent
  self._root = root or self
  self:_read()
end

function DataTransmitProtocol.DtpAnswer:_read()
  self.destination_ip = RadioIp(self._io)
  self.source_ip = RadioIp(self._io)
  self.result = DataTransmitProtocol.Results(self._io:read_u1())
end


