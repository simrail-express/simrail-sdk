from __future__ import annotations

import enum
from typing import Optional


class BrakeMode(enum.Enum):
    T = "T"
    P = "P"
    R = "R"
    RMG = "R+Mg"


class ETCSLevel(enum.Enum):
    L1 = "L1"
    L2 = "L2"


class InterlockType(enum.Enum):
    PP = "PP"
    S = "S"
    SS = "SS"
    SP = "SP"
    W24 = "W24"


class RadioChannel(enum.Enum):
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"
    R5 = "R5"
    R6 = "R6"
    R7 = "R7"


class StationType(enum.Enum):
    BRANCH_OFF_POINT = "pprj"
    BLOCK_POST = "odst"
    FREIGHT_GROUP = "gt"
    HALT = "po"
    JUNCTION = "podg"
    LINES_MERGING = "pzs"
    PASSING_LOOP = "m"
    STATION = "st"
    TECHNICAL_STATION = "stth"


class StopTypeResponse(enum.Enum):
    CommercialStop = "CommercialStop"
    NoncommercialStop = "NoncommercialStop"
    NoStopOver = "NoStopOver"


class StopType(enum.Enum):
    PH = "ph"
    PT = "pt"

    @classmethod
    def from_stop_type_response(cls, timetable_point) -> Optional[StopType]:
        if timetable_point.stopType is StopTypeResponse.CommercialStop:
            return cls.PH
        # @TODO: This is hacky, report upstream
        if timetable_point.arrivalTime != timetable_point.departureTime:
            return cls.PT
        return None


class Parity(enum.Enum):
    ODD = "N"
    EVEN = "P"


class RunningOnTrack(enum.Enum):
    P = "P"
    L = "L"
