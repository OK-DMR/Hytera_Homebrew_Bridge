#!/usr/bin/env python3
import string


def byteswap_bytes(data: bytes) -> bytes:
    return byteswap_bytearray(bytearray(data))


def byteswap_bytearray(data: bytearray) -> bytes:
    trim = len(data)
    # add padding, that will get removed, to have odd number of bytes
    if len(data) % 2 != 0:
        data += 0x00
    data[0::2], data[1::2] = data[1::2], data[0::2]
    return bytes(data)[:trim]


def octet_string_to_utf8(octets: str) -> str:
    return "".join(filter(lambda c: c in string.printable, octets))
