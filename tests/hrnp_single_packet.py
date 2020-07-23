#!/usr/bin/env python3

import sys

sys.path.append("..")

from tests.prettyprint import prettyprint

if len(sys.argv) < 2:
    print("use as ./hrnp_single_packet <hexstring>")
    exit(0)

from kaitai.hytera_radio_network_protocol import HyteraRadioNetworkProtocol

packet = HyteraRadioNetworkProtocol.from_bytes(bytes.fromhex(sys.argv[1]))
prettyprint(packet)
