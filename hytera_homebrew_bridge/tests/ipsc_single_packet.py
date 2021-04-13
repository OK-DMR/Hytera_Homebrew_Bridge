#!/usr/bin/env python3
import os
import sys
from binascii import b2a_hex as ahex, hexlify

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from dmr_utils3.decode import voice_head_term, voice_sync
from hytera_homebrew_bridge.tests.prettyprint import prettyprint
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    packet = IpSiteConnectProtocol.from_bytes(bytes.fromhex(sys.argv[1]))
    print(
        "source id: \t%s\ntarget id: \t%s\ncall type: \t%s\ntimeslot: \t%s\ncolor_code: \t%s\npacket_type: \t%s\nslot_type: \t%s\nframe_type: \t%s\n\n"
        % (
            packet.source_radio_id,
            packet.destination_radio_id,
            IpSiteConnectProtocol.CallTypes(packet.call_type),
            packet.Timeslots(packet.timeslot_raw),
            packet.color_code,
            packet.packet_type,
            packet.slot_type,
            packet.frame_type,
        )
    )

    prettyprint(packet)

    original = bytearray(packet.ipsc_payload)
    # swap bytes
    original[0::2], original[1::2] = original[1::2], original[0::2]

    print(hexlify(original))

    if (
        packet.slot_type == IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header
        or packet.slot_type
        == IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc
    ):
        lc = voice_head_term(bytes(original))
        print(lc)
        print(
            "LC: OPT-{} SRC-{} DST-{}, SLOT TYPE: CC-{} DTYPE-{}".format(
                ahex(lc["LC"][0:3]),
                ahex(lc["LC"][3:6]),
                ahex(lc["LC"][6:9]),
                ahex(lc["CC"]),
                ahex(lc["DTYPE"]),
            )
        )
    elif packet.slot_type == IpSiteConnectProtocol.SlotTypes.slot_type_sync:
        lc = voice_sync(bytes(original))
        print(lc)
