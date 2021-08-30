#!/usr/bin/env python3
from typing import Dict, Optional

from kaitaistruct import KaitaiStruct

from hytera_homebrew_bridge.dmrlib.mmdvm_utils import (
    get_mmdvm_timeslot,
    get_ipsc_timeslot,
)
from hytera_homebrew_bridge.dmrlib.terminal import Terminal, BurstInfo
from hytera_homebrew_bridge.kaitai.hytera_radio_network_protocol import (
    HyteraRadioNetworkProtocol,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_heartbeat import (
    IpSiteConnectHeartbeat,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.lib.logging_trait import LoggingTrait
from hytera_homebrew_bridge.lib.utils import byteswap_bytes
from hytera_homebrew_bridge.tests.prettyprint import _prettyprint


class TransmissionWatcher(LoggingTrait):
    def __init__(self):
        self.terminals: Dict[int, Terminal] = {}

    def ensure_terminal(self, dmrid: int):
        if dmrid not in self.terminals:
            self.terminals[dmrid] = Terminal(dmrid)

    def process_mmdvm(
        self, parsed: Mmdvm, do_debug: bool = True
    ) -> Optional[BurstInfo]:
        terminal_id: Optional[int] = None
        burst: Optional[BurstInfo] = None

        if not hasattr(parsed, "command_data"):
            self.log_debug("MMDVM unknown packet")
            self.log_debug(str(_prettyprint(parsed)))
        elif isinstance(parsed.command_data, Mmdvm.TypeUnknown):
            self.log_debug(
                "MMDVM unknown command data {parsed.command_data.__class__.__name__}"
            )
        elif isinstance(parsed.command_data, Mmdvm.TypeDmrData):
            terminal_id = parsed.command_data.source_id
            timeslot = get_mmdvm_timeslot(parsed.command_data)
            self.ensure_terminal(terminal_id)
            burst = self.terminals[terminal_id].process_dmr_data(
                parsed.command_data.dmr_data, timeslot=timeslot
            )
        elif isinstance(parsed.command_data, Mmdvm.TypeTalkerAlias):
            terminal_id = parsed.command_data.radio_id
            self.ensure_terminal(terminal_id)
            self.terminals[terminal_id].set_callsign_alias(
                parsed.command_data.talker_alias
            )

        if do_debug and terminal_id is not None:
            self.terminals[terminal_id].debug()

        return burst

    def process_hytera_ipsc(
        self, parsed: IpSiteConnectProtocol, do_debug: bool = True
    ) -> BurstInfo:
        terminal_id = parsed.source_radio_id
        timeslot = get_ipsc_timeslot(parsed)
        payload_swap = byteswap_bytes(parsed.ipsc_payload)
        self.ensure_terminal(terminal_id)
        burst = self.terminals[terminal_id].process_dmr_data(
            payload_swap, timeslot=timeslot
        )
        if do_debug:
            self.terminals[terminal_id].debug()
        return burst

    def process_packet(
        self, parsed: KaitaiStruct, do_debug=True
    ) -> Optional[BurstInfo]:
        if isinstance(parsed, Mmdvm):
            return self.process_mmdvm(parsed, do_debug=do_debug)
        elif isinstance(parsed, IpSiteConnectProtocol):
            return self.process_hytera_ipsc(parsed, do_debug=do_debug)
        elif isinstance(parsed, IpSiteConnectHeartbeat):
            # ignore these
            pass
        elif isinstance(parsed, HyteraRadioNetworkProtocol):
            self.log_debug("HRNP Packet received")
            self.log_debug(str(_prettyprint(parsed)))
        else:
            self.log_error(
                f"Did not process packet of class {parsed.__class__.__name__}"
            )
        return None

    def end_all_transmissions(self):
        for terminal in self.terminals.values():
            for timeslot in terminal.timeslots.values():
                timeslot.transmission.end_transmissions()
