#!/usr/bin/env python3

import sys
from glob import glob
from prettyprint import prettyprint

sys.path.append("..")

for testfile in sorted(glob("data/hstrp.*")):
    with open(testfile, "rb") as file:
        print("----------")
        print(testfile)
        from hytera_common.hstrp import HSTRPPacket

        packet = HSTRPPacket(file.read())
        prettyprint(packet.packet)
