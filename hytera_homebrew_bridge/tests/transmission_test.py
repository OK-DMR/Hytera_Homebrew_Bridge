#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser, Namespace
from binascii import unhexlify
from typing import Optional

from kaitaistruct import KaitaiStruct
from kamene.layers.inet import UDP
from kamene.layers.l2 import Ether
from kamene.utils import PcapReader
from okdmr.kaitai.homebrew.mmdvm2020 import Mmdvm2020
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol

from hytera_homebrew_bridge.dmrlib.packet_utils import try_parse_packet
from hytera_homebrew_bridge.dmrlib.transmission_watcher import TransmissionWatcher
from hytera_homebrew_bridge.tests.prettyprint import prettyprint


def arguments() -> ArgumentParser:
    parser = ArgumentParser(description="Read transmission file(s) and debug")
    parser.add_argument(
        "--hytera",
        dest="hytera",
        action="store_true",
        help="Use only Hytera IPSC packets",
    )
    parser.add_argument(
        "--mmdvm",
        "--homebrew",
        dest="mmdvm",
        action="store_true",
        help="Use only MMDVM/Homebrew packets",
    )
    parser.add_argument(
        "files",
        metavar="file",
        type=str,
        nargs="+",
        help="One or more transmission files in same format",
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="filetype",
        default="pcap",
        choices=["pcap", "pcapng", "hex"],
        help="type of files to read (default: pcap)",
    )
    parser.add_argument(
        "--skip", dest="skip", type=int, default=0, help="number of packets to skip"
    )
    parser.add_argument(
        "--step",
        dest="do_stepping",
        action="store_true",
        default=False,
        help="You will need to press enter key after each parsed packet",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        default=False,
        action="store_true",
        help="Show more verbose output of packet processing process",
    )
    parser.set_defaults(skipped=0, counter=0)
    return parser


def process_packet_bytes(
    packet: bytes, _watcher: TransmissionWatcher, _args: Namespace
):
    # skipping number of packets
    if _args.skip > 0 and _args.skipped < _args.skip:
        _args.skipped += 1
        return

    # try parse, might be NoneType
    packetdata: Optional[KaitaiStruct] = try_parse_packet(packet)

    if _args.hytera and not isinstance(packetdata, IpSiteConnectProtocol):
        return

    if _args.mmdvm and not isinstance(packetdata, Mmdvm2020):
        return

    # log raw hex only if packet is not filtered
    print(packet.hex())

    if packetdata:
        _watcher.process_packet(packetdata, do_debug=_args.verbose)

    if _args.do_stepping:
        input("Press Enter to continue or CTRL+C to end")
        print(f"\033[A                                           \033[A")

    args.counter += 1


def feed_from_file(filepath: str, _watcher: TransmissionWatcher, _args: Namespace):
    with open(filepath, "r") as filehandle:
        for line in filehandle.readlines():
            process_packet_bytes(unhexlify(line.strip()), _watcher, _args)
    _watcher.end_all_transmissions()


def feed_from_pcapng(filepath: str, _watcher: TransmissionWatcher, _args: Namespace):
    with PcapReader(filepath) as pcap_reader:
        for block in pcap_reader:
            if isinstance(block, Ether) and block.haslayer(UDP.name):
                udp = block.getlayer(UDP)
                if not udp:
                    continue
                process_packet_bytes(udp.getfieldval("load"), _watcher, _args)
    _watcher.end_all_transmissions()


if __name__ == "__main__":
    args: Namespace = arguments().parse_args(sys.argv[1:])
    watcher: TransmissionWatcher = TransmissionWatcher()

    for file in args.files:
        if not os.path.isfile(file):
            print(f"File does not exist {file}")
            continue
        if args.filetype == "hex":
            feed_from_file(file, watcher, args)
        elif args.filetype == "pcapng":
            feed_from_pcapng(file, watcher, args)
