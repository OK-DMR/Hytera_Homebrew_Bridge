#!/usr/bin/env python3

from easysnmp import snmp_walk, SNMPVariable

from hytera_homebrew_bridge.lib.settings import BridgeSettings
from hytera_homebrew_bridge.lib.utils import octet_string_to_utf8


class SNMP:
    OID_PSU_VOLTAGE: str = "iso.3.6.1.4.1.40297.1.2.1.2.1.0"
    OID_PA_TEMPERATURE: str = "iso.3.6.1.4.1.40297.1.2.1.2.2.0"
    OID_VSWR: str = "iso.3.6.1.4.1.40297.1.2.1.2.4.0"
    # Forward power
    OID_TX_FWD_POWER: str = "iso.3.6.1.4.1.40297.1.2.1.2.5.0"
    # Reflected power
    OID_TX_REF_POWER: str = "iso.3.6.1.4.1.40297.1.2.1.2.6.0"
    OID_RSSI_TS1: str = "iso.3.6.1.4.1.40297.1.2.1.2.9.0"
    OID_RSSI_TS2: str = "iso.3.6.1.4.1.40297.1.2.1.2.10.0"

    OID_REPEATER_MODEL: str = "iso.3.6.1.4.1.40297.1.2.4.1.0"
    OID_MODEL_NUMBER: str = "iso.3.6.1.4.1.40297.1.2.4.2.0"
    # string
    OID_FIRMWARE_VERSION: str = "iso.3.6.1.4.1.40297.1.2.4.3.0"
    # Radio Data Version, string
    OID_RCDB_VERSION: str = "iso.3.6.1.4.1.40297.1.2.4.4.0"
    OID_SERIAL_NUMBER: str = "iso.3.6.1.4.1.40297.1.2.4.5.0"
    # callsign
    OID_RADIO_ALIAS: str = "iso.3.6.1.4.1.40297.1.2.4.6.0"
    # integer
    OID_RADIO_ID: str = "iso.3.6.1.4.1.40297.1.2.4.7.0"
    # digital=0, analog=1, mixed=2
    OID_CUR_CHANNEL_MODE: str = "iso.3.6.1.4.1.40297.1.2.4.8.0"
    OID_CUR_CHANNEL_NAME: str = "iso.3.6.1.4.1.40297.1.2.4.9.0"
    # Hz
    OID_TX_FREQUENCE: str = "iso.3.6.1.4.1.40297.1.2.4.10.0"
    # Hz
    OID_RX_FREQUENCE: str = "iso.3.6.1.4.1.40297.1.2.4.11.0"
    # receive=0, transmit=1
    OID_WORK_STATUS: str = "iso.3.6.1.4.1.40297.1.2.4.12.0"
    OID_CUR_ZONE_ALIAS: str = "iso.3.6.1.4.1.40297.1.2.4.13.0"

    @staticmethod
    def walk_ip(address: tuple, settings_storage: BridgeSettings) -> dict:
        ip, port = address
        try:
            walk_result: list = snmp_walk(
                "1.3.6.1.4.1.40297.1.2.4",
                hostname=ip,
                community=settings_storage.snmp_family,
                version=1,
            )
            for snmp_var in walk_result:
                if isinstance(snmp_var, SNMPVariable):
                    value = snmp_var.value
                    if snmp_var.oid in (
                        SNMP.OID_REPEATER_MODEL,
                        SNMP.OID_MODEL_NUMBER,
                        SNMP.OID_FIRMWARE_VERSION,
                        SNMP.OID_RCDB_VERSION,
                        SNMP.OID_RADIO_ALIAS,
                        SNMP.OID_CUR_ZONE_ALIAS,
                        SNMP.OID_SERIAL_NUMBER,
                        SNMP.OID_CUR_CHANNEL_NAME,
                    ):
                        value = octet_string_to_utf8(value)
                    settings_storage.hytera_snmp_data[snmp_var.oid] = value
        except SystemError:
            pass

        return settings_storage.hytera_snmp_data
