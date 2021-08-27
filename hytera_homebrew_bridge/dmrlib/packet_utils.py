# /usr/bin/env python3
import traceback
from typing import Optional

from kaitaistruct import KaitaiStruct, ValidationNotEqualError

from hytera_homebrew_bridge.kaitai.hytera_dmr_application_protocol import (
    HyteraDmrApplicationProtocol,
)
from hytera_homebrew_bridge.kaitai.hytera_radio_network_protocol import (
    HyteraRadioNetworkProtocol,
)
from hytera_homebrew_bridge.kaitai.hytera_simple_transport_reliability_protocol import (
    HyteraSimpleTransportReliabilityProtocol,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_heartbeat import (
    IpSiteConnectHeartbeat,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.kaitai.real_time_transport_protocol import (
    RealTimeTransportProtocol,
)


def parse_hytera_data(bytedata):
    if len(bytedata) < 2:
        # probably just heartbeat response
        return IpSiteConnectHeartbeat.from_bytes(bytedata)
    elif bytedata[0:2] == bytes([0x32, 0x42]):
        # HSTRP
        return HyteraSimpleTransportReliabilityProtocol.from_bytes(bytedata)
    elif bytedata[0:1] == bytes([0x7E]):
        # HRNP
        return HyteraRadioNetworkProtocol.from_bytes(bytedata)
    elif (int.from_bytes(bytedata[0:1], byteorder="big") & 0x80) == 0x80 and (
        int.from_bytes(bytedata[0:1], byteorder="big") & 0xC0
    ) == 2:
        return RealTimeTransportProtocol.from_bytes(bytedata)
    elif (
        int.from_bytes(bytedata[0:8], byteorder="little") == 0
        or bytedata[0:4] == b"ZZZZ"
        or bytedata[20:22] == bytes([0x11, 0x11])
    ):
        if bytedata[5:9] == bytes([0x00, 0x00, 0x00, 0x14]):
            return IpSiteConnectHeartbeat.from_bytes(bytedata)
        else:
            return IpSiteConnectProtocol.from_bytes(bytedata)
    else:
        # HDAP
        return HyteraDmrApplicationProtocol.from_bytes(bytedata)


def try_parse_packet(udpdata: bytes) -> Optional[KaitaiStruct]:
    # Try Hytera packets first
    try:
        return parse_hytera_data(udpdata)
    except BaseException as e:
        if (
            not isinstance(e, EOFError)
            and not isinstance(e, ValidationNotEqualError)
            and not isinstance(e, UnicodeDecodeError)
        ):
            traceback.print_exc()

    # Try MMDVM/Homebrew packets
    try:
        return Mmdvm.from_bytes(udpdata)
    except BaseException as e:
        if (
            not isinstance(e, EOFError)
            and not isinstance(e, ValidationNotEqualError)
            and not isinstance(e, UnicodeDecodeError)
        ):
            traceback.print_exc()

    print(f"Unknown packet: {udpdata.hex()}")
