#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from tests.prettyprint import prettyprint
    from kaitai.ip_site_connect_protocol import IpSiteConnectProtocol

    packet = IpSiteConnectProtocol.from_bytes(bytes.fromhex(sys.argv[1]))
    print(
        "source id: \t%s\ntarget id: \t%s\ncall type: \t%s\ntimeslot: \t%s\npacket_type: \t%s\nslot_type: \t%s\n\n"
        % (
            packet.source_radio_id,
            packet.destination_radio_id,
            IpSiteConnectProtocol.CallTypes(packet.call_type),
            packet.Timeslots(packet.timeslot_raw),
            packet.PacketTypes(packet.packet_type),
            packet.slot_type,
        )
    )
    prettyprint(packet)
