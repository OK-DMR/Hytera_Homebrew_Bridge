#!/usr/bin/env python3

import sys

from prettyprint import prettyprint

sys.path.append("..")

if len(sys.argv) < 2:
    print("use as ./hrnp_single_packet <hexstring>")
    exit(0)

from kaitai.ip_site_connect_protocol import IpSiteConnectProtocol

packet = IpSiteConnectProtocol.from_bytes(bytes.fromhex(sys.argv[1]))

print("%s\t%s\tcall:%s\tTS:%s\tpacket_type:%s\tslot_type:%s" % (
    packet.source_radio_id.radio_id,
    packet.destination_radio_id.radio_id,
    packet.call_type,
    packet.Timeslots(packet.timeslot_raw),
    packet.PacketTypes(packet.packet_type),
    packet.slot_type
))
prettyprint(packet)
