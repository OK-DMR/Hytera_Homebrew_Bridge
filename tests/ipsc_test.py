#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
    from tests.common import parse_test_data

    datapath = "%s/data/ipsc.*" % os.path.dirname(os.path.realpath(__file__))
    parse_test_data(class_name=IpSiteConnectProtocol, glob_string=datapath)
