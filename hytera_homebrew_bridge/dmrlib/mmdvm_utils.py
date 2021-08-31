#!/usr/bin/env python3
from bitarray import bitarray

from hytera_homebrew_bridge.dmrlib.terminal import BurstInfo, DataType
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm


def get_mmdvm_timeslot(mmdvmdata: Mmdvm.TypeDmrData) -> int:
    return 1 if mmdvmdata.slot_no == Mmdvm.Timeslots.timeslot_1 else 2


def get_ipsc_timeslot(ipscdata: IpSiteConnectProtocol) -> int:
    return (
        1 if ipscdata.timeslot_raw == IpSiteConnectProtocol.Timeslots.timeslot_1 else 2
    )


def int_to_bitstring(val: int, minlength: int = 4) -> str:
    return "{1:0{0}b}".format(minlength, val)


def get_mmdvm_bitflags(burst: BurstInfo, packet: IpSiteConnectProtocol) -> bytes:
    flags: bitarray = bitarray()
    # timeslot
    flags.append(1 if get_ipsc_timeslot(packet) == 2 else 0)
    # group/private
    flags.append(
        1 if packet.call_type == IpSiteConnectProtocol.CallTypes.private_call else 0
    )
    if burst.data_type in [
        DataType.VoiceBurstB,
        DataType.VoiceBurstC,
        DataType.VoiceBurstD,
        DataType.VoiceBurstE,
        DataType.VoiceBurstF,
    ]:
        # frame type
        flags.extend("00")
        # data type
        flags.extend(
            int_to_bitstring(burst.data_type.value - DataType.VoiceBurstA.value)
        )
    elif burst.data_type in [DataType.VoiceBurstA]:
        # frame type
        flags.extend("01")
        # data type
        flags.extend(
            int_to_bitstring(burst.data_type.value - DataType.VoiceBurstA.value)
        )
    else:
        # frame type
        flags.extend("10")
        # data type
        flags.extend(int_to_bitstring(burst.data_type.value))

    return flags.tobytes()
