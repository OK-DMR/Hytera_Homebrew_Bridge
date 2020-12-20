#!/usr/bin/env python3
import os
import sys
from asyncio import Queue
import asyncio

try:
    import hytera_homebrew_bridge
except ImportError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    )

from hytera_homebrew_bridge.lib.hytera_mmdvm_translator import HyteraMmdvmTranslator
from hytera_homebrew_bridge.lib.settings import BridgeSettings

MINIMAL_CONFIG = """
[ip-site-connect]\n
ip = 192.168.1.2
p2p_port = 50000
dmr_port = 50001
rdac_port = 50002

[homebrew]\n
local_ip = 0.0.0.0
master_ip = 127.0.0.1
master_port = 62031
password = S3CR3T
"""


async def test_mmdv_to_hytera():
    hytera_incoming: Queue = Queue()
    hytera_outgoing: Queue = Queue()
    mmdvm_incoming: Queue = Queue()
    mmdvm_outgoing: Queue = Queue()
    settings: BridgeSettings = BridgeSettings(filedata=MINIMAL_CONFIG)

    translator: HyteraMmdvmTranslator = HyteraMmdvmTranslator(
        settings=settings,
        hytera_outgoing=hytera_outgoing,
        hytera_incoming=hytera_incoming,
        mmdvm_outgoing=mmdvm_outgoing,
        mmdvm_incoming=mmdvm_incoming,
    )

    asyncio.create_task(translator.translate_from_mmdvm())
    asyncio.create_task(translator.translate_from_hytera())


if __name__ == "__main__":
    asyncio.run(test_mmdv_to_hytera())
