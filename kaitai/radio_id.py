# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version("0.9"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s"
        % (kaitaistruct.__version__)
    )


class RadioId(KaitaiStruct):
    """represented as 3 bytes, each byte interpreted as number (0-255)"""

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.radio_id_raw = self._io.read_u4le()

    @property
    def radio_id(self):
        if hasattr(self, "_m_radio_id"):
            return self._m_radio_id if hasattr(self, "_m_radio_id") else None

        self._m_radio_id = self.radio_id_raw >> 8
        return self._m_radio_id if hasattr(self, "_m_radio_id") else None
