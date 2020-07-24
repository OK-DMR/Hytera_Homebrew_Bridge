#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from tests.prettyprint import prettyprint
    from kaitai.location_protocol import LocationProtocol

    packet = LocationProtocol.from_bytes(bytes.fromhex(sys.argv[1]))
    prettyprint(packet)
