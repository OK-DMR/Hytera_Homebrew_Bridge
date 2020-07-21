from kaitai.hytera_radio_network_protocol import HyteraRadioNetworkProtocol


class HRNPPacket(object):
    """
    Big Endian
    1b Header Identifier = 0x7E
    1b Version
    1b Block -> indicate that data are split into multiple messages
    1b Opcode
    1b Source ID
    1b Destination ID
    2b Packet Number (PN) => start with 1, packet counter
    2b Length
    2b Checksum => 0=no check
    0+b Payload
    """

    minimum_size: int = 12
    raw: bytes = None
    packet: HyteraRadioNetworkProtocol = None

    def __init__(self, data: bytes):
        self.raw = data
        if len(data) < self.minimum_size:
            return
        self.packet = HyteraRadioNetworkProtocol.from_bytes(data)

    def get_opcode_name(self):
        return self.packet.Opcodes(self.packet.opcode).name.upper()
