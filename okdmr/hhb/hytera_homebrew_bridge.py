#!/usr/bin/env python3
import asyncio
import socket
from asyncio import AbstractEventLoop, Queue
from typing import Optional, Dict

from okdmr.hhb.callback_interface import CallbackInterface
from okdmr.hhb.hytera_mmdvm_translator import HyteraMmdvmTranslator
from okdmr.hhb.hytera_protocols import (
    HyteraP2PProtocol,
    HyteraDMRProtocol,
    HyteraRDACProtocol,
)
from okdmr.hhb.mmdvm_protocol import MMDVMProtocol
from okdmr.hhb.settings import BridgeSettings


class HyteraRepeater(CallbackInterface):
    def __init__(self, ip: str, settings: BridgeSettings, asyncloop: AbstractEventLoop):
        # ip of hytera repeater
        self.ip: str = ip
        self.dmr_port: int = 0
        self.settings: BridgeSettings = settings
        self.loop: AbstractEventLoop = asyncloop
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
            hytera_repeater_ip=ip,
        )
        self.hytera_dmr_protocol: HyteraDMRProtocol = HyteraDMRProtocol(
            settings=self.settings,
            queue_incoming=self.queue_hytera_incoming,
            queue_outgoing=self.queue_hytera_outgoing,
            hytera_repeater_ip=ip,
        )
        self.hytera_mmdvm_translator: HyteraMmdvmTranslator = HyteraMmdvmTranslator(
            settings=self.settings,
            mmdvm_incoming=self.queue_mmdvm_incoming,
            hytera_incoming=self.queue_hytera_incoming,
            mmdvm_outgoing=self.queue_mmdvm_outgoing,
            hytera_outgoing=self.queue_hytera_outgoing,
            hytera_repeater_ip=self.ip,
        )

    def homebrew_connection_lost(self, ip: str, port: int) -> None:
        asyncio.run(self.homebrew_connect(ip=ip, port=port))

    async def hytera_dmr_connect(self) -> None:
        (transport, _) = await self.loop.create_datagram_endpoint(
            lambda: self.hytera_dmr_protocol,
            sock=self.settings.hytera_repeater_data[self.ip].dmr_socket,
        )

    async def homebrew_connect(self, ip: str, port: int) -> None:
        incorrect_config_params = self.settings.get_incorrect_configurations(ip)
        if len(incorrect_config_params) > 0:
            self.homebrew_protocol.log_error(
                "Current configuration is not valid for connection"
            )
            self.settings.print_settings()
            for param, current_value, error_message in incorrect_config_params:
                self.homebrew_protocol.log_error(
                    f"PARAM: {param} CURRENT_VALUE: {current_value} MESSAGE: {error_message}"
                )
            return

        # target address
        hb_target_address = (self.settings.hb_master_host, self.settings.hb_master_port)
        # Create Homebrew protocol handler
        hb_transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self.homebrew_protocol,
            local_addr=(self.settings.hb_local_ip, self.settings.hb_local_port),
            remote_addr=hb_target_address,
            reuse_port=True,
        )
        hb_local_socket = hb_transport.get_extra_info("socket")
        if isinstance(hb_local_socket, socket.socket):
            # Extract bound socket port
            self.settings.hb_local_port = hb_local_socket.getsockname()[1]

    async def go(self):
        # start DMR protocol
        await self.hytera_dmr_connect()

        # start translator tasks
        self.loop.create_task(self.hytera_mmdvm_translator.translate_from_mmdvm())
        self.loop.create_task(self.hytera_mmdvm_translator.translate_from_hytera())

        # mmdvm maintenance (auto login, auth, ping/pong)
        self.loop.create_task(self.homebrew_protocol.periodic_maintenance())

        # send translated or protocol generated packets to respective upstreams
        self.loop.create_task(self.hytera_dmr_protocol.send_hytera_from_queue())
        self.loop.create_task(self.homebrew_protocol.send_mmdvm_from_queue())


class HyteraHomebrewBridge(CallbackInterface):
    def __init__(self, settings_ini_path: str):
        self.loop: Optional[AbstractEventLoop] = None
        self.settings: BridgeSettings = BridgeSettings(filepath=settings_ini_path)
        self.repeaters: Dict[str, HyteraRepeater] = {}
        # hytera ipsc: p2p dmr and rdac
        self.hytera_p2p_protocol: HyteraP2PProtocol = HyteraP2PProtocol(
            settings=self.settings, repeater_accepted_callback=self
        )
        self.hytera_rdac_protocol: HyteraRDACProtocol = HyteraRDACProtocol(
            settings=self.settings, rdac_completed_callback=self
        )
        # prepare translator

    async def go(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.settings.print_settings()

        # connect Hytera repeater
        await self.hytera_p2p_connect()
        if not self.settings.hytera_disable_rdac:
            await self.hytera_rdac_connect()

    async def homebrew_connect(self, ip: str, port: int) -> None:
        if not self.repeaters.get(ip):
            self.repeaters[ip] = HyteraRepeater(
                ip=ip, settings=self.settings, asyncloop=self.loop
            )
            await self.repeaters[ip].go()

        await self.repeaters[ip].homebrew_connect(ip=ip, port=port)

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
        for ip, repeater in self.repeaters.items():
            repeater.homebrew_protocol.disconnect()

        self.hytera_p2p_protocol.disconnect()
        self.loop.stop()
        for task in asyncio.all_tasks():
            task.cancel()
            task.done()
