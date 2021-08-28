#!/usr/bin/env python3
from typing import Dict, Optional

from kaitaistruct import KaitaiStruct

from hytera_homebrew_bridge.dmrlib.mmdvm_utils import get_mmdvm_timeslot
from hytera_homebrew_bridge.dmrlib.terminal import Terminal
from hytera_homebrew_bridge.kaitai.hytera_radio_network_protocol import (
    HyteraRadioNetworkProtocol,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_heartbeat import (
    IpSiteConnectHeartbeat,
)
from hytera_homebrew_bridge.kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from hytera_homebrew_bridge.kaitai.mmdvm import Mmdvm
from hytera_homebrew_bridge.lib.utils import byteswap_bytes
from hytera_homebrew_bridge.tests.prettyprint import _prettyprint


class TransmissionWatcher:
    def __init__(self):
        self.terminals: Dict[int, Terminal] = {}

    def ensure_terminal(self, dmrid: int):
        if dmrid not in self.terminals:
            self.terminals[dmrid] = Terminal(dmrid)

    def process_mmdvm(self, parsed: Mmdvm):
        terminal_id: Optional[int] = None

        if not hasattr(parsed, "command_data"):
            print(f"MMDVM unknown packet")
            print(_prettyprint(parsed))
        elif isinstance(parsed.command_data, Mmdvm.TypeUnknown):
            print(f"MMDVM unknown command {parsed.command_data.__class__.__name__}")
        elif isinstance(parsed.command_data, Mmdvm.TypeDmrData):
            terminal_id = parsed.command_data.source_id
            timeslot = get_mmdvm_timeslot(parsed.command_data)
            self.ensure_terminal(terminal_id)
            self.terminals[terminal_id].process_dmr_data(
                parsed.command_data.dmr_data, timeslot=timeslot
            )
        elif isinstance(parsed.command_data, Mmdvm.TypeTalkerAlias):
            terminal_id = parsed.command_data.radio_id
            self.ensure_terminal(terminal_id)
            self.terminals[terminal_id].set_callsign_alias(
                parsed.command_data.talker_alias
            )

        if terminal_id is not None:
            self.terminals[terminal_id].debug()

    def process_hytera_ipsc(self, parsed: IpSiteConnectProtocol):
        terminal_id = parsed.source_radio_id
        timeslot = (
            1
            if parsed.timeslot_raw == IpSiteConnectProtocol.Timeslots.timeslot_1
            else 2
        )
        payload_swap = byteswap_bytes(parsed.ipsc_payload)
        self.ensure_terminal(terminal_id)
        self.terminals[terminal_id].process_dmr_data(payload_swap, timeslot=timeslot)

    def process_packet(self, parsed: KaitaiStruct):
        if isinstance(parsed, Mmdvm):
            self.process_mmdvm(parsed)
        elif isinstance(parsed, IpSiteConnectProtocol):
            self.process_hytera_ipsc(parsed)
        elif isinstance(parsed, IpSiteConnectHeartbeat):
            # ignore these
            pass
        elif isinstance(parsed, HyteraRadioNetworkProtocol):
            print("HRNP", _prettyprint(parsed))
        else:
            print(
                f"TransmissionWatcher::process_packet unknown {parsed.__class__.__name__}"
            )

    def end_all_transmissions(self):
        for terminal in self.terminals.values():
            for timeslot in terminal.timeslots.values():
                timeslot.transmission.end_transmissions()
