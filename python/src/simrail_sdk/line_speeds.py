from __future__ import annotations

import json
import pathlib
from typing import List, Tuple, Optional

import pydantic
import simpleregistry

from simrail_sdk import enums, base

SPEED_JSON = pathlib.Path(__file__).parent / "line_speeds.json"


class SpeedRegistry(simpleregistry.Registry):
    def from_json(self):
        json_txt = SPEED_JSON.read_text()
        speed_data = json.loads(json_txt)
        for section in speed_data:
            speed_section_response = SpeedSectionResponse(**section)
            speed_section = SpeedSection.from_speed_section_response(speed_section_response)
            self.register(speed_section)

    def symmetric(
        self, vp: List[UnboundSpeedSection], vl: List[UnboundSpeedSection], direction: int
    ) -> List[Tuple[Optional[UnboundSpeedSection], Optional[UnboundSpeedSection]]]:
        vp_by_start = {s.from_mileage: s for s in vp}
        vl_by_start = {s.from_mileage: s for s in vl}
        all_starts = sorted(set(list(vp_by_start) + list(vl_by_start)), key=lambda s: s * direction)

        symmetric: List[Tuple[Optional[UnboundSpeedSection], Optional[UnboundSpeedSection]]] = [
            (vp_by_start.get(s), vl_by_start.get(s)) for s in all_starts
        ]

        return symmetric

    def deduplicate(self, sorted_speeds: List[UnboundSpeedSection]) -> List[UnboundSpeedSection]:
        deduped_speeds: List[UnboundSpeedSection] = []
        for speed in sorted_speeds:
            if speed.from_mileage == speed.to_mileage:
                continue
            if not deduped_speeds:
                deduped_speeds = [speed]
                continue
            if deduped_speeds[-1].vmax == speed.vmax:
                deduped_speed = UnboundSpeedSection(
                    from_mileage=deduped_speeds[-1].from_mileage,
                    to_mileage=speed.to_mileage,
                    vmax=deduped_speeds[-1].vmax,
                    # line=deduped_speeds[-1].line,
                    # track_parity=deduped_speeds[-1].track_parity,
                )
                deduped_speeds[-1] = deduped_speed
                continue
            deduped_speeds.append(speed)
        return deduped_speeds

    def cap_to(self, sorted_speeds: List[UnboundSpeedSection], cap_to: int) -> List[UnboundSpeedSection]:
        for speed in sorted_speeds:
            speed.vmax = min(speed.vmax, cap_to)
        return sorted_speeds

    def get_between(
        self,
        line: int,
        a: float,
        b: float,
        tracks: int,
        cap_to: Optional[int] = None,
    ) -> List[Tuple[Optional[UnboundSpeedSection], Optional[UnboundSpeedSection]]]:
        if tracks == 2:
            vp_track = enums.Parity.ODD if a < b else enums.Parity.EVEN
            vl_track = enums.Parity.EVEN if a < b else enums.Parity.ODD
        else:
            vp_track = enums.Parity.ODD
            vl_track = None

        smaller = min([a, b])
        greater = max([a, b])

        applicable = {enums.Parity.ODD: [], enums.Parity.EVEN: [], None: []}

        def sort_key(s: SpeedSection) -> float:
            if a < b:
                return s.from_mileage
            return -s.from_mileage

        for speed_section in sorted(self.filter(line=line), key=sort_key):
            if smaller <= speed_section.from_mileage < greater:
                applicable[speed_section.track_parity].append(speed_section.cap(a, b))
                continue
            if smaller <= speed_section.to_mileage < greater:
                applicable[speed_section.track_parity].append(speed_section.cap(a, b))
                continue
            if speed_section.from_mileage <= smaller and greater < speed_section.to_mileage:
                applicable[speed_section.track_parity].append(speed_section.cap(a, b))

        deduplicated = self.deduplicate(applicable[vp_track]), self.deduplicate(applicable[vl_track])
        if cap_to:
            deduplicated = self.cap_to(deduplicated[0], cap_to), self.cap_to(deduplicated[1], cap_to)
        return self.symmetric(deduplicated[0], deduplicated[1], 1 if a < b else -1)


speed_registry = SpeedRegistry("speeds")


class SpeedSectionResponse(pydantic.BaseModel):
    lineNo: int
    axisStart: int
    axisEnd: int
    vMax: int
    track: str


class UnboundSpeedSection(pydantic.BaseModel):
    from_mileage: float
    to_mileage: float
    vmax: int

    def cap(self, a: float, b: float) -> UnboundSpeedSection:
        if a < b:
            from_mileage = max([a, self.from_mileage])
            to_mileage = min([b, self.to_mileage])

        else:
            from_mileage = min([a, self.to_mileage])
            to_mileage = max([b, self.from_mileage])

        return UnboundSpeedSection(from_mileage=from_mileage, to_mileage=to_mileage, vmax=self.vmax)


@simpleregistry.register(speed_registry)
class SpeedSection(base.BasePydanticModel, UnboundSpeedSection):
    line: int
    track_parity: enums.Parity

    class Config:
        pk_fields = ["line", "from_mileage", "to_mileage"]

    @property
    def surrogate_pk(self) -> str:
        return ":".join(str(v) for v in [self.line, self.from_mileage, self.to_mileage])

    @classmethod
    def from_speed_section_response(cls, response: SpeedSectionResponse) -> SpeedSection:
        return cls(
            from_mileage=response.axisStart / 1000,
            to_mileage=response.axisEnd / 1000,
            line=response.lineNo,
            track_parity=enums.Parity(response.track),
            vmax=response.vMax,
        )


speed_registry.from_json()

L9__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=60,
    line=9,
    track_parity=enums.Parity.ODD,
)
L9__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=60,
    line=9,
    track_parity=enums.Parity.EVEN,
)
L14__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=120,
    line=14,
    track_parity=enums.Parity.ODD,
)
L14__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=120,
    line=14,
    track_parity=enums.Parity.EVEN,
)
L17__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=150,
    line=17,
    track_parity=enums.Parity.ODD,
)
L17__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=150,
    line=17,
    track_parity=enums.Parity.EVEN,
)
L22__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=22,
    track_parity=enums.Parity.ODD,
)
L22__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=22,
    track_parity=enums.Parity.EVEN,
)
L25__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=25,
    track_parity=enums.Parity.ODD,
)
L25__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=25,
    track_parity=enums.Parity.EVEN,
)
L45__1__0_000__2_297 = SpeedSection(
    from_mileage=0,
    to_mileage=2.297,
    vmax=60,
    line=45,
    track_parity=enums.Parity.ODD,
)
L45__2__0_000__2_297 = SpeedSection(
    # @TODO: for removal, there is no track 2
    from_mileage=0,
    to_mileage=2.297,
    vmax=60,
    line=45,
    track_parity=enums.Parity.EVEN,
)
L61__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=110,
    line=61,
    track_parity=enums.Parity.ODD,
)
L61__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=110,
    line=61,
    track_parity=enums.Parity.EVEN,
)
# The speed is missing for the following section in the json
# This might be due to the fact, that the line changes from single track to two tracks not exactly at
# the station axis (69.221) but almost 2 km later. As this is not supported by the renderer, and it's the only such
# case, I've just added this extra placeholder so it renders nicely.
L62__2__DabrowaGorniczaStrzemieszyce = SpeedSection(
    to_mileage=69.221,
    from_mileage=67.031,
    vmax=70,
    line=62,
    track_parity=enums.Parity.EVEN,
)
L139__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=90,
    line=137,
    track_parity=enums.Parity.ODD,
)
L139__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=90,
    line=137,
    track_parity=enums.Parity.EVEN,
)
L140__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=140,
    track_parity=enums.Parity.ODD,
)
L140__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=140,
    track_parity=enums.Parity.EVEN,
)
L141__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=60,
    line=141,
    track_parity=enums.Parity.ODD,
)
L141__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=60,
    line=141,
    track_parity=enums.Parity.EVEN,
)
L142__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=80,
    line=142,
    track_parity=enums.Parity.ODD,
)
L143__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=110,
    line=143,
    track_parity=enums.Parity.ODD,
)
L143__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=110,
    line=143,
    track_parity=enums.Parity.EVEN,
)
L149__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=70,
    line=149,
    track_parity=enums.Parity.ODD,
)
L149__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=70,
    line=149,
    track_parity=enums.Parity.EVEN,
)
L151__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=110,
    line=151,
    track_parity=enums.Parity.ODD,
)
L151__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=110,
    line=151,
    track_parity=enums.Parity.EVEN,
)
L158__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=60,
    line=158,
    track_parity=enums.Parity.ODD,
)
L158__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=60,
    line=158,
    track_parity=enums.Parity.EVEN,
)
L162__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=422,
    vmax=40,
    line=162,
    track_parity=enums.Parity.ODD,
)
L163__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=40,
    line=163,
    track_parity=enums.Parity.ODD,
)
L164__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=40,
    line=164,
    track_parity=enums.Parity.ODD,
)
L164__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=40,
    line=164,
    track_parity=enums.Parity.EVEN,
)
L171__1__Placeholder = SpeedSection(
    from_mileage=3.907,
    to_mileage=4.069,
    vmax=80,
    line=171,
    track_parity=enums.Parity.ODD,
)
L271__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=80,
    line=271,
    track_parity=enums.Parity.ODD,
)
L271__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=80,
    line=271,
    track_parity=enums.Parity.EVEN,
)
L281__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=120,
    line=281,
    track_parity=enums.Parity.ODD,
)
L281__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=120,
    line=281,
    track_parity=enums.Parity.EVEN,
)
L355__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=355,
    track_parity=enums.Parity.ODD,
)
L479__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=479,
    track_parity=enums.Parity.ODD,
)
L479__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=479,
    track_parity=enums.Parity.EVEN,
)
L540__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=540,
    track_parity=enums.Parity.ODD,
)
L540__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=540,
    track_parity=enums.Parity.EVEN,
)
L570__1__Missing = SpeedSection(
    from_mileage=0,
    to_mileage=0.252,
    vmax=100,
    line=570,
    track_parity=enums.Parity.ODD,
)
L592__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=592,
    track_parity=enums.Parity.ODD,
)
L592__2__Placeholder = SpeedSection(
    # @TODO: for removal, there is no track 2
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=592,
    track_parity=enums.Parity.EVEN,
)
L651__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=30,
    line=651,
    track_parity=enums.Parity.ODD,
)
L651__2__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=30,
    line=651,
    track_parity=enums.Parity.EVEN,
)
L766__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=100,
    line=766,
    track_parity=enums.Parity.ODD,
)
L815__1__Placeholder = SpeedSection(
    from_mileage=0,
    to_mileage=1000,
    vmax=40,
    line=815,
    track_parity=enums.Parity.ODD,
)
