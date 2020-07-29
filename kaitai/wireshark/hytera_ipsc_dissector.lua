ipsc = Proto("H-IPSC", "Hytera IP Site Connect Protocol")

local fields = ipsc.fields
local IpSiteConnectProtocol = require('ip_site_connect_protocol')
local stringstream = require('string_stream')

fields.timeslot = ProtoField.uint8('ipsc.timeslot', 'timeslot')

function ipsc.dissector(buffer, pinfo, tree)
  len = buffer:len()
  if len == 0 then return end

  pinfo.cols.protocol = ipsc.name

  local subtree = tree:add(ipsc, buffer(), "Hytera IP Site Connect Protocol")
  local stringval = tostring(buffer:bytes())
  local stream = stringstream(stringval)
  local _ipsc = IpSiteConnectProtocol:from_string(stringval)

  subtree:add(fields.timeslot, buffer(16, 2))

end

local udp_port = DissectorTable.get("udp.port")
udp_port:add(50001, ipsc)
