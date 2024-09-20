from __future__ import annotations

import enum


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


class StopType(enum.Enum):
    PH = "ph"
    PT = "pt"
