#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace

from kaitaistruct import KaitaiStruct
from kamene.all import *
from kamene.layers.inet import UDP, IP
from kamene.layers.inet6 import IPv6
from okdmr.kaitai.hytera.real_time_transport_protocol import RealTimeTransportProtocol

from hytera_homebrew_bridge.dmrlib.packet_utils import try_parse_packet
from hytera_homebrew_bridge.lib.packet_format import common_log_format

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )


def arguments() -> ArgumentParser:
    parser = ArgumentParser(
        description="Read and debug UDP packets in PCAP/PCAPNG file"
    )
    parser.add_argument("file", type=str, help="PCAP or PCAPNG file to be read")
    parser.add_argument(
        "--hide-unknown",
        "-u",
        action="store_true",
        help="Hide uknown packets (default is showing them)",
    )
    parser.add_argument(
        "--ports",
        "-p",
        dest="filter_ports",
        default=-1,
        type=int,
        nargs="+",
        help="Filter specific port(s)",
    )
    parser.add_argument(
        "--no-rttp",
        "-n",
        action="store_true",
        help="Will suppress RTTP/RTP protocol from tool output",
    )
    return parser


def debug_udp_packet(
    packet: Ether, _args: Namespace, hide_unknown: bool = False
) -> None:
    udp: UDP = packet.getlayer(UDP)
    if not hasattr(udp, "load"):
        return
    if _args.filter_ports != -1:
        if (
            int(udp.dport) not in _args.filter_ports
            and int(udp.sport) not in _args.filter_ports
        ):
            return
    known_packet: KaitaiStruct = try_parse_packet(udpdata=udp.load)
    if _args.no_rttp and isinstance(known_packet, RealTimeTransportProtocol):
        return
    print(udp.load.hex())
    if not known_packet and not hide_unknown:
        print("Unknown UDP packet")
        packet.display()
    else:
        ip: IP = packet.getlayer(IP.name)
        if not ip:
            ip: IPv6 = packet.getlayer(IPv6.name)
        logline = common_log_format(
            proto=known_packet.__class__.__name__,
            from_ip_port=(ip.src, udp.sport),
            to_ip_port=(ip.dst, udp.dport),
            dmrdata_hash="",
            packet_data=known_packet,
            use_color=True,
        )
        if logline:
            print(logline)


def read_pcap(filepath: str, _args: Namespace, hide_unknown: bool = False):
    with PcapReader(filepath) as pcap_reader:
        for pkt in pcap_reader:
            if isinstance(pkt, Ether) and pkt.haslayer(UDP.name):
                debug_udp_packet(packet=pkt, _args=_args, hide_unknown=hide_unknown)


if __name__ == "__main__":
    args = arguments().parse_args(sys.argv[1:])
    print(args)
    read_pcap(args.file, hide_unknown=args.hide_unknown, _args=args)
