#!/usr/bin/env python3

import sys
from glob import glob

from prettyprint import prettyprint

sys.path.append("..")

for hrnp_testfile in sorted(glob("data/hrnp.*")):
    with open(hrnp_testfile, "rb") as file:
        print("----------")
        print(hrnp_testfile)
        from hytera_common.hrnp import HRNPPacket

        packet = HRNPPacket(file.read())
        prettyprint(packet.packet)
