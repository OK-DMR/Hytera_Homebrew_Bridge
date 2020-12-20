#!/usr/bin/env python3
from asyncio import Queue

from hytera_homebrew_bridge.lib.settings import BridgeSettings


class HyteraMmdvmTranslator:
    def __init__(
        self,
        settings: BridgeSettings,
        hytera_incoming: Queue,
        hytera_outgoing: Queue,
        mmdvm_incoming: Queue,
        mmdvm_outgoing: Queue,
    ):
        self.settings = settings
        self.queue_hytera_to_translate = hytera_incoming
        self.queue_hytera_output = hytera_outgoing
        self.queue_mmdvm_to_translate = mmdvm_incoming
        self.queue_mmdvm_output = mmdvm_outgoing
