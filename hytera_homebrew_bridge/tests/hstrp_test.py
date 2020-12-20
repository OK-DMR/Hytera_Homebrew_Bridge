#!/usr/bin/env python3
import os
import sys

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.kaitai.hytera_simple_transport_reliability_protocol import (
    HyteraSimpleTransportReliabilityProtocol,
)
from hytera_homebrew_bridge.tests.common import parse_test_data

if __name__ == "__main__":
    datapath = "%s/data/hstrp.*" % os.path.dirname(os.path.realpath(__file__))
    parse_test_data(
        class_name=HyteraSimpleTransportReliabilityProtocol, glob_string=datapath
    )
