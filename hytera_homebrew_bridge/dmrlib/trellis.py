#!/usr/bin/env python3
from array import array

from bitarray import bitarray
from dmr_utils3.decode import to_bytes

TRELLIS_34_INTERLEAVE_MATRIX = [
    0,
    1,
    8,
    9,
    16,
    17,
    24,
    25,
    32,
    33,
    40,
    41,
    48,
    49,
    56,
    57,
    64,
    65,
    72,
    73,
    80,
    81,
    88,
    89,
    96,
    97,
    2,
    3,
    10,
    11,
    18,
    19,
    26,
    27,
    34,
    35,
    42,
    43,
    50,
    51,
    58,
    59,
    66,
    67,
    74,
    75,
    82,
    83,
    90,
    91,
    4,
    5,
    12,
    13,
    20,
    21,
    28,
    29,
    36,
    37,
    44,
    45,
    52,
    53,
    60,
    61,
    68,
    69,
    76,
    77,
    84,
    85,
    92,
    93,
    6,
    7,
    14,
    15,
    22,
    23,
    30,
    31,
    38,
    39,
    46,
    47,
    54,
    55,
    62,
    63,
    70,
    71,
    78,
    79,
    86,
    87,
    94,
    95,
]

TRELLIS_34_ENCODER_STATE_TRANSITION = [
    0,
    8,
    4,
    12,
    2,
    10,
    6,
    14,
    4,
    12,
    2,
    10,
    6,
    14,
    0,
    8,
    1,
    9,
    5,
    13,
    3,
    11,
    7,
    15,
    5,
    13,
    3,
    11,
    7,
    15,
    1,
    9,
    3,
    11,
    7,
    15,
    1,
    9,
    5,
    13,
    7,
    15,
    1,
    9,
    5,
    13,
    3,
    11,
    2,
    10,
    6,
    14,
    0,
    8,
    4,
    12,
    6,
    14,
    0,
    8,
    4,
    12,
    2,
    10,
]

TRELLIS_34_DIBITS = {(0, 1): 3, (0, 0): 1, (1, 0): -1, (1, 1): -3}

TRELLIS_34_CONSTELLATION_POINTS = {
    (1, -1): 0,
    (-1, -1): 1,
    (3, -3): 2,
    (-3, -3): 3,
    (-3, -1): 4,
    (3, -1): 5,
    (-1, -3): 6,
    (1, -3): 7,
    (-3, 3): 8,
    (3, 3): 9,
    (-1, 1): 10,
    (1, 1): 11,
    (1, 3): 12,
    (-1, 3): 13,
    (3, 1): 14,
    (-3, 1): 15,
}


def t34_make_dibits(stream: bitarray) -> array:
    if len(stream) != 196:
        raise Exception("t34_make_dibits expects 196 bits in bitarray")

    out: array = array("b", [0] * 98)

    for i in range(0, 196, 2):
        o = int(i / 2)
        out[o] = TRELLIS_34_DIBITS[(stream[i], stream[i + 1])]

    return out


def t34_deinterleave(original: array) -> array:
    out: array = array("b", [0] * 98)

    for i in range(0, 98):
        out[TRELLIS_34_INTERLEAVE_MATRIX[i]] = original[i]

    return out


def t34_constellation_points(deinterleaved: array) -> array:
    out: array = array("b", [0] * 49)

    for i in range(0, 98, 2):
        o = int(i / 2)
        out[o] = TRELLIS_34_CONSTELLATION_POINTS[
            (deinterleaved[i], deinterleaved[i + 1])
        ]

    return out


def t34_extract_tribits(constellation_points: array) -> array:
    out: array = array("b", [0] * 48)
    last: int = 0

    for i in range(48):
        start = last * 8
        matches = False

        for j in range(start, start + 8):
            if constellation_points[i] == TRELLIS_34_ENCODER_STATE_TRANSITION[j]:
                matches = True
                last = abs((j - start) % 255)
                out[i] = last

        if not matches:
            raise Exception(
                f"Trellis data corrupted, point {i} constellation {constellation_points[i]}"
            )

    return out


def t34_tribits_to_binary(tribits: array) -> bitarray:
    if len(tribits) != 48:
        raise Exception(f"Expected 48 tribits got {len(tribits)}")

    out: bitarray = bitarray(196 * "0", endian="big")

    for i in range(0, 144, 3):
        o = int(i / 3)
        out[i] = (tribits[o] & 0x4) > 0
        out[i + 1] = (tribits[o] & 0x2) > 0
        out[i + 2] = (tribits[o] & 0x1) > 0

    return out


def trellis_34_decode(encoded: bitarray) -> bitarray:
    if not len(encoded) == 196:
        raise Exception(
            f"Trellis 3/4 decoder needs at least 18 bytes (196 bits), got {len(encoded)}"
        )
    dibits: array = t34_make_dibits(encoded)
    deinterleaved: array = t34_deinterleave(dibits)
    points: array = t34_constellation_points(deinterleaved)
    tribits: array = t34_extract_tribits(points)
    decoded: bitarray = t34_tribits_to_binary(tribits)
    return decoded


def trellis_34_decode_as_bytes(encoded: bitarray) -> bytes:
    bits: bitarray = trellis_34_decode(encoded)
    return to_bytes(bits + bitarray("0000"))
