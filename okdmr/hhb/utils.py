#!/usr/bin/env python3
import logging

from okdmr.kaitai.homebrew.mmdvm2020 import Mmdvm2020


def half_byte_to_bytes(half_byte: int, output_bytes: int = 2) -> bytes:
    return bytes([half_byte | half_byte << 4]) * output_bytes


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
    sequence_number: int,
    timeslot_is_ts1: bool,
    hytera_slot_type: int,
    dmr_payload: bytes,
    is_private_call: bool,
    source_id: int,
    target_id: int,
    color_code: int,
    frame_type: int,
    packet_type: int,
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
        frame_type.to_bytes(2, byteorder="little")
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


def log_mmdvm_configuration(logger: logging.Logger, packet: Mmdvm2020) -> None:
    if not isinstance(
        packet.command_data, Mmdvm2020.TypeRepeaterConfigurationOrClosing
    ):
        return
    if not isinstance(packet.command_data.data, Mmdvm2020.TypeRepeaterConfiguration):
        return

    c: Mmdvm2020.TypeRepeaterConfiguration = packet.command_data.data
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
