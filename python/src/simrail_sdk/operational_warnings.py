import decimal
from typing import Optional, Set

import flask_babel
import simpleregistry

from simrail_sdk import base, stations, line_sections, enums

_ = flask_babel.lazy_gettext


warnings_registry = simpleregistry.Registry("warnings")


@simpleregistry.register(warnings_registry)
class Warning(base.BasePydanticModel):
    station: Optional[stations.Station]
    line_section: Optional[line_sections.LineSection]
    line: int
    tracks: Set[int]
    v_odd: Optional[int]
    v_even: Optional[int]
    from_mileage: decimal.Decimal
    to_mileage: decimal.Decimal
    reason: flask_babel.LazyString
    is_temporary: bool = True

    class Config:
        arbitrary_types_allowed = True
        pk_fields = ["surrogate_pk"]

    def get_location(self, direction: enums.Parity = enums.Parity.ODD) -> str:
        if self.station:
            return self.station.name
        return self.line_section.name(direction)

    def get_speed(self, direction: enums.Parity = enums.Parity.ODD) -> Optional[int]:
        return self.v_odd if direction is enums.Parity.ODD else self.v_even

    @property
    def surrogate_pk(self) -> str:
        station_or_line_section = self.station.name if self.station else str(self.line_section)
        tracks_comma_separated = ",".join(str(t) for t in self.tracks)
        return ":".join(
            str(v)
            for v in [
                station_or_line_section,
                tracks_comma_separated,
                self.from_mileage,
                self.to_mileage,
            ]
        )


LK1__DabrowaGorniczaZabkowice = Warning(
    station=stations.DabrowaGorniczaZabkowice,
    tracks={2},
    v_odd=50,
    v_even=50,
    line=1,
    from_mileage=decimal.Decimal("292.662"),
    to_mileage=decimal.Decimal("292.896"),
    reason=_("Unsettled ballast"),
)

LK4__GoraWlodowska__Zawiercie = Warning(
    line_section=line_sections.LK4__GoraWlodowska__Zawiercie,
    tracks={1, 2},
    v_odd=120,
    v_even=120,
    line=4,
    from_mileage=decimal.Decimal("207.703"),
    to_mileage=decimal.Decimal("207.723"),
    reason=_("Poor condition of the viaduct"),
)

LK62__Wolbrom__Jaroszowiec = Warning(
    line_section=line_sections.LK62__Wolbrom__JaroszowiecOlkuski,
    tracks={1, 2},
    v_odd=20,
    v_even=20,
    line=62,
    from_mileage=decimal.Decimal("26.185"),
    to_mileage=decimal.Decimal("26.194"),
    reason=_("No staff at level crossing"),
)
LK62__Sosnowiec_Dandowka = Warning(
    station=stations.SosnowiecDandowka,
    tracks={1},
    v_odd=30,
    v_even=30,
    line=62,
    from_mileage=decimal.Decimal("78.780"),
    to_mileage=decimal.Decimal("78.830"),
    reason=_("Poor condition of the viaduct"),
)

LK171__DabrowaGorniczaWschodnia__1 = Warning(
    station=stations.DabrowaGorniczaWschodnia,
    tracks={1},
    line=171,
    v_odd=40,
    v_even=40,
    from_mileage=decimal.Decimal("11.977"),
    to_mileage=decimal.Decimal("12.063"),
    reason=_("Poor condition of the switch"),
)
LK171__DabrowaGorniczaWschodnia__2 = Warning(
    station=stations.DabrowaGorniczaWschodnia,
    tracks={2},
    line=171,
    v_odd=40,
    v_even=40,
    from_mileage=decimal.Decimal("12.048"),
    to_mileage=decimal.Decimal("13.117"),
    reason=_("Poor condition of the track"),
)
LK171__SosnowiecDandowka = Warning(
    station=stations.SosnowiecDandowka,
    tracks={1, 2},
    line=171,
    v_odd=30,
    v_even=30,
    from_mileage=decimal.Decimal("24.400"),
    to_mileage=decimal.Decimal("24.450"),
    reason=_("Poor condition of the viaduct"),
)
LK171__KatowiceMuchowiec = Warning(
    station=stations.KatowiceMuchKmb,
    tracks={1},
    line=171,
    v_odd=20,
    v_even=20,
    from_mileage=decimal.Decimal("37.590"),
    to_mileage=decimal.Decimal("37.690"),
    reason=_("Poor condition of the switch"),
)

LK657__KatowiceMuchowiec = Warning(
    station=stations.KatowiceMuchKmb,
    tracks={1},
    line=657,
    v_odd=20,
    v_even=20,
    from_mileage=decimal.Decimal("9.300"),
    to_mileage=decimal.Decimal("9.400"),
    reason=_("Poor condition of the switch"),
)
