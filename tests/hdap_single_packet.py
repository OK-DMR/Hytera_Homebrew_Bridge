#!/usr/bin/env python3

if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 2:
        print("use as %s <hexstring>" % sys.argv[0])
        exit(0)

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    from tests.prettyprint import prettyprint
    from kaitai.hytera_dmr_application_protocol import HyteraDmrApplicationProtocol

    packet = HyteraDmrApplicationProtocol.from_bytes(bytes.fromhex(sys.argv[1]))
    print(packet)
    print(packet.message_type)
    prettyprint(packet)
