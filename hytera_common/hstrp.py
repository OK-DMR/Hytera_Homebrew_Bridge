from kaitai.hytera_simple_transport_reliability_protocol import (
    HyteraSimpleTransportReliabilityProtocol,
)


class HSTRPPacket(object):
    """
    Big-endian
    2b header = ASCII content 2B
    1b version = expect 0x00
    1b type (bitflags) indicating type of packet
    2b sequence number = packet counter
    ?b options (might not be present at all, or multiple)
    ?b payload (multiple messages, such as RRS, LP, TMP, RCP, TP or DTP, not RTP)
    """

    raw: bytes = None
    packet: HyteraSimpleTransportReliabilityProtocol = None
    minimum_size: int = 6

    def __init__(self, data: bytes):
        self.raw = data
        if len(data) < self.minimum_size:
            return
        self.packet = HyteraSimpleTransportReliabilityProtocol.from_bytes(data)
