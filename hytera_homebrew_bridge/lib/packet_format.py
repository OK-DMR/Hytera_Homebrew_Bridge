#!/usr/bin/env python3
import base64
import io
import zlib
from binascii import hexlify

from dmr_utils3.decode import voice_head_term
from okdmr.kaitai.homebrew.mmdvm2020 import Mmdvm2020
from okdmr.kaitai.hytera.hytera_radio_network_protocol import HyteraRadioNetworkProtocol
from okdmr.kaitai.hytera.hytera_simple_transport_reliability_protocol import (
    HyteraSimpleTransportReliabilityProtocol,
)
from okdmr.kaitai.hytera.ip_site_connect_heartbeat import IpSiteConnectHeartbeat
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol
from okdmr.kaitai.hytera.real_time_transport_protocol import RealTimeTransportProtocol

from hytera_homebrew_bridge.lib.utils import byteswap_bytes
from hytera_homebrew_bridge.tests.prettyprint import prettyprint

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
    0xBBBB: "VOICE",
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

dmr_data_types: dict = {0: "PI HEADER", 1: "VOICE | DATA", 2: "TERMINATOR LC"}


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


def format_mmdvm_data(mmdvm: Mmdvm2020.TypeDmrData) -> str:
    data_type: str = format_brackets(
        text=(
            mmdvm_data_types_data.get(mmdvm.data_type, "unknown mmdvm")
            if mmdvm.frame_type == 2
            else mmdvm_data_types_voice.get(mmdvm.data_type, "unknown mmdvm voice")
        ),
        width=14,
    )
    dmr_data_type: str = dmr_data_types.get(
        mmdvm.data_type, "DMR DT %d" % int(mmdvm.data_type)
    )
    dmr_data_hash: str = base64.urlsafe_b64encode(mmdvm.dmr_data).decode("ascii")
    return (
        format_brackets(
            text=f"TS"
            + ("2" if mmdvm.slot_no == Mmdvm2020.Timeslots.timeslot_2 else "1"),
            width=3,
        )
        + format_brackets(
            text="PRIVATE"
            if mmdvm.call_type == Mmdvm2020.CallTypes.private_call
            else "GROUP",
            width=7,
        )
        + format_brackets(text=mmdvm_frame_types.get(mmdvm.frame_type, "N/A"), width=13)
        + data_type
        + format_brackets(text=dmr_data_type, width=14)
        + f"[SEQ {mmdvm.sequence_no: <3}] "
        + f"[{mmdvm.source_id} -> {mmdvm.target_id}] "
        + f"[STREAM {mmdvm.stream_id}] "
        + f"[{dmr_data_hash}] "
    )


def format_ipsc_data(ipsc: IpSiteConnectProtocol) -> str:
    if (
        ipsc.slot_type == IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header
        or ipsc.slot_type
        == IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc
    ):
        lc = voice_head_term(byteswap_bytes(ipsc.ipsc_payload))
        dmr_data_type: str = dmr_data_types.get(
            int(lc["DTYPE"][0]), "DMR DT %d" % int(lc["DTYPE"][0])
        )
    else:
        dmr_data_type: str = "DMR DT ?"

    dmr_data_hash: str = base64.urlsafe_b64encode(
        # comparable is only first 33 bytes of dmr payload, 34th byte is endianness leftover
        byteswap_bytes(ipsc.ipsc_payload)[0:-1]
    ).decode("ascii")
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
                -1 if isinstance(ipsc.frame_type, int) else ipsc.frame_type.value,
                f"Unkown Frame Type {ipsc.frame_type}",
            ),
            width=13,
        )
        + format_brackets(
            text=ipsc_data_types.get(
                -1 if isinstance(ipsc.slot_type, int) else ipsc.slot_type.value,
                f"Unknown Data Type {ipsc.slot_type}",
            ),
            width=14,
        )
        + format_brackets(text=dmr_data_type, width=14)
        + f"[SEQ {ipsc.sequence_number: <3}] "
        + f"[{ipsc.source_radio_id} -> {ipsc.destination_radio_id}] "
        + f"[{dmr_data_hash}] "
    )


def common_log_format(
    proto: str,
    dmrdata_hash: str,
    from_ip_port: tuple,
    to_ip_port: tuple,
    packet_data: any,
    use_color: bool = False,
    color_default: int = 7,
    color_ipsc: int = 11,
    color_mmdvm: int = 14,
) -> str:
    packet_data_formatted: str = ""
    color: int = color_default
    prefix_mmdvm: str = "MMDVM"
    prefix_ipsc: str = "IPSC"
    prefix_hrnp: str = "HRNP"
    prefix_hstrp: str = "HSTRP"
    prefix_rttp: str = "RTTP"
    prefix_unknown: str = "UNDEF"
    if not packet_data:
        return ""
    elif isinstance(packet_data, IpSiteConnectProtocol):
        packet_data_formatted = format_ipsc_data(packet_data)
        color = color_ipsc
        proto = prefix_ipsc
    elif isinstance(packet_data, IpSiteConnectHeartbeat):
        packet_data_formatted = "[ IPSC Heartbeat / KeepAlive ]"
        color = color_default
        proto = prefix_ipsc
    elif isinstance(packet_data, HyteraRadioNetworkProtocol):
        packet_data_formatted = str(prettyprint(packet_data))
        color = color_ipsc
        proto = prefix_hrnp
    elif isinstance(packet_data, HyteraSimpleTransportReliabilityProtocol):
        packet_data_formatted = str(prettyprint(packet_data))
        color = color_ipsc
        proto = prefix_hstrp
    elif isinstance(packet_data, Mmdvm2020):
        proto = prefix_mmdvm
        if hasattr(packet_data, "command_data"):
            if isinstance(packet_data.command_data, Mmdvm2020.TypeDmrData):
                packet_data_formatted = format_mmdvm_data(packet_data.command_data)
                color = color_mmdvm
            elif isinstance(packet_data.command_data, Mmdvm2020.TypeUnknown):
                color = color_default
                packet_data_formatted = (
                    f"[ UNKNOWN UDP DATA ] [ {packet_data.command_data.unknown_data} ]"
                )
                proto = prefix_unknown
            else:
                packet_data_formatted = (
                    f"[ {packet_data.command_data.__class__.__name__} ]"
                )
                color = color_default

        if not packet_data_formatted:
            packet_data_formatted += f"[ {packet_data.command_prefix} ]"
            color = color_default
    elif isinstance(packet_data, Mmdvm2020.TypeDmrData):
        proto = prefix_mmdvm
        packet_data_formatted = format_mmdvm_data(packet_data)
        color = color_mmdvm
    elif isinstance(packet_data, RealTimeTransportProtocol):
        proto = prefix_rttp
        color = color_ipsc
        packet_data_formatted = (
            f"[SEQUENCE: {packet_data.fixed_header.sequence_number}] "
            f"[timestamp: {packet_data.fixed_header.timestamp}]"
        )
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

    log: str = f"[ {proto: <5} ] {dmrdata_hash} " + ip_from_to + packet_data_formatted
    return _terminal_col256(log, color) if use_color else log
