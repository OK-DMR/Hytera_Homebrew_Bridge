#!/usr/bin/env python3
from asyncio import protocols

from okdmr.dmrlib.utils.logging_trait import LoggingTrait

from okdmr.hhb.settings import BridgeSettings
from okdmr.hhb.snmp import SNMP


class CustomBridgeDatagramProtocol(protocols.DatagramProtocol, LoggingTrait):
    """
    Code de-duplication
    """

    def __init__(self, settings: BridgeSettings) -> None:
        """

        :param settings:
        """
        super().__init__()
        self.settings = settings

    async def hytera_repeater_obtain_snmp(
        self, address: tuple, force: bool = False
    ) -> None:
        """

        :param address:
        :param force:
        :return:
        """
        self.settings.hytera_repeater_ip = address[0]
        if self.settings.snmp_enabled and (
            force or not self.settings.hytera_snmp_data.get(address[0])
        ):
            await SNMP().walk_ip(address, self.settings)
        else:
            self.log_warning(
                f"SNMP is disabled or not available "
                f"snmp_enabled:{self.settings.snmp_enabled} "
                f"force:{force} "
                f"hytera_snmp_data:{address[0] in self.settings.hytera_snmp_data}"
            )
