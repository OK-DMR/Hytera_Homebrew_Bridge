import asyncio
import socket
from asyncio import Queue
from logging import Logger

from okdmr.dmrlib.protocols.hytera.p2p_datagram_protocol import P2PDatagramProtocol
from okdmr.dmrlib.storage import ADDRESS_TYPE, ADDRESS_EMPTY
from okdmr.dmrlib.storage.repeater import Repeater
from okdmr.dmrlib.storage.repeater_storage import RepeaterStorage

from okdmr.hhb.hytera_mmdvm_translator import HyteraMmdvmTranslator
from okdmr.hhb.mmdvm_protocol import MMDVMProtocol
from okdmr.hhb.settings import BridgeSettings


class HyteraRepeater(Repeater):
    def __init__(
        self,
        settings: BridgeSettings,
        storage: RepeaterStorage,
        dmr_id: int = 0,
        callsign: str = "",
        serial: str = "",
        address_in: ADDRESS_TYPE = ADDRESS_EMPTY,
        address_out: ADDRESS_TYPE = ADDRESS_EMPTY,
        address_nat: ADDRESS_TYPE = ADDRESS_EMPTY,
        snmp_enabled: bool = True,
        nat_enabled: bool = False,
        logger: Logger = None,
    ):
        super().__init__(
            dmr_id=dmr_id,
            callsign=callsign,
            serial=serial,
            address_in=address_in,
            address_out=address_out,
            nat_enabled=nat_enabled,
            address_nat=address_nat,
            snmp_enabled=snmp_enabled,
            logger=logger,
        )

        self.storage: RepeaterStorage = storage
        self.settings: BridgeSettings = settings
        self.dmr_port: int = 0
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
            repeater_id=self.id,
            storage=self.storage,
        )
        self.hytera_dmr_protocol: P2PDatagramProtocol = P2PDatagramProtocol(
            storage=self.storage,
            p2p_port=self.settings.p2p_port,
            rdac_port=self.settings.rdac_port,
        )
        self.hytera_mmdvm_translator: HyteraMmdvmTranslator = HyteraMmdvmTranslator(
            settings=self.settings,
            storage=self.storage,
            mmdvm_incoming=self.queue_mmdvm_incoming,
            hytera_incoming=self.queue_hytera_incoming,
            mmdvm_outgoing=self.queue_mmdvm_outgoing,
            hytera_outgoing=self.queue_hytera_outgoing,
            repeater_id=self.id,
        )

    def homebrew_connection_lost(self) -> None:
        asyncio.run(self.homebrew_connect())

    async def hytera_dmr_connect(self) -> None:
        (transport, _) = await asyncio.get_event_loop().create_datagram_endpoint(
            lambda: self.hytera_dmr_protocol,
        )

    async def homebrew_connect(self) -> None:

        # target address
        hb_target_address = (self.settings.hb_master_host, self.settings.hb_master_port)
        # Create Homebrew protocol handler
        hb_transport, _ = await asyncio.get_event_loop().create_datagram_endpoint(
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

        loop = asyncio.get_running_loop()

        # start translator tasks
        loop.create_task(self.hytera_mmdvm_translator.translate_from_mmdvm())
        loop.create_task(self.hytera_mmdvm_translator.translate_from_hytera())

        # mmdvm maintenance (auto login, auth, ping/pong)
        loop.create_task(self.homebrew_protocol.periodic_maintenance())

        # send translated or protocol generated packets to respective upstreams
        # loop.create_task(self.hytera_dmr_protocol.send_hytera_from_queue())
        loop.create_task(self.homebrew_protocol.send_mmdvm_from_queue())
