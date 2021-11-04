#!/usr/bin/env python3

from bitarray import bitarray
from dmr_utils3.decode import to_bits, to_bytes
from okdmr.kaitai.etsi.dmr_csbk import DmrCsbk
from okdmr.kaitai.etsi.dmr_data import DmrData
from okdmr.kaitai.etsi.dmr_data_header import DmrDataHeader
from okdmr.kaitai.etsi.dmr_ip_udp import DmrIpUdp

from hytera_homebrew_bridge.tests.prettyprint import prettyprint

SYNC_PATTERNS: dict = {
    0x755FD7DF75F7: "bs sourced voice",
    0xDFF57D75DF5D: "bs sourced data",
    0x7F7D5DD57DFD: "ms sourced voice",
    0xD5D7F77FD757: "ms sourced data",
    0x77D55F7DFD77: "ms sourced rc sync",
    0x5D577F7757FF: "tdma direct mode time slot 1 voice",
    0xF7FDD5DDFD55: "tdma direct mode time slot 1 data",
    0x7DFFD5F55D5F: "tdma direct mode time slot 2 voice",
    0xD7557F5FF7F5: "tdma direct mode time slot 2 data",
    0xDD7FF5D757DD: "reserved sync pattern (future)",
}


def as_int(bytedata: bytes, byteorder: str = "little") -> int:
    return int.from_bytes(bytedata, byteorder)


def decode_complete_lc(_data):
    binlc = bitarray(endian="big")
    binlc.extend(
        [
            _data[136],
            _data[121],
            _data[106],
            _data[91],
            _data[76],
            _data[61],
            _data[46],
            _data[31],
            _data[152],
            _data[137],
            _data[122],
            _data[107],
            _data[92],
            _data[77],
            _data[62],
            _data[47],
            _data[32],
            _data[17],
            _data[2],
            _data[123],
            _data[108],
            _data[93],
            _data[78],
            _data[63],
            _data[48],
            _data[33],
            _data[18],
            _data[3],
            _data[184],
            _data[169],
            _data[94],
            _data[79],
            _data[64],
            _data[49],
            _data[34],
            _data[19],
            _data[4],
            _data[185],
            _data[170],
            _data[155],
            _data[140],
            _data[65],
            _data[50],
            _data[35],
            _data[20],
            _data[5],
            _data[186],
            _data[171],
            _data[156],
            _data[141],
            _data[126],
            _data[111],
            _data[36],
            _data[21],
            _data[6],
            _data[187],
            _data[172],
            _data[157],
            _data[142],
            _data[127],
            _data[112],
            _data[97],
            _data[82],
            _data[7],
            _data[188],
            _data[173],
            _data[158],
            _data[143],
            _data[128],
            _data[113],
            _data[98],
            _data[83],
            _data[68],
            _data[53],
            _data[174],
            _data[159],
            _data[144],
            _data[129],
            _data[114],
            _data[99],
            _data[84],
            _data[69],
            _data[54],
            _data[39],
            _data[24],
            _data[145],
            _data[130],
            _data[115],
            _data[100],
            _data[85],
            _data[70],
            _data[55],
            _data[40],
            _data[25],
            _data[10],
            _data[191],
        ]
    )
    return binlc


def decode_csbk(csbk: bytes):
    csbk_kaitai = DmrCsbk.from_bytes(csbk)
    print(prettyprint(csbk_kaitai))


def decode_data_header(hdr: bytes):
    as_struct = DmrDataHeader.from_bytes(hdr)
    print(prettyprint(as_struct.data))


def decode_data_burst(dmr_data: bytes):
    burst = to_bits(dmr_data)
    burst_info = burst[0:98] + burst[166:272]
    burst_slot_type = burst[98:108] + burst[156:166]
    burst_sync = burst[108:156]
    burst_sync_signature = SYNC_PATTERNS.get(
        as_int(to_bytes(burst_sync), "big"),
        f"Embedded Signalling {to_bytes(burst_sync).hex().upper()}",
    )
    link_control = decode_complete_lc(burst_info).tobytes()
    color_code = as_int(to_bytes(burst_slot_type[0:4]))
    data_type = as_int(to_bytes(burst_slot_type[4:8]))
    fec_parity = to_bytes(burst_slot_type[8:20])
    print(
        f"[Color Code: {color_code}] [Data Type: {data_type}] [FEC Parity: {fec_parity.hex()}] [Sync: {burst_sync_signature}]"
    )
    if data_type == 3:
        decode_csbk(link_control)
    elif data_type == 6:
        decode_data_header(link_control)
    elif data_type == 7:
        print(prettyprint(DmrIpUdp.UdpIpv4CompressedHeader.from_bytes(link_control)))
        print(prettyprint(DmrData.Rate12Unconfirmed.from_bytes(link_control)))
