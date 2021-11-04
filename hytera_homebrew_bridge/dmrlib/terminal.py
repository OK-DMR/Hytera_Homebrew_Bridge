#!/usr/bin/env python3
from typing import Dict

from hytera_homebrew_bridge.dmrlib.burst_info import BurstInfo
from hytera_homebrew_bridge.dmrlib.timeslot import Timeslot
from hytera_homebrew_bridge.dmrlib.transmission_type import TransmissionType


class Terminal:
    def __init__(self, dmrid: int, callsign: str = ""):
        self.id: int = dmrid
        self.call: str = callsign
        self.timeslots: Dict[int, Timeslot] = {
            1: Timeslot(timeslot=1),
            2: Timeslot(timeslot=2),
        }

    def set_callsign_alias(self, newalias: str):
        self.call = newalias

    def process_dmr_data(self, dmrdata: bytes, timeslot: int) -> BurstInfo:
        burst = BurstInfo(data=dmrdata)
        return self.timeslots[timeslot].process_burst(burst)

    def get_status(self) -> TransmissionType:
        for tsdata in self.timeslots.values():
            return tsdata.transmission.type
        return TransmissionType.Idle

    def debug(self, printout: bool = True) -> str:
        status: str = f"[ID: {self.id}] [CALL: {self.call}]\n"
        for ts in self.timeslots.values():
            status += "\t" + ts.debug(False) + "\n"

        if printout:
            print(status)
        return status
