#!/usr/bin/env python3
import os
import sys

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

import io
import zlib
from binascii import hexlify

import kamene.all
from kamene.layers.l2 import Ether

from hytera_homebrew_bridge.lib.utils import byteswap_bytes

from pcapng.scanner import FileScanner
from pcapng.blocks import EnhancedPacket
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.kaitai.hytera_dmr_application_protocol import (
    HyteraDmrApplicationProtocol,
)
from hytera_homebrew_bridge.kaitai.hytera_radio_network_protocol import (
    HyteraRadioNetworkProtocol,
)
from hytera_homebrew_bridge.kaitai.hytera_simple_transport_reliability_protocol import (
    HyteraSimpleTransportReliabilityProtocol,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.ip_site_connect_heartbeat import (
    IpSiteConnectHeartbeat,
)
from hytera_homebrew_bridge.kaitai.real_time_transport_protocol import (
    RealTimeTransportProtocol,
)
from hytera_homebrew_bridge.tests.prettyprint import _prettyprint
import kamene.packet


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
        rtsp = RealTimeTransportProtocol.from_bytes(bytedata)
        if rtsp.fixed_header.padding:
            print(
                "{0}={1}".format(
                    col256(rtsp.__class__.__name__, bg="001", fg="345"),
                    col256(str(_prettyprint(rtsp)), "352"),
                )
            )
            print("RTSP %s has padding bytes")
            exit(1)
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


def col256(text, fg=None, bg=None, bold=False):
    def _get_color(col):
        return "8;5;{0:d}".format(_to_color(col))

    def _to_color(num):
        if isinstance(num, int):
            return num  # Assume it is already a color

        if isinstance(num, str) and len(num) <= 3:
            return 16 + int(num, 6)

        raise ValueError("Invalid color: {0!r}".format(num))

    if not isinstance(text, str):
        text = repr(text)

    buf = io.StringIO()

    if bold:
        buf.write("\x1b[1m")

    if fg is not None:
        buf.write("\x1b[3{0}m".format(_get_color(fg)))

    if bg is not None:
        buf.write("\x1b[4{0}m".format(_get_color(bg)))

    buf.write(text)
    buf.write("\x1b[0m")
    return buf.getvalue()


def pprint_options(options):
    if len(options):
        yield "--"
        for key, values in options.iter_all_items():
            for value in values:
                yield col256(key + ":", bold=True, fg="453")
                yield col256(str(value), fg="340")


def make_printable(data):  # todo: preserve unicode
    stream = io.StringIO()
    for ch in data:
        if ch == "\\":
            stream.write("\\\\")
        elif ch in "\n\r" or (32 <= ord(ch) <= 126):
            stream.write(ch)
        else:
            stream.write("\\x{0:02x}".format(ord(ch)))
    return stream.getvalue()


def pprint_enhanced_packet(block):
    if block.interface.link_type == 1:

        _info = format_kamene_packet(Ether(block.packet_data))
        print("\n".join(_info))

    else:
        print("        Printing information for non-ethernet packets")
        print("        is not supported yet.")


def format_kamene_packet(packet, extra_data=None):
    if extra_data is None:
        extra_data = {}

    if packet.__class__.__name__ is "IP":
        extra_data["ip.src"] = packet.fields["src"]
        extra_data["ip.dst"] = packet.fields["dst"]

    elif packet.__class__.__name__ is "UDP":
        extra_data["udp.sport"] = packet.fields["sport"]
        extra_data["udp.dport"] = packet.fields["dport"]

    elif packet.__class__.__name__ is "Raw":
        packet_data = packet.fields["load"]
        packet_data_formatted = hexlify(packet_data)
        packet_hash = ""
        is_hpd = True
        is_hbp = True

        try:
            hpd = parse_hytera_data(packet_data)
            if isinstance(hpd, IpSiteConnectProtocol):
                swap = byteswap_bytes(hpd.ipsc_payload)
                packet_hash = hexlify(
                    (zlib.crc32(swap) & 0xFFFFFFFF).to_bytes(length=4, byteorder="big")
                ).decode("UTF-8")
                packet_data_formatted = (
                    f"HYTD slot-type {hpd.slot_type} frame-type {hpd.frame_type} "
                    f"call-type {hpd.call_type} seq {hpd.sequence_number} "
                    f"FROM: {hpd.source_radio_id} TO: {hpd.destination_radio_id}"
                    f"\n{hexlify(packet_data)}"
                )
        except:
            is_hpd = False

        if not is_hpd:
            try:
                hbp = Mmdvm.from_bytes(packet_data)
                if isinstance(hbp.command_data, Mmdvm.TypeDmrData):
                    packet_hash = hexlify(
                        (zlib.crc32(hbp.command_data.dmr_data) & 0xFFFFFFFF).to_bytes(
                            length=4, byteorder="big"
                        )
                    ).decode("UTF-8")
                    packet_data_formatted = (
                        f"DMRD call-type {hbp.command_data.call_type} "
                        f"frame-type {hbp.command_data.frame_type} "
                        f"data-type {hbp.command_data.data_type} "
                        f"seq {hbp.command_data.sequence_no} "
                        f"FROM: {hbp.command_data.source_id} TO: {hbp.command_data.target_id}"
                        f"\n{hexlify(packet_data)}"
                    )
            except:
                is_hbp = False

        if not is_hpd and not is_hbp:
            # not a Hytera or Homebrew packet
            yield col256(f"[NOT SUPPORTED PACKET] %s" % hexlify(packet_data), 1)
        else:
            yield col256(
                "%s [ %s %s -> %s %s ] %s"
                % (
                    packet_hash,
                    str(extra_data["ip.src"]).ljust(15),
                    str(extra_data["udp.sport"]).ljust(5),
                    str(extra_data["ip.dst"]).ljust(15),
                    str(extra_data["udp.dport"]).ljust(5),
                    packet_data_formatted,
                ),
                123,
            )

    if packet.payload:
        if isinstance(packet.payload, kamene.packet.Packet):
            for line in format_kamene_packet(packet.payload, extra_data):
                yield line
        elif isinstance(packet.payload, kamene.packet.Raw):
            for line in format_kamene_packet(packet.payload, extra_data):
                yield line


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("use as %s <path-to-pcap-file>" % sys.argv[0])
        exit(0)

    print("Supports only IPv4 UDP packets of MMDVM/Homebrew and Hytera IPSC protocols")

    with open(sys.argv[1], "rb") as testfile:
        scanner = FileScanner(testfile)
        counter = 0
        for block in scanner:
            if isinstance(block, EnhancedPacket):
                counter += 1
                pprint_enhanced_packet(block)
        print("{0} packets worked through".format(counter))
