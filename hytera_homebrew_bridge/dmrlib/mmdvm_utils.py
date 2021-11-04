#!/usr/bin/env python3
from bitarray import bitarray
from okdmr.kaitai.homebrew.mmdvm2020 import Mmdvm2020
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol

from hytera_homebrew_bridge.dmrlib.burst_info import BurstInfo
from hytera_homebrew_bridge.dmrlib.data_type import DataType


def get_mmdvm_timeslot(mmdvmdata: Mmdvm2020.TypeDmrData) -> int:
    return 1 if mmdvmdata.slot_no == Mmdvm2020.Timeslots.timeslot_1 else 2


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


DMR_DATA_TYPE_TO_IPSC_SLOT_TYPE: dict = {
    DataType.VoiceBurstA: IpSiteConnectProtocol.SlotTypes.slot_type_data_c,
    DataType.VoiceBurstB: IpSiteConnectProtocol.SlotTypes.slot_type_data_d,
    DataType.VoiceBurstC: IpSiteConnectProtocol.SlotTypes.slot_type_data_e,
    DataType.VoiceBurstD: IpSiteConnectProtocol.SlotTypes.slot_type_data_f,
    DataType.VoiceBurstE: IpSiteConnectProtocol.SlotTypes.slot_type_data_a,
    DataType.VoiceBurstF: IpSiteConnectProtocol.SlotTypes.slot_type_data_b,
    DataType.VoiceLCHeader: IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header,
    DataType.Rate34DataContinuation: IpSiteConnectProtocol.SlotTypes.slot_type_rate_34_data,
    DataType.Rate12DataContinuation: IpSiteConnectProtocol.SlotTypes.slot_type_rate_12_data,
    DataType.CSBK: IpSiteConnectProtocol.SlotTypes.slot_type_csbk,
    DataType.DataHeader: IpSiteConnectProtocol.SlotTypes.slot_type_data_header,
    DataType.PrivacyIndicatorHeader: IpSiteConnectProtocol.SlotTypes.slot_type_privacy_indicator,
    DataType.TerminatorWithLC: IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc,
}

DMR_DATA_TYPE_TO_IPSC_FRAME_TYPE: dict = {
    DataType.VoiceBurstA: IpSiteConnectProtocol.FrameTypes.frame_type_voice,
    DataType.VoiceBurstB: IpSiteConnectProtocol.FrameTypes.frame_type_voice,
    DataType.VoiceBurstC: IpSiteConnectProtocol.FrameTypes.frame_type_voice_sync,
    DataType.VoiceBurstD: IpSiteConnectProtocol.FrameTypes.frame_type_voice,
    DataType.VoiceBurstE: IpSiteConnectProtocol.FrameTypes.frame_type_voice,
    DataType.VoiceBurstF: IpSiteConnectProtocol.FrameTypes.frame_type_voice,
    DataType.VoiceLCHeader: IpSiteConnectProtocol.FrameTypes.frame_type_data_header,
    DataType.Rate34DataContinuation: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataType.Rate12DataContinuation: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataType.CSBK: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataType.DataHeader: IpSiteConnectProtocol.FrameTypes.frame_type_data_header,
    DataType.PrivacyIndicatorHeader: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataType.TerminatorWithLC: IpSiteConnectProtocol.FrameTypes.frame_type_data,
}


def get_ipsc_frame_type(burst: BurstInfo) -> int:
    return DMR_DATA_TYPE_TO_IPSC_FRAME_TYPE.get(
        burst.data_type, IpSiteConnectProtocol.FrameTypes.frame_type_voice
    ).value


def get_ipsc_slot_type(burst: BurstInfo) -> int:
    return DMR_DATA_TYPE_TO_IPSC_SLOT_TYPE.get(
        burst.data_type, IpSiteConnectProtocol.SlotTypes.slot_type_data_a
    ).value
