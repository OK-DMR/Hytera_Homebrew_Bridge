from typing import Optional

from kaitaistruct import KaitaiStruct

from kaitai.hytera_dmr_application_protocol import HyteraDmrApplicationProtocol
from kaitai.hytera_radio_network_protocol import HyteraRadioNetworkProtocol
from kaitai.hytera_simple_transport_reliability_protocol import (
    HyteraSimpleTransportReliabilityProtocol,
)
from kaitai.ip_site_connect_heartbeat import IpSiteConnectHeartbeat
from kaitai.ip_site_connect_protocol import IpSiteConnectProtocol
from kaitai.real_time_transport_protocol import RealTimeTransportProtocol
from tests.prettyprint import _prettyprint
from .generic_service import GenericHyteraService
from .storage import Storage


class DMRHyteraService(GenericHyteraService):
    def run(self) -> None:
        self.create_socket()
        while True:
            try:
                data, address = self.serverSocket.recvfrom(4096)
                ip, port = address
                self.log("data (%d) received from %s.%s" % (len(data), ip, port))
                self.log(data.hex())

                if len(data) == 1 and data[0] == 0x00:
                    # RPTL
                    self.serverSocket.sendto(bytes([0x41]), address)
                    continue

                slot = data[16]
                packetType = data[8]
                slotType = data[18:19]
                frameType = data[22:23]
                self.log(
                    "recv slot:%s packetType:%s slotType:%s frameType:%s"
                    % (hex(slot), hex(packetType), slotType.hex(), frameType.hex())
                )
                packet = self.parse_hytera_data(data)
                if packet:
                    self.log(
                        "type: %s data:\n%s"
                        % (packet.__class__.__name__, _prettyprint(packet))
                    )
                else:
                    self.log("unknown packet")

            except Exception as err:
                self.selfLogger.error(err, exc_info=True)

    @staticmethod
    def parse_hytera_data(bytedata) -> Optional[KaitaiStruct]:
        if len(bytedata) < 2:
            # probably just heartbeat response
            return IpSiteConnectHeartbeat.from_bytes(bytedata)
        elif bytedata[0:2] == bytes([0x32, 0x42]):
            # HSTRP
            return HyteraSimpleTransportReliabilityProtocol.from_bytes(bytedata)
        elif bytedata[0:1] == bytes([0x7E]):
            # HRNP
            return HyteraRadioNetworkProtocol.from_bytes(bytedata)
        elif (int.from_bytes(bytedata[0:1], byteorder="big") & 0x80) == 0x80 and (
            int.from_bytes(bytedata[0:1], byteorder="big") & 0xC0
        ) == 2:
            return RealTimeTransportProtocol.from_bytes(bytedata)
        elif (
            int.from_bytes(bytedata[0:8], byteorder="little") == 0
            or bytedata[0:4] == b"ZZZZ"
            or bytedata[20:22] == bytes([0x11, 0x11])
        ):
            if bytedata[5:9] == bytes([0x00, 0x00, 0x00, 0x14]):
                return IpSiteConnectHeartbeat.from_bytes(bytedata)
            else:
                return IpSiteConnectProtocol.from_bytes(bytedata)
        else:
            # HDAP
            return HyteraDmrApplicationProtocol.from_bytes(bytedata)


if __name__ == "__main__":
    t = DMRHyteraService()
    t.set_storage(Storage()).start()
