#!/usr/bin/env python3
import string

from kaitaistruct import KaitaiStruct

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
from hytera_homebrew_bridge.kaitai.real_time_transport_protocol import (
    RealTimeTransportProtocol,
)


def byteswap_bytes(data: bytes) -> bytes:
    return byteswap_bytearray(bytearray(data))


def byteswap_bytearray(data: bytearray) -> bytes:
    trim = len(data) - 1
    # add padding, that will get removed, to have odd number of bytes
    if len(data) % 2 != 0:
        data.append(0x00)
    data[0::2], data[1::2] = data[1::2], data[0::2]
    return bytes(data[:trim])


def hytpatcher_byte_swap(pl: bytes) -> bytes:
    """
    static slice/join function for swapping the bytes in ambe payload between MMDVM and Hytera
    :rtype: bytes
    :param pl:
    :return: bytes
    """
    return b"".join(
        [
            pl[2:4],
            pl[0:2],
            pl[6:8],
            pl[4:6],
            pl[10:12],
            pl[8:10],
            pl[14:16],
            pl[12:14],
            pl[18:20],
            pl[16:18],
            pl[22:24],
            pl[20:22],
            pl[26:28],
            pl[24:26],
            pl[30:32],
            pl[28:30],
            pl[34:36],
            pl[32:34],
            pl[38:40],
            pl[36:38],
            pl[42:44],
            pl[40:42],
            pl[46:48],
            pl[44:46],
            pl[50:52],
            pl[48:50],
            pl[54:56],
            pl[52:54],
            pl[58:60],
            pl[56:58],
            pl[62:64],
            pl[60:62],
            pl[66:68],
            pl[64:66],
        ]
    )


def octet_string_to_utf8(octets: str) -> str:
    return "".join(filter(lambda c: c in string.printable, octets))


def parse_hytera_data(bytedata: bytes) -> KaitaiStruct:
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
        rtsp = RealTimeTransportProtocol.from_bytes(bytedata)
        return rtsp
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
