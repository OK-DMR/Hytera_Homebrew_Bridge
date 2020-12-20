#!/usr/bin/env python3
import os
import sys

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.tests.prettyprint import prettyprint
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    print("MMDVM (2020) packet")

    packet = Mmdvm.from_bytes(bytes.fromhex(sys.argv[1]))
    prettyprint(packet)
