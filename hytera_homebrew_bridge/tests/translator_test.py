#!/usr/bin/env python3
import asyncio
import os
import sys
from asyncio import Queue
from binascii import unhexlify

import pytest
from kaitaistruct import KaitaiStruct

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.lib.hytera_mmdvm_translator import HyteraMmdvmTranslator
from hytera_homebrew_bridge.lib.settings import BridgeSettings
from hytera_homebrew_bridge.lib.utils import parse_hytera_data


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

    asyncio.create_task(translator.translate_from_mmdvm())
    asyncio.create_task(translator.translate_from_hytera())

    # testcase 1
    hytera_input: bytes = unhexlify(
        "5a5a5a5a072c000041000501010000001111cccc111100004013fc9655e07d83c44095585"
        "adee19ae61e8abd2d8e93ce71a5daf4340322cfaf5600f955e001006f00000009382300"
    )
    hytera_parsed: KaitaiStruct = parse_hytera_data(hytera_input)
    mmdvm_output: bytes = unhexlify(
        "444d52440123380900006f00000000010000000096fce055837d40c45895de5a9ae11ee6bd"
        "8a8e2dce93a571f4da0334cf2256aff9"
    )

    await hytera_incoming.put(hytera_parsed)
    mmdvm_translated: bytes = await mmdvm_outgoing.get()
    # Null out StreamID for sake of this testcase
    mmdvm_translated = mmdvm_translated[0:16] + bytes(4) + mmdvm_translated[20:]

    assert mmdvm_output == mmdvm_translated

    # testcase 2
    mmdvm_input: bytes = unhexlify("")


if __name__ == "__main__":
    asyncio.run(test_mmdv_to_hytera())
