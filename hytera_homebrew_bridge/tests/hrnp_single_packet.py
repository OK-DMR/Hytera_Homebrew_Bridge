#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from hytera_homebrew_bridge.tests.prettyprint import prettyprint
    from hytera_homebrew_bridge.kaitai.hytera_radio_network_protocol import (
        HyteraRadioNetworkProtocol,
    )

    packet = HyteraRadioNetworkProtocol.from_bytes(bytes.fromhex(sys.argv[1]))
    prettyprint(packet)
