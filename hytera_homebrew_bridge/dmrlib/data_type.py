from enum import Enum


class DataType(Enum):
    PrivacyIndicatorHeader = 0
    VoiceLCHeader = 1
    TerminatorWithLC = 2
    CSBK = 3
    MBCHeader = 4
    MBCContinuation = 5
    DataHeader = 6
    Rate12DataContinuation = 7
    Rate34DataContinuation = 8
    Idle = 9
    Rate1DataContinuation = 10
    UnifiedSingleBlockData = 11
    VoiceBurstA = 12
    VoiceBurstB = 13
    VoiceBurstC = 14
    VoiceBurstD = 15
    VoiceBurstE = 16
    VoiceBurstF = 17
    IPSCSync = 18
    UnknownDataType = 19
