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


class DmrCsbk(KaitaiStruct):
    """TS 102 361-2 V2.3.1 CSBK decoding"""

    class CsbkoTypes(Enum):
        unit_to_unit_voice_service_request = 4
        unit_to_unit_voice_service_answer_response = 5
        channel_timing = 7
        negative_acknowledge_response = 38
        bs_outbound_activation_csbk_pdu = 56
        preamble = 61

    class CsbkDataOrCsbk(Enum):
        csbk_content_follows_preambles = 0
        data_content_follows_preambles = 1

    class CsbkGroupOrIndividual(Enum):
        target_address_is_an_individual = 0
        target_address_is_a_group = 1

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.last_block = self._io.read_bits_int_be(1) != 0
        self.protect_flag = self._io.read_bits_int_be(1) != 0
        self.csbk_opcode = KaitaiStream.resolve_enum(
            DmrCsbk.CsbkoTypes, self._io.read_bits_int_be(6)
        )
        self.feature_set_id = self._io.read_bits_int_be(8)
        if self.csbk_opcode == DmrCsbk.CsbkoTypes.preamble:
            self.preamble_data_or_csbk = KaitaiStream.resolve_enum(
                DmrCsbk.CsbkDataOrCsbk, self._io.read_bits_int_be(1)
            )

        if self.csbk_opcode == DmrCsbk.CsbkoTypes.preamble:
            self.preamble_group_or_individual = KaitaiStream.resolve_enum(
                DmrCsbk.CsbkGroupOrIndividual, self._io.read_bits_int_be(1)
            )

        self.preamble_reserved_1 = self._io.read_bits_int_be(6)
        self.preamble_csbk_blocks_to_follow = self._io.read_bits_int_be(8)
        self.preamble_target_address = self._io.read_bits_int_be(24)
        self.preamble_source_address = self._io.read_bits_int_be(24)
