#!/usr/bin/env python3
import os
import sys

from okdmr.kaitai.etsi.dmr_data_header import DmrDataHeader
from okdmr.kaitai.etsi.link_control import LinkControl
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol

from hytera_homebrew_bridge.dmrlib.burst_info import BurstInfo
from hytera_homebrew_bridge.dmrlib.data_type import DataType
from hytera_homebrew_bridge.dmrlib.decode import decode_complete_lc
from hytera_homebrew_bridge.lib.packet_format import format_ipsc_data
from hytera_homebrew_bridge.lib.utils import byteswap_bytes

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.tests.prettyprint import prettyprint, _prettyprint

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    packet = IpSiteConnectProtocol.from_bytes(bytes.fromhex(sys.argv[1]))

    print(format_ipsc_data(packet))

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

    burst = BurstInfo(data=byteswap_bytes(packet.ipsc_payload))
    burst.debug()
    if burst.data_type == DataType.TerminatorWithLC:
        info_bytes = decode_complete_lc(burst.info_bits)
        print(_prettyprint(LinkControl.from_bytes(info_bytes)))
    elif burst.data_type == DataType.DataHeader:
        info_bytes = decode_complete_lc(burst.info_bits)
        print(_prettyprint(DmrDataHeader.from_bytes(info_bytes)))
