#!/usr/bin/env python3
import os
import sys

from okdmr.kaitai.homebrew.mmdvm2020 import Mmdvm2020

from hytera_homebrew_bridge.dmrlib.decode import decode_data_burst
from hytera_homebrew_bridge.dmrlib.terminal import BurstInfo
from hytera_homebrew_bridge.lib.packet_format import format_mmdvm_data

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.tests.prettyprint import prettyprint

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    print(sys.argv[1])
    packet = Mmdvm2020.from_bytes(bytes.fromhex(sys.argv[1]))
    if isinstance(packet.command_data, Mmdvm2020.TypeDmrData):
        print(format_mmdvm_data(packet.command_data))
        decode_data_burst(packet.command_data.dmr_data)

    prettyprint(packet)

    if packet.command_prefix == "DMRD":
        burst: BurstInfo = BurstInfo(packet.command_data.dmr_data)
        burst.debug()
