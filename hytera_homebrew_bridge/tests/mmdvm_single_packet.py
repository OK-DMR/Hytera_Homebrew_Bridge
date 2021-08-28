#!/usr/bin/env python3
import os
import sys
from binascii import hexlify, b2a_hex

from dmr_utils3.ambe_utils import deinterleave

from hytera_homebrew_bridge.dmrlib.decode import decode_data_burst, decode_complete_lc
from hytera_homebrew_bridge.dmrlib.terminal import BurstInfo, DataType
from hytera_homebrew_bridge.kaitai.dmr_data import DmrData
from hytera_homebrew_bridge.lib.packet_format import format_mmdvm_data

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.tests.prettyprint import prettyprint, _prettyprint
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    print(sys.argv[1])
    packet = Mmdvm.from_bytes(bytes.fromhex(sys.argv[1]))
    if isinstance(packet.command_data, Mmdvm.TypeDmrData):
        print(format_mmdvm_data(packet.command_data))
        decode_data_burst(packet.command_data.dmr_data)

    prettyprint(packet)

    if packet.command_prefix == "DMRD":
        burst: BurstInfo = BurstInfo(packet.command_data.dmr_data)
        burst.debug()
