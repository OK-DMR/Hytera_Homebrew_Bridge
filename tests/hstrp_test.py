#!/usr/bin/env python3

import sys
from glob import glob
from pprint import pprint

sys.path.append("..")

for testfile in sorted(glob("data/hstrp.*")):
    with open(testfile, "rb") as file:
        from hytera_common.hstrp import HSTRPPacket

        packet = HSTRPPacket(file.read())
        print("----------")
        print(testfile)
        pprint(packet.packet.__dict__)
