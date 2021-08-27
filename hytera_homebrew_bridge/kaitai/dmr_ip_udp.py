# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version("0.9"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s"
        % (kaitaistruct.__version__)
    )


class DmrIpUdp(KaitaiStruct):
    """ETSI TS 102 361-3 V1.3.1, section 7, PDUs"""

    class SourceIpAddressIds(Enum):
        radio_network = 0
        usb_ethernet_interface_network = 1

    class DestinationIpAddressIds(Enum):
        radio_network = 0
        usb_ethernet_interface_network = 1
        group_network = 2

    class UdpPortIds(Enum):
        present_in_extended_header = 0
        utf16be_text_message_port_5016 = 1
        location_interface_protocol = 2

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass

    class UdpIpv4CompressedHeader(KaitaiStruct):
        """7.2.3 UDP/IPv4 Compressed Header, Table 7.14"""

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ipv4_identification = self._io.read_bytes(2)
            self.source_ip_address_id = KaitaiStream.resolve_enum(
                DmrIpUdp.SourceIpAddressIds, self._io.read_bits_int_be(4)
            )
            self.destination_ip_address_id = KaitaiStream.resolve_enum(
                DmrIpUdp.DestinationIpAddressIds, self._io.read_bits_int_be(4)
            )
            self.header_compression_opcode_msb = self._io.read_bits_int_be(1) != 0
            self.udp_source_port_id = KaitaiStream.resolve_enum(
                DmrIpUdp.UdpPortIds, self._io.read_bits_int_be(7)
            )
            self.header_compression_opcode_lsb = self._io.read_bits_int_be(1) != 0
            self.udp_destination_port_id = KaitaiStream.resolve_enum(
                DmrIpUdp.UdpPortIds, self._io.read_bits_int_be(7)
            )
            self._io.align_to_byte()
            if (
                self.udp_source_port_id
                == DmrIpUdp.UdpPortIds.present_in_extended_header
            ):
                self.udp_source_port = self._io.read_bytes(2)

            if (
                self.udp_destination_port_id
                == DmrIpUdp.UdpPortIds.present_in_extended_header
            ):
                self.udp_destination_port = self._io.read_bytes(2)

            self.user_data = self._io.read_bytes_full()
