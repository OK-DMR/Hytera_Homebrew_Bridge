# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version("0.9"):
    raise Exception(
        "Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s"
        % (kaitaistruct.__version__)
    )


class IpSiteConnectHeartbeat(KaitaiStruct):
    """Hytera IP Multi-Site Connect Protocol heartbeat packet, either simple KEEPALIVE/UP or PING/PONG"""

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        _on = self._io.size()
        if _on == 1:
            self.data = IpSiteConnectHeartbeat.Keepalive(self._io, self, self._root)
        elif _on == 20:
            self.data = IpSiteConnectHeartbeat.PingPong(self._io, self, self._root)
        else:
            self.data = IpSiteConnectHeartbeat.Unknown(self._io, self, self._root)

    class Keepalive(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.nullbyte = self._io.read_bytes(1)
            if not self.nullbyte == b"\x00":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x00", self.nullbyte, self._io, u"/types/keepalive/seq/0"
                )

    class PingPong(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = self._io.read_bytes(4)
            if not self.header == b"\x5A\x5A\x5A\x5A":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x5A\x5A\x5A\x5A",
                    self.header,
                    self._io,
                    u"/types/ping_pong/seq/0",
                )
            self.heartbeat_identitier = self._io.read_bytes(5)
            if not self.heartbeat_identitier == b"\x0A\x00\x00\x00\x14":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x0A\x00\x00\x00\x14",
                    self.heartbeat_identitier,
                    self._io,
                    u"/types/ping_pong/seq/1",
                )
            self.nullbytes = self._io.read_bytes(3)
            if not self.nullbytes == b"\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x00\x00\x00", self.nullbytes, self._io, u"/types/ping_pong/seq/2"
                )
            self.heartbeat_seq = self._io.read_u1()
            self.tail = self._io.read_bytes(7)
            if not self.tail == b"\x5A\x59\x5A\x00\x00\x00\x00":
                raise kaitaistruct.ValidationNotEqualError(
                    b"\x5A\x59\x5A\x00\x00\x00\x00",
                    self.tail,
                    self._io,
                    u"/types/ping_pong/seq/4",
                )

    class Unknown(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes_full()
