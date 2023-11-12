#!/usr/bin/env python3
import asyncio
from asyncio import AbstractEventLoop
from typing import Optional
from uuid import UUID

from okdmr.dmrlib.protocols.hytera.p2p_datagram_protocol import P2PDatagramProtocol
from okdmr.dmrlib.protocols.hytera.rdac_datagram_protocol import RDACDatagramProtocol
from okdmr.dmrlib.storage.repeater_storage import RepeaterStorage
from okdmr.dmrlib.utils.logging_trait import LoggingTrait

from okdmr.hhb.hhb_repeater_storage import HHBRepeaterStorage
from okdmr.hhb.hytera_repeater import HyteraRepeater
from okdmr.hhb.settings import BridgeSettings


class HyteraHomebrewBridge(LoggingTrait):
    def __init__(self, settings_ini_path: str):
        self.loop: Optional[AbstractEventLoop] = None
        self.settings: BridgeSettings = BridgeSettings(filepath=settings_ini_path)
        self.storage: RepeaterStorage = HHBRepeaterStorage()
        # hytera ipsc: p2p dmr and rdac
        self.hytera_p2p_protocol: P2PDatagramProtocol = P2PDatagramProtocol(
            storage=self.storage,
        )
        self.hytera_rdac_protocol: RDACDatagramProtocol = RDACDatagramProtocol(
            storage=self.storage, callback=lambda u: self.homebrew_connect(u)
        )
        # prepare translator

    async def go(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.settings.print_settings()

        # connect Hytera repeater
        await self.hytera_p2p_connect()
        if not self.settings.hytera_disable_rdac:
            await self.hytera_rdac_connect()

    async def homebrew_connect(self, repeater_id: UUID) -> None:
        rpt: HyteraRepeater = self.storage.match_uuid(repeater_id)
        await rpt.go()
        await rpt.homebrew_connect()

    async def hytera_p2p_connect(self) -> None:
        """
        Start P2P/IPSC Service handler
        :return:
        """
        await self.loop.create_datagram_endpoint(
            lambda: self.hytera_p2p_protocol,
            local_addr=(self.settings.ipsc_ip, self.settings.p2p_port),
        )

    async def hytera_rdac_connect(self) -> None:
        """
        Start RDAC service handler
        :return:
        """
        await self.loop.create_datagram_endpoint(
            lambda: self.hytera_rdac_protocol,
            local_addr=(self.settings.ipsc_ip, self.settings.rdac_port),
        )

    def stop_running(self) -> None:
        self.log_info("stop_running called")

        for rpt in self.storage.all():
            if isinstance(rpt, HyteraRepeater):
                rpt.homebrew_protocol.disconnect()

        self.hytera_p2p_protocol.disconnect()
        self.loop.stop()
        for task in asyncio.all_tasks():
            task.cancel()
            task.done()
