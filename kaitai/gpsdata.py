# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version("0.9"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s"
        % (kaitaistruct.__version__)
    )


class Gpsdata(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.gps_status = self._io.read_bytes(1)
        self.gps_time = self._io.read_bytes(6)
        self.gps_date = self._io.read_bytes(6)
        self.north_south = self._io.read_bytes(1)
        self.latitude = self._io.read_bytes(9)
        self.east_west = self._io.read_bytes(1)
        self.longitude = self._io.read_bytes(10)
        self.speed = self._io.read_bytes(2)
        self.direction = self._io.read_bytes(3)
