#!/usr/bin/env python3
import os
import sys

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.kaitai.location_protocol import LocationProtocol
from hytera_homebrew_bridge.tests.common import parse_test_data


def test_basic_location_report():
    datastring = (
        "a0020032000000010a2110dd000041313833363438323631303"
        "1354e343731382e383035314530313835342e34333837302e313132310b0300"
    )

    location: LocationProtocol = LocationProtocol.from_bytes(bytes.fromhex(datastring))

    assert location.data.gpsdata.gps_status == b"A"


if __name__ == "__main__":
    datapath = "%s/data/location_protocol.*" % os.path.dirname(
        os.path.realpath(__file__)
    )
    parse_test_data(class_name=LocationProtocol, glob_string=datapath)
