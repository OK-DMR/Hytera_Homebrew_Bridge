#!/usr/bin/env python3

import sys
from glob import glob

from prettyprint import prettyprint

sys.path.append("..")

for testfile in sorted(glob("data/location_protocol.*")):
    print("----------")
    print(testfile)
    from kaitai.location_protocol import LocationProtocol

    packet = LocationProtocol.from_file(testfile)
    print(packet.data.radio_ip.radio_id)
    prettyprint(packet)
