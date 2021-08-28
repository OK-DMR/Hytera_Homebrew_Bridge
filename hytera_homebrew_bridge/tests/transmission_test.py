#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser
from binascii import unhexlify
from typing import Optional

from kaitaistruct import KaitaiStruct
from kamene.layers.inet import UDP
from kamene.layers.l2 import Ether
from kamene.utils import PcapReader

from hytera_homebrew_bridge.dmrlib.packet_utils import try_parse_packet
from hytera_homebrew_bridge.dmrlib.transmission_watcher import TransmissionWatcher


def arguments() -> ArgumentParser:
    parser = ArgumentParser(description="Read transmission file(s) and debug")
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
    return parser


def feed_from_file(filepath: str, _watcher: TransmissionWatcher):
    with open(filepath, "r") as filehandle:
        for line in filehandle.readlines():
            packetdata: Optional[KaitaiStruct] = try_parse_packet(
                unhexlify(line.strip())
            )
            print(line.strip())
            if packetdata:
                _watcher.process_packet(packetdata)


def feed_from_pcapng(filepath: str, _watcher: TransmissionWatcher):
    with PcapReader(filepath) as pcap_reader:
        for block in pcap_reader:
            if isinstance(block, Ether) and block.haslayer(UDP.name):
                udp = block.getlayer(UDP)
                if not udp:
                    continue
                packetdata: Optional[KaitaiStruct] = try_parse_packet(
                    udp.getfieldval("load")
                )
                if packetdata:
                    _watcher.process_packet(packetdata)
    _watcher.end_all_transmissions()


if __name__ == "__main__":
    args = arguments().parse_args(sys.argv[1:])
    watcher: TransmissionWatcher = TransmissionWatcher()

    for file in args.files:
        if not os.path.isfile(file):
            print(f"File does not exist {file}")
            continue
        if args.filetype == "hex":
            feed_from_file(file, watcher)
        elif args.filetype == "pcapng":
            feed_from_pcapng(file, watcher)
