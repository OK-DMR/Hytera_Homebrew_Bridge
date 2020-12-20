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
from datetime import datetime

import kamene.all
from kamene.layers.l2 import Ether

from pcapng.scanner import FileScanner
from pcapng.blocks import EnhancedPacket
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
from hytera_homebrew_bridge.kaitai.homebrew import Homebrew
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
    text = [
        col256(" Packet+ ", bg="001", fg="345"),
        # col256('NIC:', bold=True),
        # col256(str(block.interface_id), fg='145'),
        col256(str(block.interface.options["if_name"]), fg="140"),
        col256(
            str(
                datetime.utcfromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
            ),
            fg="455",
        ),
    ]
    try:
        text.extend(
            [
                col256("NIC:", bold=True),
                col256(block.interface_id, fg="145"),
                col256(block.interface.options["if_name"], fg="140"),
            ]
        )
    except KeyError:
        pass

    text.extend(
        [
            # col256('Size:', bold=True),
            col256(str(block.packet_len) + " bytes", fg="025")
        ]
    )

    if block.captured_len != block.packet_len:
        text.extend(
            [
                col256("Truncated to:", bold=True),
                col256(str(block.captured_len) + "bytes", fg="145"),
            ]
        )

    text.extend(pprint_options(block.options))
    print(" ".join(text))

    if block.interface.link_type == 1:

        _info = format_kamene_packet(Ether(block.packet_data))
        print("\n".join("    " + line for line in _info))

    else:
        print("        Printing information for non-ethernet packets")
        print("        is not supported yet.")


def format_kamene_packet(packet):
    fields = []
    for f in packet.fields_desc:
        # if isinstance(f, ConditionalField) and not f._evalcond(self):
        #     continue
        if f.name in packet.fields:
            if isinstance(packet.fields[f.name], (bytes, bytearray)):
                val = packet.fields[f.name].hex()
                if packet.__class__.__name__ == "Raw":
                    is_hpd = True
                    is_hbp = True
                    try:
                        hpd = parse_hytera_data(packet.fields[f.name])
                        if hpd:
                            if hasattr(hpd, "extra_data") and hpd.extra_data:
                                print(
                                    "{0}={1}".format(
                                        col256(
                                            hpd.__class__.__name__, bg="001", fg="345"
                                        ),
                                        col256(str(_prettyprint(hpd)), "352"),
                                    )
                                )
                                print("hpd %s has extra data")
                                exit(1)

                            fields.append(
                                "{0}={1}".format(
                                    col256(hpd.__class__.__name__, bg="001", fg="345"),
                                    col256(str(_prettyprint(hpd)), "352"),
                                )
                            )
                    except:
                        is_hpd = False
                    if not is_hpd:
                        try:
                            hbp = Homebrew.from_bytes(packet.fields[f.name])
                            fields.append(
                                "{0}={1}".format(
                                    col256(hbp.command_prefix, bg="001", fg="345"),
                                    col256(str(_prettyprint(hbp)), "352"),
                                )
                            )
                        except:
                            is_hbp = False

                    if not is_hpd and not is_hbp:
                        # not a Hytera or Homebrew packet
                        pass

            else:
                val = f.i2repr(packet, packet.fields[f.name])

        elif f.name in packet.overloaded_fields:
            val = f.i2repr(packet, packet.overloaded_fields[f.name])

        else:
            continue

        fields.append("{0}={1}".format(col256(f.name, "542"), col256(val, "352")))

    yield "{0} {1}".format(col256(packet.__class__.__name__, "501"), " ".join(fields))

    if packet.payload:
        if isinstance(packet.payload, kamene.packet.Packet):
            for line in format_kamene_packet(packet.payload):
                yield "    " + line
        elif isinstance(packet.payload, kamene.packet.Raw):
            for line in format_kamene_packet(packet.payload):
                yield "    " + line
        else:
            for line in repr(packet.payload).splitlines():
                yield "    " + bytes(line).hex()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("use as %s <path-to-pcap-file>" % sys.argv[0])
        exit(0)

    with open(sys.argv[1], "rb") as testfile:
        scanner = FileScanner(testfile)
        counter = 0
        for block in scanner:
            if isinstance(block, EnhancedPacket):
                counter += 1
                pprint_enhanced_packet(block)
        print("{0} packets worked through".format(counter))
