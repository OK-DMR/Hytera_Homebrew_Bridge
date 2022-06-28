#!/usr/bin/env python3
import os

from okdmr.kaitai.hytera.hytera_radio_network_protocol import HyteraRadioNetworkProtocol
from okdmr.kaitai.hytera.hytera_simple_transport_reliability_protocol import (
    HyteraSimpleTransportReliabilityProtocol,
)
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol
from okdmr.kaitai.hytera.location_protocol import LocationProtocol

from hytera_homebrew_bridge.tests.common import parse_test_data


def test_lp_bins():
    datapath = "%s/data/location_protocol.*" % os.path.dirname(
        os.path.realpath(__file__)
    )
    parse_test_data(class_name=LocationProtocol, glob_string=datapath)


def test_hrnp_bins():
    datapath = "%s/data/hrnp.*" % os.path.dirname(os.path.realpath(__file__))
    parse_test_data(class_name=HyteraRadioNetworkProtocol, glob_string=datapath)


def test_hstrp_bins():
    datapath = "%s/data/hstrp.*" % os.path.dirname(os.path.realpath(__file__))
    parse_test_data(
        class_name=HyteraSimpleTransportReliabilityProtocol, glob_string=datapath
    )


def test_ipsc_bins():
    datapath = "%s/data/ipsc.*" % os.path.dirname(os.path.realpath(__file__))
    parse_test_data(class_name=IpSiteConnectProtocol, glob_string=datapath)
