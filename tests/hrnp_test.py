#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    print(sys.path)

    from kaitai.hytera_radio_network_protocol import HyteraRadioNetworkProtocol
    from tests.common import parse_test_data

    datapath = "%s/data/hrnp.*" % os.path.dirname(os.path.realpath(__file__))
    parse_test_data(class_name=HyteraRadioNetworkProtocol, glob_string=datapath)
