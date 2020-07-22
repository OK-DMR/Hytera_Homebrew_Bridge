# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from kaitai import datetimestring
from kaitai import radio_ip
from kaitai import intervalstring
from kaitai import gpsdata
class LocationProtocol(KaitaiStruct):

    class LpGeneralTypes(Enum):
        standard_location_immediate_service = 160
        emergency_location_reporting_service = 176
        triggered_location_reporting_service = 192
        condition_triggered_reporting_service = 208

    class Subtypes(Enum):
        report_request = 1
        report_answer = 2
        report = 3
        report_stop_request = 4
        report_stop_answer = 5
        quick_gps_request = 17
        quick_gps_answer = 18
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.opcode = KaitaiStream.resolve_enum(self._root.LpGeneralTypes, self._io.read_u1())
        self.subtype = KaitaiStream.resolve_enum(self._root.Subtypes, self._io.read_u1())
        if  ((self.opcode != self._root.LpGeneralTypes.emergency_location_immediate_service) and (self.subtype != self._root.Subtypes.report)) :
            self.request_id = self._io.read_bytes(4)

        self.radio_ip = radio_ip.RadioIp(self._io)
        if  ((self.opcode == self._root.LpGeneralTypes.emergency_location_immediate_service) and (self.subtype == self._root.Subtypes.report)) :
            self.emergency_data = self._root.AppendEmergencyReport(self._io, self, self._root)


    class AppendEmergencyReport(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.emergency_type = self._io.read_bytes(1)
            self.gpsdata = gpsdata.Gpsdata(self._io)


    class AppendTriggeredReportRequest(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.starttime = datetimestring.Datetimestring(self._io)
            self.stoptime = datetimestring.Datetimestring(self._io)
            self.interval = intervalstring.Intervalstring(self._io)


    class AppendResult(KaitaiStruct):
        """applies to emergency.stop_answer, triggered.report_answer, triggered.report_stop_answer
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.result = self._io.read_bytes(2)


    class RequestId(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.request_id = self._io.read_bytes(4)


    class AppendStandardAnswer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.result = self._io.read_bytes(2)
            self.gpsdata = gpsdata.Gpsdata(self._io)



