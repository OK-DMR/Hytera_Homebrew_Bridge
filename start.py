#!/usr/bin/env python3
import asyncio
import socket
from asyncio import AbstractEventLoop, BaseTransport
from signal import SIGINT, SIGTERM
from typing import Optional

from lib.mmdvm_protocol import MMDVMProtocol
from lib.settings import BridgeSettings


class HyteraHomebrewBridge:
    def __init__(self):
        self.settings: BridgeSettings = BridgeSettings(filepath="settings.ini")
        self.homebrew_protocol: MMDVMProtocol = MMDVMProtocol(
            settings=self.settings,
            connection_lost_callback=self.homebrew_connection_lost,
        )
        self.loop: Optional[AbstractEventLoop] = None
        self.hb_transport: Optional[BaseTransport] = None
        self.hb_protocol: Optional[MMDVMProtocol] = None

    async def go(self):
        self.loop = asyncio.get_running_loop()
        self.print_welcome()

        await self.homebrew_connect()

    async def homebrew_connect(self):
        # target address
        hb_target_address = (self.settings.hb_master_host, self.settings.hb_master_port)
        # Create Homebrew protocol handler
        self.hb_transport, self.hb_protocol = await self.loop.create_datagram_endpoint(
            lambda: self.homebrew_protocol,
            local_addr=(self.settings.hb_local_ip, self.settings.hb_local_port),
            remote_addr=hb_target_address,
            reuse_address=True,
        )
        hb_local_socket = self.hb_transport.get_extra_info("socket")
        if isinstance(hb_local_socket, socket.socket):
            # Extract bound socket port
            self.settings.hb_local_port = hb_local_socket.getsockname()[1]
        self.loop.create_task(self.homebrew_protocol.periodic_maintenance())

    def print_welcome(self):
        print("Hytera Homebrew Bridge")
        print("This project is experimental, use at your own risk\n")
        self.settings.print_settings()

    def homebrew_connection_lost(self):
        self.homebrew_connect()

    def stop_running(self):
        self.loop.stop()


if __name__ == "__main__":
    bridge: HyteraHomebrewBridge = HyteraHomebrewBridge()

    loop = asyncio.get_event_loop()
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, bridge.stop_running)

    try:
        loop.run_until_complete(bridge.go())
        loop.run_forever()
    finally:
        loop.close()
