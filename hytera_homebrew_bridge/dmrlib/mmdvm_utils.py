#!/usr/bin/env python3
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm


def get_mmdvm_timeslot(mmdvmdata: Mmdvm.TypeDmrData):
    return 1 if mmdvmdata.slot_no == Mmdvm.Timeslots.timeslot_1 else 2
