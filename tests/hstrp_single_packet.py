#!/usr/bin/env python3

import sys

sys.path.append("..")

from tests.prettyprint import prettyprint

if len(sys.argv) < 2:
    print("use as %s <hexstring>" % sys.argv[0])
    exit(0)

from kaitai.hytera_simple_transport_reliability_protocol import HyteraSimpleTransportReliabilityProtocol

packet = HyteraSimpleTransportReliabilityProtocol.from_bytes(bytes.fromhex(sys.argv[1]))
prettyprint(packet)
