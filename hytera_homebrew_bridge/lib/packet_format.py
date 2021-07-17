#!/usr/bin/env python3
import io
import zlib
from binascii import hexlify

from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm

mmdvm_frame_types: dict = {0: "VOICE", 1: "VOICE SYNC", 2: "DATA SYNC", 3: "UNUSED"}

mmdvm_data_types_data: dict = {
    0: "PI HEADER",
    1: "VOICE LC HDR",
    2: "TERMINATOR LC",
    3: "CSBK",
    4: "MBC HEADER",
    5: "MBC CONTINUE",
    6: "DATA HEADER",
    7: "DATA 1/2 RATE",
    8: "DATA 3/4 RATE",
    9: "IDLE",
    10: "DATA 1 RATE",
    11: "UNIFIED DATA",
}

mmdvm_data_types_voice: dict = {
    0: "VOICE A",
    1: "VOICE B",
    2: "VOICE C",
    3: "VOICE D",
    4: "VOICE E",
    5: "VOICE F",
}

ipsc_frame_types: dict = {
    0x1111: "VOICE SYNC",
    0x3333: "DATA SYNC | CSBK",
    0xEEEE: "SYNC",
    0x6666: "DATA HEADER",
    0x0000: "DATA",
    0xFFFF: "UNKNOWN 0xFFFF",
}

ipsc_data_types: dict = {
    0x0000: "PI HEADER",
    0x1111: "VOICE LC HDR",
    0x2222: "TERMINATOR LC",
    0x3333: "CSBK",
    0x4444: "DATA HEADER",
    0x5555: "DATA 1/2 RATE",
    0x6666: "DATA 3/4 RATE",
    0x7777: "VOICE C",
    0x8888: "VOICE D",
    0x9999: "VOICE E",
    0xAAAA: "VOICE F",
    0xBBBB: "VOICE A",
    0xCCCC: "VOICE B",
    0xDDDD: "WAKEUP",
    0xEEEE: "SYNC",
}


def _terminal_col256(text, fg=None, bg=None, bold=False):
    def _terminal_get_color(col):
        return "8;5;{0:d}".format(_to_terminal_color(col))

    def _to_terminal_color(num):
        if isinstance(num, int):
            # Assume it is already a color
            return num

        if isinstance(num, str) and len(num) <= 3:
            return 16 + int(num, 6)

        raise ValueError("Invalid color: {0!r}".format(num))

    if not isinstance(text, str):
        text = repr(text)

    buf = io.StringIO()

    if bold:
        buf.write("\x1b[1m")

    if fg is not None:
        buf.write("\x1b[3{0}m".format(_terminal_get_color(fg)))

    if bg is not None:
        buf.write("\x1b[4{0}m".format(_terminal_get_color(bg)))

    buf.write(text)
    buf.write("\x1b[0m")
    return buf.getvalue()


def format_brackets(
    text: str, padding: str = " ", align: str = "<", width: int = 10
) -> str:
    return f"[{text:{padding}{align}{width}}] "


def get_dmr_data_hash(dmrdata: bytes) -> str:
    return hexlify(
        (zlib.crc32(dmrdata) & 0xFFFFFFFF).to_bytes(length=4, byteorder="big")
    ).decode("UTF-8")


def format_mmdvm_data(mmdvm: Mmdvm.TypeDmrData) -> str:
    data_type: str = format_brackets(
        text=(
            mmdvm_data_types_data.get(mmdvm.data_type)
            if mmdvm.frame_type == 2
            else mmdvm_data_types_voice.get(mmdvm.data_type)
        ),
        width=14,
    )
    return (
        format_brackets(text=f"TS" + ("2" if mmdvm.slot_no else "1"), width=3)
        + format_brackets(text="PRIVATE" if mmdvm.call_type else "GROUP", width=7)
        + format_brackets(text=mmdvm_frame_types.get(mmdvm.frame_type, "N/A"), width=13)
        + data_type
        + f"[SEQ {mmdvm.sequence_no: <3}] "
        + f"[{mmdvm.source_id} -> {mmdvm.target_id}] "
        + f"[STREAM {mmdvm.stream_id}] "
    )


def format_ipsc_data(ipsc: IpSiteConnectProtocol) -> str:
    return (
        format_brackets(
            text=f"TS"
            + (
                "1"
                if ipsc.timeslot_raw == IpSiteConnectProtocol.Timeslots.timeslot_1
                else "2"
            ),
            width=3,
        )
        + format_brackets(
            text="PRIVATE"
            if ipsc.call_type == IpSiteConnectProtocol.CallTypes.private_call
            else "GROUP",
            width=7,
        )
        + format_brackets(
            text=ipsc_frame_types.get(
                0 if isinstance(ipsc.frame_type, int) else ipsc.frame_type.value,
                f"Unkown Frame Type {ipsc.frame_type}",
            ),
            width=13,
        )
        + format_brackets(
            text=ipsc_data_types.get(ipsc.slot_type.value, "Unknown Data Type"),
            width=14,
        )
        + f"[SEQ {ipsc.sequence_number: <3}] "
        + f"[{ipsc.source_radio_id} -> {ipsc.destination_radio_id}] "
    )


def common_log_format(
    proto: str,
    dmrdata_hash: str,
    from_ip_port: tuple,
    to_ip_port: tuple,
    packet_data: any,
    use_color: bool = False,
) -> str:
    if isinstance(packet_data, IpSiteConnectProtocol):
        packet_data_formatted = format_ipsc_data(packet_data)
        color = 110
    elif isinstance(packet_data, Mmdvm.TypeDmrData):
        packet_data_formatted = format_mmdvm_data(packet_data)
        color = 120
    else:
        packet_data_formatted = (
            f"Unsupported common_log_format for data {type(packet_data).__name__}"
        )
        color = 1

    if len(from_ip_port) > 1:
        ip_from_to = format_brackets(
            text=f" {from_ip_port[0]: <15} {from_ip_port[1]: <5} -> {to_ip_port[0]: <15} {to_ip_port[1]: <5} "
        )
    else:
        ip_from_to = ""

    log: str = f"{proto} {dmrdata_hash} " + ip_from_to + packet_data_formatted
    return _terminal_col256(log, color) if use_color else log
