#!/usr/bin/env python3

import sys
from glob import glob
from pprint import pprint

sys.path.append('..')

for hrnp_testfile in sorted(glob('data/hrnp.*')):
    with open(hrnp_testfile, 'rb') as file:
        from hytera_common.hrnp import HRNPPacket

        packet = HRNPPacket(file.read())
        print('----------')
        print(hrnp_testfile)
        print(packet.get_opcode_name())
        pprint(packet.packet.__dict__)
