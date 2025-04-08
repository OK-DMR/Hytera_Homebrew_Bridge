#!/usr/bin/env python3
from typing import Dict, Union

from bitarray import bitarray
from okdmr.dmrlib.etsi.layer2.burst import Burst
from okdmr.dmrlib.etsi.layer2.elements.data_types import DataTypes
from okdmr.dmrlib.etsi.layer2.elements.voice_bursts import VoiceBursts
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol


def get_ipsc_timeslot(ipscdata: IpSiteConnectProtocol) -> int:
    return (
        1 if ipscdata.timeslot_raw == IpSiteConnectProtocol.Timeslots.timeslot_1 else 2
    )


def int_to_bitstring(val: int, minlength: int = 4) -> str:
    return "{1:0{0}b}".format(minlength, val)


def get_mmdvm_bitflags(burst: Burst, packet: IpSiteConnectProtocol) -> bytes:
    flags: bitarray = bitarray()
    # timeslot
    flags.append(1 if get_ipsc_timeslot(packet) == 2 else 0)
    # group/private
    flags.append(
        1 if packet.call_type == IpSiteConnectProtocol.CallTypes.private_call else 0
    )

    if burst.is_vocoder:
        assert burst.voice_burst != VoiceBursts.Unknown
        # 01 is voice sync
        # 00 voice data
        # 10 data or data sync
        # 11 unused
        flags.extend("01" if burst.voice_burst == VoiceBursts.VoiceBurstA else "00")
        # 0 is VoiceBurst A, 1 is VoiceBurst B, etc...
        flags.extend(
            int_to_bitstring(burst.voice_burst.value - VoiceBursts.VoiceBurstA)
        )
    else:
        # frame type 10 is data or data sync
        flags.extend("10")
        # data type is the real value from burst
        flags.extend(int_to_bitstring(int(burst.data_type.value)))

    return flags.tobytes()


DMR_DATA_TYPE_TO_IPSC_SLOT_TYPE: Dict[
    Union[DataTypes, VoiceBursts], IpSiteConnectProtocol.SlotTypes
] = {
    VoiceBursts.VoiceBurstA: IpSiteConnectProtocol.SlotTypes.slot_type_data_a,
    VoiceBursts.VoiceBurstB: IpSiteConnectProtocol.SlotTypes.slot_type_data_b,
    VoiceBursts.VoiceBurstC: IpSiteConnectProtocol.SlotTypes.slot_type_data_c,
    VoiceBursts.VoiceBurstD: IpSiteConnectProtocol.SlotTypes.slot_type_data_d,
    VoiceBursts.VoiceBurstE: IpSiteConnectProtocol.SlotTypes.slot_type_data_e,
    VoiceBursts.VoiceBurstF: IpSiteConnectProtocol.SlotTypes.slot_type_data_f,
    DataTypes.VoiceLCHeader: IpSiteConnectProtocol.SlotTypes.slot_type_voice_lc_header,
    DataTypes.Rate34Data: IpSiteConnectProtocol.SlotTypes.slot_type_rate_34_data,
    DataTypes.Rate12Data: IpSiteConnectProtocol.SlotTypes.slot_type_rate_12_data,
    DataTypes.Rate1Data: IpSiteConnectProtocol.SlotTypes.slot_type_rate_12_data,
    DataTypes.CSBK: IpSiteConnectProtocol.SlotTypes.slot_type_csbk,
    DataTypes.DataHeader: IpSiteConnectProtocol.SlotTypes.slot_type_data_header,
    DataTypes.PIHeader: IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc,
    DataTypes.TerminatorWithLC: IpSiteConnectProtocol.SlotTypes.slot_type_terminator_with_lc,
}

DMR_DATA_TYPE_TO_IPSC_FRAME_TYPE: Dict[
    Union[VoiceBursts, DataTypes], IpSiteConnectProtocol.FrameTypes
] = {
    VoiceBursts.VoiceBurstA: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    VoiceBursts.VoiceBurstB: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    VoiceBursts.VoiceBurstC: IpSiteConnectProtocol.FrameTypes.frame_type_voice_sync,
    VoiceBursts.VoiceBurstD: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    VoiceBursts.VoiceBurstE: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    VoiceBursts.VoiceBurstF: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataTypes.VoiceLCHeader: IpSiteConnectProtocol.FrameTypes.frame_type_data_header,
    DataTypes.Rate34Data: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataTypes.Rate12Data: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataTypes.Rate1Data: IpSiteConnectProtocol.SlotTypes.slot_type_rate_12_data,
    DataTypes.CSBK: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataTypes.DataHeader: IpSiteConnectProtocol.FrameTypes.frame_type_data_header,
    DataTypes.PIHeader: IpSiteConnectProtocol.FrameTypes.frame_type_data,
    DataTypes.TerminatorWithLC: IpSiteConnectProtocol.FrameTypes.frame_type_data,
}

DMR_DATA_TYPE_TO_IPSC_PACKET_TYPE: Dict[
    Union[VoiceBursts, DataTypes], IpSiteConnectProtocol.PacketTypes
] = {
    VoiceBursts.VoiceBurstA: IpSiteConnectProtocol.PacketTypes.a,
    VoiceBursts.VoiceBurstB: IpSiteConnectProtocol.PacketTypes.a,
    VoiceBursts.VoiceBurstC: IpSiteConnectProtocol.PacketTypes.b,
    VoiceBursts.VoiceBurstD: IpSiteConnectProtocol.PacketTypes.a,
    VoiceBursts.VoiceBurstE: IpSiteConnectProtocol.PacketTypes.a,
    VoiceBursts.VoiceBurstF: IpSiteConnectProtocol.PacketTypes.a,
    DataTypes.VoiceLCHeader: IpSiteConnectProtocol.PacketTypes.a,
    DataTypes.Rate34Data: IpSiteConnectProtocol.PacketTypes.a,
    DataTypes.Rate12Data: IpSiteConnectProtocol.PacketTypes.a,
    DataTypes.Rate1Data: IpSiteConnectProtocol.PacketTypes.a,
    DataTypes.CSBK: IpSiteConnectProtocol.PacketTypes.a,
    DataTypes.DataHeader: IpSiteConnectProtocol.PacketTypes.a,
    DataTypes.PIHeader: IpSiteConnectProtocol.PacketTypes.a,
    DataTypes.TerminatorWithLC: IpSiteConnectProtocol.PacketTypes.terminator,
}


def get_ipsc_packet_type(burst: Burst) -> int:
    return DMR_DATA_TYPE_TO_IPSC_PACKET_TYPE.get(
        burst.voice_burst if burst.is_vocoder else burst.data_type,
        IpSiteConnectProtocol.PacketTypes.a,
    ).value


def get_ipsc_frame_type(burst: Burst) -> int:
    return DMR_DATA_TYPE_TO_IPSC_FRAME_TYPE.get(
        burst.voice_burst if burst.is_vocoder else burst.data_type,
        IpSiteConnectProtocol.FrameTypes.frame_type_voice,
    ).value


def get_ipsc_slot_type(burst: Burst) -> int:
    return DMR_DATA_TYPE_TO_IPSC_SLOT_TYPE.get(
        burst.voice_burst if burst.is_vocoder else burst.data_type,
        IpSiteConnectProtocol.SlotTypes.slot_type_data_a,
    ).value
