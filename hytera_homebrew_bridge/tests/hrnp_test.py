#!/usr/bin/env python3
import os
import sys

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

if __name__ == "__main__":
    from hytera_homebrew_bridge.kaitai.hytera_radio_network_protocol import (
        HyteraRadioNetworkProtocol,
    )
    from hytera_homebrew_bridge.tests.common import parse_test_data

    datapath = "%s/data/hrnp.*" % os.path.dirname(os.path.realpath(__file__))
    parse_test_data(class_name=HyteraRadioNetworkProtocol, glob_string=datapath)
