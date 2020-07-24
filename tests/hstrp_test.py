#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from kaitai.hytera_simple_transport_reliability_protocol import (
        HyteraSimpleTransportReliabilityProtocol,
    )
    from tests.common import parse_test_data

    datapath = "%s/data/hstrp.*" % os.path.dirname(os.path.realpath(__file__))
    parse_test_data(
        class_name=HyteraSimpleTransportReliabilityProtocol, glob_string=datapath
    )
