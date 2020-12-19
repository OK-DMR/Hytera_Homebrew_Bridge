#!/usr/bin/env python3
import asyncio
import socket
import sys
from asyncio import AbstractEventLoop
from signal import SIGINT, SIGTERM
from typing import Optional

from hytera_homebrew_bridge.lib.hytera_protocols import (
    HyteraP2PProtocol,
    HyteraDMRProtocol,
    HyteraRDACProtocol,
)
from hytera_homebrew_bridge.lib.mmdvm_protocol import MMDVMProtocol
from hytera_homebrew_bridge.lib.settings import BridgeSettings


class HyteraHomebrewBridge:
    def __init__(self, settings_ini_path: str):
        self.loop: Optional[AbstractEventLoop] = None
        self.settings: BridgeSettings = BridgeSettings(filepath=settings_ini_path)
        # homebrew / mmdvm
        self.homebrew_protocol: MMDVMProtocol = MMDVMProtocol(
            settings=self.settings,
            connection_lost_callback=self.homebrew_connection_lost,
        )
        # hytera ipsc: p2p dmr and rdac
        self.hytera_p2p_protocol: HyteraP2PProtocol = HyteraP2PProtocol(
            settings=self.settings,
        )
        self.hytera_dmr_protocol: HyteraDMRProtocol = HyteraDMRProtocol(
            settings=self.settings
        )
        self.hytera_rdac_protocol: HyteraRDACProtocol = HyteraRDACProtocol(
            settings=self.settings, rdac_completed_callback=self.homebrew_connect()
        )

    async def go(self):
        self.loop = asyncio.get_running_loop()
        self.settings.print_settings()

        await self.hytera_p2p_connect()
        await self.hytera_dmr_connect()
        await self.hytera_rdac_connect()

    async def hytera_p2p_connect(self):
        # P2P/IPSC Service address
        await self.loop.create_datagram_endpoint(
            lambda: self.hytera_p2p_protocol,
            reuse_address=True,
            local_addr=(self.settings.ipsc_ip, self.settings.p2p_port),
        )

    async def hytera_dmr_connect(self):
        await self.loop.create_datagram_endpoint(
            lambda: self.hytera_dmr_protocol,
            reuse_address=True,
            local_addr=(self.settings.ipsc_ip, self.settings.dmr_port),
        )

    async def hytera_rdac_connect(self):
        await self.loop.create_datagram_endpoint(
            lambda: self.hytera_rdac_protocol,
            reuse_address=True,
            local_addr=(self.settings.ipsc_ip, self.settings.rdac_port),
        )

    async def homebrew_connect(self):
        # target address
        hb_target_address = (self.settings.hb_master_host, self.settings.hb_master_port)
        # Create Homebrew protocol handler
        hb_transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self.homebrew_protocol,
            local_addr=(self.settings.hb_local_ip, self.settings.hb_local_port),
            remote_addr=hb_target_address,
            reuse_address=True,
        )
        hb_local_socket = hb_transport.get_extra_info("socket")
        if isinstance(hb_local_socket, socket.socket):
            # Extract bound socket port
            self.settings.hb_local_port = hb_local_socket.getsockname()[1]
        self.loop.create_task(self.homebrew_protocol.periodic_maintenance())

    def homebrew_connection_lost(self):
        self.homebrew_connect()

    def stop_running(self):
        self.homebrew_protocol.disconnect()
        self.hytera_p2p_protocol.disconnect()
        self.loop.stop()
        for task in asyncio.Task.all_tasks():
            task.cancel()
            task.done()


if __name__ == "__main__":
    print("Hytera Homebrew Bridge")
    print("This project is experimental, use at your own risk\n")

    if len(sys.argv) < 2:
        print("use as hytera-homebrew-bridge <path to settings.ini>")
        print(
            "If you do not have the settings.ini file, you can obtain one here: "
            "https://github.com/OK-DMR/Hytera_Homebrew_Bridge/blob/master/settings.ini.default"
        )
        exit(1)

    bridge: HyteraHomebrewBridge = HyteraHomebrewBridge(sys.argv[1])

    loop = asyncio.get_event_loop()
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, bridge.stop_running)

    try:
        loop.run_until_complete(bridge.go())
        loop.run_forever()
    finally:
        print("Hytera Homebrew Bridge Ended")
