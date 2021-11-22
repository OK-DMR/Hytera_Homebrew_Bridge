#!/usr/bin/env python3
import asyncio
import os
import sys
from asyncio import Queue
from binascii import unhexlify

import pytest
from kaitaistruct import KaitaiStruct
from okdmr.kaitai.homebrew.mmdvm2020 import Mmdvm2020
from okdmr.kaitai.hytera.ip_site_connect_protocol import IpSiteConnectProtocol

from hytera_homebrew_bridge.dmrlib.packet_utils import parse_hytera_data
from hytera_homebrew_bridge.lib.packet_format import common_log_format

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.lib.hytera_mmdvm_translator import HyteraMmdvmTranslator
from hytera_homebrew_bridge.lib.settings import BridgeSettings


@pytest.mark.asyncio
async def test_mmdv_to_hytera():
    hytera_incoming: Queue = Queue()
    hytera_outgoing: Queue = Queue()
    mmdvm_incoming: Queue = Queue()
    mmdvm_outgoing: Queue = Queue()
    settings: BridgeSettings = BridgeSettings(filedata=BridgeSettings.MINIMAL_SETTINGS)

    translator: HyteraMmdvmTranslator = HyteraMmdvmTranslator(
        settings=settings,
        hytera_outgoing=hytera_outgoing,
        hytera_incoming=hytera_incoming,
        mmdvm_outgoing=mmdvm_outgoing,
        mmdvm_incoming=mmdvm_incoming,
    )

    t1 = asyncio.create_task(translator.translate_from_mmdvm())
    t2 = asyncio.create_task(translator.translate_from_hytera())

    # testcase 1
    hytera_input: bytes = unhexlify(
        "5a5a5a5a4d2600004100050102000000222233335555000040f95d41430ca0bf743"
        "5d904d028fd9457ff5dd7dcf502ad501259a9e1361a22182c0069430c00003c38230063382300"
    )
    hytera_parsed: KaitaiStruct = parse_hytera_data(hytera_input)
    mmdvm_output: bytes = unhexlify(
        "444d52440123386323383c00000000e300000000415d0c43bfa0357404d928d094fdff57d75df5dcad021250a95936e1221a2c1869"
    )

    await hytera_incoming.put(hytera_parsed)
    mmdvm_translated: bytes = await mmdvm_outgoing.get()
    # Null out StreamID for sake of this testcase
    mmdvm_translated = mmdvm_translated[0:16] + bytes(4) + mmdvm_translated[20:]

    assert mmdvm_output == mmdvm_translated

    t1.cancel()
    t2.cancel()


@pytest.mark.asyncio
async def test_byteswap():
    hytera_incoming: Queue = Queue()
    hytera_outgoing: Queue = Queue()
    mmdvm_incoming: Queue = Queue()
    mmdvm_outgoing: Queue = Queue()
    settings: BridgeSettings = BridgeSettings(filedata=BridgeSettings.MINIMAL_SETTINGS)

    translator: HyteraMmdvmTranslator = HyteraMmdvmTranslator(
        settings=settings,
        hytera_outgoing=hytera_outgoing,
        hytera_incoming=hytera_incoming,
        mmdvm_outgoing=mmdvm_outgoing,
        mmdvm_incoming=mmdvm_incoming,
    )

    t1 = asyncio.create_task(translator.translate_from_mmdvm())
    t2 = asyncio.create_task(translator.translate_from_hytera())

    mmdvm_in: bytes = bytes.fromhex(
        (
            "444d52449428072200000900280722837cd1c462fab9e71"
            "66019c12ee3fab9e7166170a05390f74018c12ee3eab9e7166018c12ee30030"
        )
    )
    mmdvm_in_parsed: Mmdvm2020 = Mmdvm2020.from_bytes(mmdvm_in)
    print(
        common_log_format(
            proto="MMDVM",
            packet_data=mmdvm_in_parsed,
            to_ip_port=("", ""),
            from_ip_port=("", ""),
            dmrdata_hash="",
        )
    )
    await mmdvm_incoming.put(mmdvm_in_parsed)
    hytera_out: bytes = await hytera_outgoing.get()
    hytera_out_parsed: IpSiteConnectProtocol = IpSiteConnectProtocol.from_bytes(
        hytera_out
    )
    print(
        common_log_format(
            proto="IPSC",
            packet_data=hytera_out_parsed,
            to_ip_port=("", ""),
            from_ip_port=("", ""),
            dmrdata_hash="",
        )
    )

    t1.cancel()
    t2.cancel()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_mmdv_to_hytera())
