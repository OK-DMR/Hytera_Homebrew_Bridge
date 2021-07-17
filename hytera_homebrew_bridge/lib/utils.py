#!/usr/bin/env python3
import logging
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
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.kaitai.real_time_transport_protocol import (
    RealTimeTransportProtocol,
)


def byteswap_bytes(data: bytes) -> bytes:
    return byteswap_bytearray(bytearray(data))


def half_byte_to_bytes(half_byte: int, output_bytes: int = 2) -> bytes:
    return bytes([half_byte | half_byte << 4]) * output_bytes


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
        or bytedata[20] == bytedata[21]  # color code shall be same in both bytes
    ):
        if bytedata[5:9] == bytes([0x00, 0x00, 0x00, 0x14]):
            return IpSiteConnectHeartbeat.from_bytes(bytedata)
        else:
            return IpSiteConnectProtocol.from_bytes(bytedata)
    else:
        # HDAP
        return HyteraDmrApplicationProtocol.from_bytes(bytedata)


def assemble_hytera_ipsc_sync_packet(
    is_private_call: bool,
    source_id: int,
    target_id: int,
    timeslot_is_ts1: bool,
    sequence_number: int,
    color_code: int = 1,
) -> bytes:
    source_id_sync_bytes: bytes = source_id.to_bytes(3, byteorder="big")
    source_id_sync_bytes = bytes(
        [
            source_id_sync_bytes[0],
            0,
            source_id_sync_bytes[1],
            0,
            source_id_sync_bytes[2],
            0,
        ]
    )
    target_id_sync_bytes: bytes = target_id.to_bytes(3, byteorder="big")
    target_id_sync_bytes = bytes(
        [
            target_id_sync_bytes[0],
            0,
            target_id_sync_bytes[1],
            0,
            target_id_sync_bytes[2],
            0,
        ]
    )
    return (
        # IPSC packet header
        b"\x5a\x5a\x5a\x5a"
        + sequence_number.to_bytes(1, byteorder="little")
        + bytes(3)
        # magic
        + b"\x42\x00\x05\x01"
        # timeslot
        + (b"\x01" if timeslot_is_ts1 else b"\x02")
        + bytes(3)
        # timeslot
        + (b"\x11\x11" if timeslot_is_ts1 else b"\x22\x22")
        # slot type
        + b"\xEE\xEE"
        # color code
        + half_byte_to_bytes(half_byte=color_code, output_bytes=2)
        # 1111 => voice sync, 3333 => data sync
        + b"\x11\x11"
        + b"\x40"
        + bytes(7)
        + target_id_sync_bytes
        + source_id_sync_bytes
        + bytes(14)
        + bytes(4)
        + (b"\x00" if is_private_call else b"\x01")
        + bytes(1)
        + target_id.to_bytes(3, byteorder="little")
        + bytes(1)
        + source_id.to_bytes(3, byteorder="little")
        + bytes(1)
    )


def assemble_hytera_ipsc_wakeup_packet(
    timeslot_is_ts1: bool,
    source_id: int,
    target_id: int = 2293760,
    is_private_call: bool = True,
    color_code: int = 1,
) -> bytes:
    return (
        b"\x5a\x5a\x5a\x5a"
        + bytes(4)
        +
        # magic
        b"\x42\x00\x05\x01"
        +
        # timeslot = wakeup
        (b"\x01" if timeslot_is_ts1 else b"\x02")
        + bytes(3)
        +
        # timeslot
        (b"\x11\x11" if timeslot_is_ts1 else b"\x22\x22")
        +
        # slot type
        b"\xDD\xDD"
        +
        # color code
        half_byte_to_bytes(half_byte=color_code, output_bytes=2)
        +
        # is ipsc sync?
        b"\x00\x00"
        + b"\x40"
        + bytes(11)
        + b"\x01\x00\x02\x00\x02\x00\x01"
        + bytes(13)
        + b"\xff\xff\xef\x08\x2a\x00"
        + (b"\x00" if is_private_call else b"\x01")
        + bytes(1)
        + target_id.to_bytes(3, byteorder="little")
        + bytes(1)
        + source_id.to_bytes(3, byteorder="little")
        + bytes(1)
    )


def assemble_hytera_ipsc_packet(
    udp_port: int,
    sequence_number: int,
    timeslot_is_ts1: bool,
    hytera_slot_type: int,
    dmr_payload: bytes,
    is_private_call: bool,
    source_id: int,
    target_id: int,
    color_code: int,
) -> bytes:
    return (
        b"\x5a\x5a\x5a\x5a"
        +
        # sequence_number
        sequence_number.to_bytes(1, byteorder="little")
        +
        # reserved_3
        b"\xE0\x00\x00"
        +
        # packet type
        b"\x01"
        +
        # reserved_7a
        b"\x00\x05\x01"
        + (b"\x01" if timeslot_is_ts1 else b"\x02")
        + b"\x00\x00\x00"
        +
        # timeslot_raw
        (b"\x11\x11" if timeslot_is_ts1 else b"\x22\x22")
        +
        # slot_type
        hytera_slot_type.to_bytes(2, byteorder="little")
        +
        # color code
        half_byte_to_bytes(half_byte=color_code, output_bytes=2)
        +
        # frame_type
        b"\x00\x00"
        +
        # reserved_2a
        b"\x40\x5C"
        +
        # payload data
        dmr_payload
        +
        # two byte crc16 checksum
        b"\x00\x00"
        +
        # reserved_2b
        b"\x63\x02"
        +
        # call_type, mmdvm true = private, ipsc 00 = private
        (b"\x00" if is_private_call else b"\x01")
        + b"\x00"
        +
        # destination id
        target_id.to_bytes(3, byteorder="little")
        + b"\x00"
        +
        # source id
        source_id.to_bytes(3, byteorder="little")
        +
        # reserved_1b
        b"\x00"
    )


def log_mmdvm_configuration(logger: logging.Logger, packet: Mmdvm) -> None:
    if not isinstance(packet.command_data, Mmdvm.TypeRepeaterConfigurationOrClosing):
        return
    if not isinstance(packet.command_data.data, Mmdvm.TypeRepeaterConfiguration):
        return

    c: Mmdvm.TypeRepeaterConfiguration = packet.command_data.data
    log = (
        "-------- MMDVM CONFIGURATION PACKET --------\n"
        f"Repeater ID\t| {c.repeater_id}\n"
        f"Callsign\t| {c.call_sign}\n"
        f"Frequence RX\t| {c.rx_freq} Hz\n"
        f"Frequence TX\t| {c.tx_freq} Hz\n"
        f"TX Power\t| {c.tx_power}\n"
        f"Color-Code\t| {c.color_code}\n"
        f"Latitude\t| {c.latitude}\n"
        f"Longitude\t| {c.longitude}\n"
        f"Location\t| {c.location}\n"
        f"Description\t| {c.description}\n"
        f"Slots\t\t| {2 if c.slots == '3' else 1}\n"
        f"URL\t\t| {c.url}\n"
        f"Software ID\t| {c.software_id}\n"
        f"Package ID\t| {c.package_id}\n"
        "-------- MMDVM CONFIGURATION PACKET --------"
    )
    for line in log.splitlines():
        logger.info(line)
