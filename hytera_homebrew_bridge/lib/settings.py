#!/usr/bin/env python3

import configparser

from hytera_homebrew_bridge.lib.logging_trait import LoggingTrait

_UNSET = object()


class BridgeSettings(LoggingTrait):
    SECTION_GENERAL = "general"
    SECTION_HOMEBREW = "homebrew"
    SECTION_IPSC = "ip-site-connect"
    SECTION_SNMP = "snmp"
    SECTION_LOGGING = "logging"

    HYTERA_MODE_IPSC = "ip-site-connect"
    HYTERA_MODE_FTPC = "forward-to-pc"
    HYTERA_ALL_MODES = (HYTERA_MODE_FTPC, HYTERA_MODE_IPSC)

    MMDVM_PROTOCOL_2015 = "homebrew"
    MMDVM_PROTOCOL_2020 = "mmdvm"
    MMDVM_PROTOCOL_DMRG = "dmrgateway"
    MMDVM_KNOWN_PROTOCOLS = (
        MMDVM_PROTOCOL_2015,
        MMDVM_PROTOCOL_2020,
        MMDVM_PROTOCOL_DMRG,
    )

    MINIMAL_SETTINGS = """
    [ip-site-connect]
    ip = 192.168.1.2
    p2p_port = 50000
    dmr_port = 50001
    rdac_port = 50002

    [homebrew]
    local_ip = 0.0.0.0
    master_ip = 192.168.1.3
    master_port = 62031
    password = B3S3CURE
    """

    def __init__(self, filepath: str = None, filedata: str = None) -> None:

        if not filepath and not filedata:
            raise SystemError(
                "Cannot init BridgeSettings without filepath and filedata, at least one must be provided"
            )

        if filepath and filedata:
            raise SystemError(
                "Both filename and filedata provided, this is unsupported, choose one"
            )

        parser = configparser.ConfigParser()
        parser.sections()
        if filepath:
            parser.read(filenames=filepath)
        else:
            parser.read_string(string=filedata)

        self.snmp_enabled = parser.getboolean(
            self.SECTION_SNMP, "enabled", fallback=True
        )
        self.snmp_family = parser.get(self.SECTION_SNMP, "family", fallback="public")

        self.hb_protocol = parser.get(
            self.SECTION_HOMEBREW, "protocol", fallback=self.MMDVM_PROTOCOL_2020
        )
        if self.hb_protocol not in self.MMDVM_KNOWN_PROTOCOLS:
            raise LookupError(
                "Invalid Homebrew protocol configured (%s) valid options are %s"
                % (self.hb_protocol, self.MMDVM_KNOWN_PROTOCOLS)
            )

        self.hb_master_host = parser.get(self.SECTION_HOMEBREW, "master_ip")
        self.hb_master_port = parser.getint(self.SECTION_HOMEBREW, "master_port")
        self.hb_local_ip = parser.get(self.SECTION_HOMEBREW, "local_ip")
        self.hb_local_port = parser.getint(
            self.SECTION_HOMEBREW, "local_port", fallback=0
        )
        self.hb_password = parser.get(self.SECTION_HOMEBREW, "password")

        self.hb_repeater_dmr_id: int = self.getint_safe(
            parser, self.SECTION_HOMEBREW, "repeater_dmr_id", fallback=None
        )
        self.hb_callsign: str = parser.get(
            self.SECTION_HOMEBREW, "callsign", fallback=""
        )
        self.hb_color_code = self.getint_safe(
            parser, self.SECTION_HOMEBREW, "color_code", fallback=1
        )
        self.hb_latitude = parser.get(self.SECTION_HOMEBREW, "latitude", fallback="")
        self.hb_longitude = parser.get(self.SECTION_HOMEBREW, "longitude", fallback="")
        self.hb_antenna_height = self.getint_safe(
            parser, self.SECTION_HOMEBREW, "antenna_height", fallback=0
        )
        self.hb_location = parser.get(self.SECTION_HOMEBREW, "location", fallback="")
        self.hb_description = parser.get(
            self.SECTION_HOMEBREW, "description", fallback=""
        )
        self.hb_timeslots = parser.get(self.SECTION_HOMEBREW, "timeslots", fallback="3")
        self.hb_url = parser.get(
            self.SECTION_HOMEBREW,
            "url",
            fallback="https://github.com/ok-dmr/Hytera_Homebrew_Bridge",
        )
        self.hb_software_id = parser.get(
            self.SECTION_HOMEBREW, "software_id", fallback="2021.2"
        )
        self.hb_package_id = parser.get(
            self.SECTION_HOMEBREW, "package_id", fallback="Hytera Homebrew Bridge"
        )
        self.hb_rx_freq: str = parser.get(
            self.SECTION_HOMEBREW, "rx_freq", fallback=None
        )
        self.hb_tx_freq: str = parser.get(
            self.SECTION_HOMEBREW, "tx_freq", fallback=None
        )
        self.hb_tx_power: int = self.getint_safe(
            parser, self.SECTION_HOMEBREW, "tx_power", fallback=0
        )
        self.hb_stream_id_random: bool = parser.getboolean(
            self.SECTION_HOMEBREW, "use_random_stream_id", fallback=True
        )

        self.hytera_mode: str = parser.get(
            self.SECTION_GENERAL, "hytera_mode", fallback=self.HYTERA_MODE_IPSC
        )
        if self.hytera_mode not in self.HYTERA_ALL_MODES:
            raise LookupError(
                "Invalid Hytera mode %s, valid options are %s"
                % (self.hytera_mode, self.HYTERA_ALL_MODES)
            )

        if self.hytera_mode == self.HYTERA_MODE_IPSC:
            self.ipsc_ip: str = parser.get(self.SECTION_IPSC, "ip")
            self.p2p_port: int = parser.getint(self.SECTION_IPSC, "p2p_port")
            self.dmr_port: int = parser.getint(self.SECTION_IPSC, "dmr_port")
            self.rdac_port: int = parser.getint(self.SECTION_IPSC, "rdac_port")
            self.hytera_disable_rdac: bool = parser.getboolean(
                self.SECTION_IPSC, "disable_rdac", fallback=False
            )

        # hytera_protocols variables
        self.hytera_is_registered: bool = False
        self.hytera_snmp_data: dict = dict()

        # hytera repeater data
        self.hytera_repeater_id: int = 0
        self.hytera_callsign: str = ""
        self.hytera_hardware: str = ""
        self.hytera_firmware: str = ""
        self.hytera_serial_number: str = ""
        self.hytera_repeater_mode: int = 0
        self.hytera_tx_freq: int = 0
        self.hytera_rx_freq: int = 0
        self.hytera_repeater_ip: str = ""

    @staticmethod
    def getint_safe(
        parser: configparser.ConfigParser, section: str, key: str, fallback=_UNSET
    ):
        """
        Handles empty values where int is expected
        Errors such as "ValueError: invalid literal for int() with base 10: ''" won't be propagated, if fallback is set

        @param parser:
        @param section:
        @param key:
        @param fallback:
        @return:
        """
        try:
            return parser.getint(section, key, fallback=fallback)
        except ValueError:
            if fallback is _UNSET:
                raise
            return fallback

    def get_repeater_rx_freq(self) -> str:
        from hytera_homebrew_bridge.lib import snmp

        return (
            self.hb_rx_freq
            or str(self.hytera_rx_freq)
            or str(self.hytera_snmp_data.get(snmp.SNMP.OID_RX_FREQUENCE))
        )

    def get_repeater_tx_freq(self) -> str:
        from hytera_homebrew_bridge.lib import snmp

        return (
            self.hb_tx_freq
            or str(self.hytera_tx_freq)
            or str(self.hytera_snmp_data.get(snmp.SNMP.OID_TX_FREQUENCE))
        )

    def get_repeater_callsign(self) -> str:
        from hytera_homebrew_bridge.lib import snmp

        return (
            self.hb_callsign
            or self.hytera_callsign
            or self.hytera_snmp_data.get(snmp.SNMP.OID_RADIO_ALIAS)
        )

    def get_repeater_dmrid(self) -> int:
        from hytera_homebrew_bridge.lib import snmp

        return int(
            self.hb_repeater_dmr_id
            or self.hytera_repeater_id
            or self.hytera_snmp_data.get(snmp.SNMP.OID_RADIO_ID)
            or 0
        )

    def get_incorrect_configurations(self) -> list:
        rtn: list = list()

        generic_error_message: str = (
            "Value might have not been configured and was not obtained in Hytera repeater "
            "configuration process (either P2P, RDAC or SNMP) "
        )

        repeater_id = self.get_repeater_dmrid()
        if repeater_id < 1:
            rtn.append(("homebrew.repeater_dmr_id", repeater_id, generic_error_message))

        repeater_callsign = self.get_repeater_callsign()
        if not repeater_callsign:
            rtn.append(("homebrew.callsign", repeater_callsign, generic_error_message))

        return rtn

    def print_settings(self) -> None:
        self.log_info("Settings Loaded")
        self.log_info(
            f"Hytera Repeater is expected to connect at {self.ipsc_ip} and ports"
            f" [MASTER PORT: {self.p2p_port}] [DMR PORT: {self.dmr_port}] [RDAC PORT: {self.rdac_port}]",
        )
        self.log_info(
            f"Upstream Homebrew/MMDVM server is expected at {self.hb_master_host}:{self.hb_master_port}\n"
        )

    def print_repeater_configuration(self):
        pass
