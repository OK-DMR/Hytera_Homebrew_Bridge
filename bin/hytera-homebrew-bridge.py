#!/usr/bin/env python3
import asyncio
import importlib.util
import logging
import os
import socket
import sys
from asyncio import AbstractEventLoop, Queue
from signal import SIGINT, SIGTERM
from typing import Optional


class HyteraHomebrewBridge:
    def __init__(self, settings_ini_path: str):
        self.loop: Optional[AbstractEventLoop] = None
        self.settings: BridgeSettings = BridgeSettings(filepath=settings_ini_path)
        # message queues for translator
        self.queue_mmdvm_outgoing: Queue = Queue()
        self.queue_hytera_incoming: Queue = Queue()
        self.queue_hytera_outgoing: Queue = Queue()
        self.queue_mmdvm_incoming: Queue = Queue()
        # homebrew / mmdvm
        self.homebrew_protocol: MMDVMProtocol = MMDVMProtocol(
            settings=self.settings,
            connection_lost_callback=self.homebrew_connection_lost,
            queue_outgoing=self.queue_mmdvm_outgoing,
            queue_incoming=self.queue_mmdvm_incoming,
        )
        # hytera ipsc: p2p dmr and rdac
        self.hytera_p2p_protocol: HyteraP2PProtocol = HyteraP2PProtocol(
            settings=self.settings, repeater_accepted_callback=self.homebrew_connect()
        )
        self.hytera_dmr_protocol: HyteraDMRProtocol = HyteraDMRProtocol(
            settings=self.settings,
            queue_incoming=self.queue_hytera_incoming,
            queue_outgoing=self.queue_hytera_outgoing,
        )
        self.hytera_rdac_protocol: HyteraRDACProtocol = HyteraRDACProtocol(
            settings=self.settings, rdac_completed_callback=self.homebrew_connect()
        )
        # prepare translator
        self.hytera_mmdvm_translator: HyteraMmdvmTranslator = HyteraMmdvmTranslator(
            settings=self.settings,
            mmdvm_incoming=self.queue_mmdvm_incoming,
            hytera_incoming=self.queue_hytera_incoming,
            mmdvm_outgoing=self.queue_mmdvm_outgoing,
            hytera_outgoing=self.queue_hytera_outgoing,
        )

    async def go(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.settings.print_settings()

        # start translator tasks
        self.loop.create_task(self.hytera_mmdvm_translator.translate_from_mmdvm())
        self.loop.create_task(self.hytera_mmdvm_translator.translate_from_hytera())

        # mmdvm maintenance (auto login, auth, ping/pong)
        self.loop.create_task(self.homebrew_protocol.periodic_maintenance())

        # send translated or protocol generated packets to respective upstreams
        self.loop.create_task(self.hytera_dmr_protocol.send_hytera_from_queue())
        self.loop.create_task(self.homebrew_protocol.send_mmdvm_from_queue())

        # connect Hytera repeater
        await self.hytera_p2p_connect()
        await self.hytera_dmr_connect()
        await self.hytera_rdac_connect()

        # MMDVM will get connected once the Hytera is set-up and running correctly
        # it is not meant to be started here

    async def hytera_p2p_connect(self) -> None:
        # P2P/IPSC Service address
        await self.loop.create_datagram_endpoint(
            lambda: self.hytera_p2p_protocol,
            reuse_address=True,
            local_addr=(self.settings.ipsc_ip, self.settings.p2p_port),
        )

    async def hytera_dmr_connect(self) -> None:
        await self.loop.create_datagram_endpoint(
            lambda: self.hytera_dmr_protocol,
            reuse_address=True,
            reuse_port=True,
            local_addr=(self.settings.ipsc_ip, self.settings.dmr_port),
        )

    async def hytera_rdac_connect(self) -> None:
        await self.loop.create_datagram_endpoint(
            lambda: self.hytera_rdac_protocol,
            reuse_address=True,
            reuse_port=True,
            local_addr=(self.settings.ipsc_ip, self.settings.rdac_port),
        )

    async def homebrew_connect(self) -> None:
        incorrect_config_params = self.settings.get_incorrect_configurations()
        if len(incorrect_config_params) > 0:
            self.homebrew_protocol.log(
                "Current configuration is not valid for connection", logging.ERROR
            )
            for triplet in incorrect_config_params:
                self.homebrew_protocol.log(
                    f"PARAM: {triplet[0]} CURRENT_VALUE: {triplet[1]} MESSAGE: {triplet[2]}"
                )
            return

        # target address
        hb_target_address = (self.settings.hb_master_host, self.settings.hb_master_port)
        # Create Homebrew protocol handler
        hb_transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self.homebrew_protocol,
            local_addr=(self.settings.hb_local_ip, self.settings.hb_local_port),
            remote_addr=hb_target_address,
            reuse_address=True,
            reuse_port=True,
        )
        hb_local_socket = hb_transport.get_extra_info("socket")
        if isinstance(hb_local_socket, socket.socket):
            # Extract bound socket port
            self.settings.hb_local_port = hb_local_socket.getsockname()[1]

    def homebrew_connection_lost(self) -> None:
        self.homebrew_connect()

    def stop_running(self) -> None:
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

    self_name: str = "hytera_homebrew_bridge"
    self_spec = importlib.util.find_spec(self_name)
    if self_spec is None:
        print("Package hytera-homebrew-bridge is not installed, trying locally\n")
        parent_folder: str = os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))
        )
        expected_folder: str = f"{parent_folder}{os.path.sep}"
        if os.path.isdir(expected_folder):
            sys.path.append(expected_folder)

    from hytera_homebrew_bridge.lib.hytera_protocols import (
        HyteraP2PProtocol,
        HyteraDMRProtocol,
        HyteraRDACProtocol,
    )
    from hytera_homebrew_bridge.lib.mmdvm_protocol import MMDVMProtocol
    from hytera_homebrew_bridge.lib.settings import BridgeSettings
    from hytera_homebrew_bridge.lib.hytera_mmdvm_translator import HyteraMmdvmTranslator

    uvloop_spec = importlib.util.find_spec("uvloop")
    if uvloop_spec:
        import uvloop

        uvloop.install()

    loop = asyncio.get_event_loop()
    # order is necessary, various asyncio object are create at bridge init
    # and those must be created after the main loop is created
    bridge: HyteraHomebrewBridge = HyteraHomebrewBridge(sys.argv[1])
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, bridge.stop_running)

    try:
        loop.run_until_complete(bridge.go())
        loop.run_forever()
    finally:
        print("Hytera Homebrew Bridge Ended")
