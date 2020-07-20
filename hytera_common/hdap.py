from kaitai.hytera_dmr_application_protocol import HyteraDmrApplicationProtocol


class HDAPPacket(object):
    """
    Big Endian, except for RCP / Radio Control Protocol
    1b message header => message type
    2b opcode
    2b number of bytes / payload size
    0+b payload
    1b checksum
    1b message footer => always 0x03
    """
    minimum_size: int = 7
    raw: bytes = None
    packet: HyteraDmrApplicationProtocol = None

    def __init__(self, data: bytes):
        self.raw = data
        if len(data) < self.minimum_size:
            return
        self.packet = HyteraDmrApplicationProtocol.from_bytes(data)