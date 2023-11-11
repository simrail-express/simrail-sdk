from __future__ import annotations

import dataclasses
from typing import List, Optional

import simpleregistry

from simrail_sdk import stations, enums


class LineSectionRegistry(simpleregistry.Registry):
    # def get_between(self, line: int, a: stations.Station, b: stations.Station) -> Optional[LineSection]:
    #     if sections := self.filter(line=line, from_station=a, to_station=b):
    #         return list(sections)[0]
    #     if sections := self.filter(line=line, from_station=b, to_station=a):
    #         return list(sections)[0]
    #     raise ValueError(f"No line {line} between {a.name} and {b.name}")

    def get_after(
        self, line: int, a: stations.Station, direction: enums.Parity
    ) -> Optional[LineSection]:
        if (
            a.station_types == [enums.StationType.HALT]
            or a.station_types == [enums.StationType.FREIGHT_GROUP]
            or a.station_types == [enums.StationType.BLOCK_POST]
        ):
            return None

        if a.station_types == [enums.StationType.BRANCH_OFF_POINT]:
            if a.belongs_to is None:
                raise ValueError(
                    f"A belongs_to station must be defined for BRANCH_OFF_POINT: {a.name}"
                )
            a = a.belongs_to

        try:
            if direction is enums.Parity.ODD:
                return self.get(line=line, from_station=a)
            return self.get(line=line, to_station=a)

        except ValueError:
            return None


line_section_registry = LineSectionRegistry("line_sections")


@simpleregistry.register(line_section_registry)
@dataclasses.dataclass(frozen=True)
class LineSection:
    line: int
    from_station: stations.Station
    to_station: stations.Station
    intermediate_points: List[stations.Station] = dataclasses.field(
        default_factory=list
    )
    interlock_type: Optional[enums.InterlockType] = enums.InterlockType.SS
    tracks: int = 2
    etcs_level: Optional[enums.ETCSLevel] = None

    def __str__(self):
        return self.name()

    def name(self, direction: enums.Parity = enums.Parity.ODD) -> str:
        if direction is enums.Parity.ODD:
            a, b = self.from_station.name, self.to_station.name
        else:
            a, b = self.to_station.name, self.from_station.name
        return f"{a} - {b}"


LK1__WarszawaZachodniaR19__WarszawaZachodnia = LineSection(
    line=1,
    from_station=stations.WarszawaZachodniaR19,
    to_station=stations.WarszawaZachodnia,
    interlock_type=None,
    tracks=2,
)
LK1__WarszawaZachodnia__WarszawaWlochy = LineSection(
    line=1,
    from_station=stations.WarszawaZachodnia,
    to_station=stations.WarszawaWlochy,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__WarszawaWlochy__Jozefinow = LineSection(
    line=1,
    from_station=stations.WarszawaWlochy,
    to_station=stations.Jozefinow,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__Jozefinow__Pruszkow = LineSection(
    line=1,
    from_station=stations.Jozefinow,
    to_station=stations.Pruszkow,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__Pruszkow__GrodziskMazowiecki = LineSection(
    line=1,
    from_station=stations.Pruszkow,
    to_station=stations.GrodziskMazowiecki,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__GrodziskMazowiecki__Zyrardow = LineSection(
    line=1,
    from_station=stations.GrodziskMazowiecki,
    to_station=stations.Zyrardow,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__Zyrardow__SkierniewiceMPZS = LineSection(
    line=1,
    from_station=stations.Zyrardow,
    to_station=stations.SkierniewiceMPzs,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__SkierniewiceMPZS__Skierniewice = LineSection(
    line=1,
    from_station=stations.SkierniewiceMPzs,
    to_station=stations.Skierniewice,
    interlock_type=None,
    tracks=2,
)
LK1__Skierniewice__SkierniewicePPZS = LineSection(
    line=1,
    from_station=stations.Skierniewice,
    to_station=stations.SkierniewicePPzs,
    interlock_type=None,
    tracks=2,
)
LK1__SkierniewicePPZS__Plycwia = LineSection(
    line=1,
    from_station=stations.SkierniewicePPzs,
    to_station=stations.Plycwia,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__Myszkow__Zawiercie = LineSection(
    line=1,
    from_station=stations.Myszkow,
    to_station=stations.Zawiercie,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__Zawiercie__LazyLA = LineSection(
    line=1,
    from_station=stations.Zawiercie,
    to_station=stations.LazyLA,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK1__LazyLA__Lazy = LineSection(
    line=1,
    from_station=stations.LazyLA,
    to_station=stations.Lazy,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__Lazy__LazyLC = LineSection(
    line=1,
    from_station=stations.Lazy,
    to_station=stations.LazyLC,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK1__LazyLC__DabrowaGorniczaZabkowiceDZA = LineSection(
    line=1,
    from_station=stations.LazyLC,
    to_station=stations.DabrowaGorniczaZabkowiceDZA,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__DabrowaGorniczaZabkowiceDZA__DabrowaGorniczaZabkowice = LineSection(
    line=1,
    from_station=stations.DabrowaGorniczaZabkowiceDZA,
    to_station=stations.DabrowaGorniczaZabkowice,
    interlock_type=None,
    tracks=2,
)
LK1__DabrowaGorniczaZabkowice__DabrowaGornicza = LineSection(
    line=1,
    from_station=stations.DabrowaGorniczaZabkowice,
    to_station=stations.DabrowaGornicza,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__DabrowaGornicza__Bedzin = LineSection(
    line=1,
    from_station=stations.DabrowaGornicza,
    to_station=stations.Bedzin,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__Bedzin__SosnowiecGlowny = LineSection(
    line=1,
    from_station=stations.Bedzin,
    to_station=stations.SosnowiecGlowny,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__SosnowiecGlowny__SosnowiecGlownyPZSR52 = LineSection(
    line=1,
    from_station=stations.SosnowiecGlowny,
    to_station=stations.SosnowiecGlownyPZSR52,
    interlock_type=None,
    tracks=2,
)
LK1__SosnowiecGlownyPZSR52__KatowiceZawodzie = LineSection(
    line=1,
    from_station=stations.SosnowiecGlownyPZSR52,
    to_station=stations.KatowiceZawodzie,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK1__KatowiceZawodzie__Katowice = LineSection(
    line=1,
    from_station=stations.KatowiceZawodzie,
    to_station=stations.Katowice,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)

LK2__WarszawaZachodnia__WarszawaCentralna = LineSection(
    line=2,
    from_station=stations.WarszawaZachodnia,
    to_station=stations.WarszawaCentralna,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK2__WarszawaCentralna__WarszawaWschodnia = LineSection(
    line=2,
    from_station=stations.WarszawaCentralna,
    to_station=stations.WarszawaWschodnia,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK2__WarszawaWschodnia__WarszawaPodskarbinska = LineSection(
    line=2,
    from_station=stations.WarszawaWschodnia,
    to_station=stations.WarszawaPodskarbinska,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)

LK4__GrodziskMazowiecki__Korytow = LineSection(
    line=4,
    from_station=stations.GrodziskMazowiecki,
    to_station=stations.Korytow,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__Korytow__Szeligi = LineSection(
    line=4,
    from_station=stations.Korytow,
    to_station=stations.Szeligi,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__Szeligi__BialaRawska = LineSection(
    line=4,
    from_station=stations.Szeligi,
    to_station=stations.BialaRawska,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__BialaRawska__Strzalki = LineSection(
    line=4,
    from_station=stations.BialaRawska,
    to_station=stations.Strzalki,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__Strzalki__Idzikowice = LineSection(
    line=4,
    from_station=stations.Strzalki,
    to_station=stations.Idzikowice,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__Idzikowice__OpocznoPoludnie = LineSection(
    line=4,
    from_station=stations.Idzikowice,
    to_station=stations.OpocznoPoludnie,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK4__OpocznoPoludnie__Pilichowice = LineSection(
    line=4,
    from_station=stations.OpocznoPoludnie,
    to_station=stations.Pilichowice,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK4__Pilichowice__Olszamowice = LineSection(
    line=4,
    from_station=stations.Pilichowice,
    to_station=stations.Olszamowice,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK4__Olszamowice__WloszczowaPolnoc = LineSection(
    line=4,
    from_station=stations.Olszamowice,
    to_station=stations.WloszczowaPolnoc,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK4__WloszczowaPolnoc__Knapowka = LineSection(
    line=4,
    from_station=stations.WloszczowaPolnoc,
    to_station=stations.Knapowka,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__Knapowka__Psary = LineSection(
    line=4,
    from_station=stations.Knapowka,
    to_station=stations.Psary,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__Psary__GoraWlodowska = LineSection(
    line=4,
    from_station=stations.Psary,
    to_station=stations.GoraWlodowska,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__GoraWlodowska__Zawiercie = LineSection(
    line=4,
    from_station=stations.GoraWlodowska,
    to_station=stations.Zawiercie,
    interlock_type=enums.InterlockType.SS,
    etcs_level=enums.ETCSLevel.L1,
    tracks=2,
)
LK4__Zawiercie__ZawiercieGT = LineSection(
    line=4,
    from_station=stations.Zawiercie,
    to_station=stations.ZawiercieGt,
    interlock_type=None,
    tracks=2,
)

LK8__SedziszowTowarowy__Sedziszow = LineSection(
    line=8,
    from_station=stations.SedziszowTowarowy,
    to_station=stations.Sedziszow,
    interlock_type=None,
    tracks=2,
)
LK8__Sedziszow__Kozlow = LineSection(
    line=8,
    from_station=stations.Sedziszow,
    to_station=stations.Kozlow,
    interlock_type=enums.InterlockType.W24,
    tracks=2,
)
LK8__Kozlow__Tunel = LineSection(
    line=8,
    from_station=stations.Kozlow,
    to_station=stations.Tunel,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK8__Tunel__Miechow = LineSection(
    line=8,
    from_station=stations.Tunel,
    to_station=stations.Miechow,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK8__Miechow__Slomniki = LineSection(
    line=8,
    from_station=stations.Miechow,
    to_station=stations.Slomniki,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK8__Slomniki__Niedzwiedz = LineSection(
    line=8,
    from_station=stations.Slomniki,
    to_station=stations.Niedzwiedz,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK8__Niedzwiedz__Zastow = LineSection(
    line=8,
    from_station=stations.Niedzwiedz,
    to_station=stations.Zastow,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK8__Zastow__Raciborowice = LineSection(
    line=8,
    from_station=stations.Zastow,
    to_station=stations.Raciborowice,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK8__Raciborowice__KrakowBatowice = LineSection(
    line=8,
    from_station=stations.Raciborowice,
    to_station=stations.KrakowBatowice,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK8__KrakowBatowice__KrakowPrzedmiescie = LineSection(
    line=8,
    from_station=stations.KrakowBatowice,
    to_station=stations.KrakowPrzedmiescie,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK8__KrakowPrzedmiescie__KrakowGlowny = LineSection(
    line=8,
    from_station=stations.KrakowPrzedmiescie,
    to_station=stations.KrakowGlowny,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)

LK9__WarszawaWschodnia__WarszawaPraga = LineSection(
    line=9,
    from_station=stations.WarszawaWschodnia,
    to_station=stations.WarszawaPraga,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)

LK19__WarszawaGlTowSR18__Jozefinow = LineSection(
    line=19,
    from_station=stations.WarszawaGlTowSr18,
    to_station=stations.Jozefinow,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)

LK22__Radzice__RadzicePzsR31 = LineSection(
    line=22,
    from_station=stations.RadzicePzsR31,
    to_station=stations.Radzice,
    interlock_type=None,
    tracks=2,
)

LK45__WarszawaWschodnia__WarszawaGrochow = LineSection(
    line=45,
    from_station=stations.WarszawaWschodnia,
    to_station=stations.WarszawaGrochow,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)

LK61__Czarnca__Zelislawice = LineSection(
    line=61,
    from_station=stations.Czarnca,
    to_station=stations.Zelislawice,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)

# LK62__Tunel__TunelR13 = LineSection(
#     line=62,
#     from_station=stations.Tunel,
#     to_station=stations.TunelR13,
#     interlock_type=None,
#     tracks=2,
# )
LK62__Tunel__Charsznica = LineSection(
    line=62,
    from_station=stations.Tunel,
    to_station=stations.Charsznica,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK62__Charsznica__Wolbrom = LineSection(
    line=62,
    from_station=stations.Charsznica,
    to_station=stations.Wolbrom,
    interlock_type=enums.InterlockType.W24,
    tracks=2,
)
LK62__Wolbrom__JaroszowiecOlkuski = LineSection(
    line=62,
    from_station=stations.Wolbrom,
    to_station=stations.JaroszowiecOlkuski,
    interlock_type=enums.InterlockType.W24,
    tracks=2,
)
LK62__JaroszowiecOlkuski__Olkusz = LineSection(
    line=62,
    from_station=stations.JaroszowiecOlkuski,
    to_station=stations.Olkusz,
    interlock_type=enums.InterlockType.W24,
    tracks=2,
)
LK62__Olkusz__Bukowno = LineSection(
    line=62,
    from_station=stations.Olkusz,
    to_station=stations.Bukowno,
    interlock_type=enums.InterlockType.W24,
    tracks=2,
)
LK62__Bukowno__Slawkow = LineSection(
    line=62,
    from_station=stations.Bukowno,
    to_station=stations.Slawkow,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK62__Slawkow__DabrowaGorniczaWschodnia = LineSection(
    line=62,
    from_station=stations.Slawkow,
    to_station=stations.DabrowaGorniczaWschodnia,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK62__DabrowaGorniczaStrzemieszyce__DabrowaGorniczaWschodnia = LineSection(
    line=62,
    to_station=stations.DabrowaGorniczaStrzemieszyce,
    from_station=stations.DabrowaGorniczaWschodnia,
    interlock_type=enums.InterlockType.W24,
    tracks=2,
)
LK62__SosnowiecKazimierz__DabrowaGorniczaStrzemieszyce = LineSection(
    line=62,
    to_station=stations.SosnowiecKazimierz,
    from_station=stations.DabrowaGorniczaStrzemieszyce,
    interlock_type=None,
    tracks=1,
)
LK62__SosnowiecKazimierzPZSSK2__SosnowiecKazimierz = LineSection(
    line=62,
    to_station=stations.SosnowiecKazimierzPZSSKZ2,
    from_station=stations.SosnowiecKazimierz,
    interlock_type=None,
    tracks=1,
)
LK62__SosnowiecDandowka__SosnowiecKazimierzPZSSK2 = LineSection(
    line=62,
    to_station=stations.SosnowiecDandowka,
    from_station=stations.SosnowiecKazimierzPZSSKZ2,
    interlock_type=None,
    tracks=1,
)
LK62__SosnowiecPoludniowy__SosnowiecDandowka = LineSection(
    line=62,
    from_station=stations.SosnowiecDandowka,
    to_station=stations.SosnowiecPoludniowy,
    interlock_type=None,
    tracks=1,
)
LK62__SosnowiecGlowny__SosnowiecPoludniowy = LineSection(
    line=62,
    from_station=stations.SosnowiecPoludniowy,
    to_station=stations.SosnowiecGlowny,
    interlock_type=None,
    tracks=1,
)

LK64__Kozlow__Sprowa = LineSection(
    line=64,
    from_station=stations.Kozlow,
    to_station=stations.Sprowa,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK64__Sprowa__Starzyny = LineSection(
    line=64,
    from_station=stations.Sprowa,
    to_station=stations.Starzyny,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)

LK133__DabrowaGorniczaZabkowiceDZAR4_7__DabrowaGorniczaZabkowiceDZA = LineSection(
    line=133,
    from_station=stations.DabrowaGorniczaZabkowiceDzaR4_7,
    to_station=stations.DabrowaGorniczaZabkowiceDZA,
    interlock_type=None,
    tracks=2,
)
LK133__DabrowaGorniczaZabkowiceDZA__DabrowaGorniczaZabkowice = LineSection(
    line=133,
    from_station=stations.DabrowaGorniczaZabkowiceDZA,
    to_station=stations.DabrowaGorniczaZabkowice,
    interlock_type=None,
    tracks=2,
)
LK133__DabrowaGorniczaZabkowice__DabrowaGorniczaHutaKatowice = LineSection(
    line=133,
    from_station=stations.DabrowaGorniczaZabkowice,
    to_station=stations.DabrowaGorniczaHutaKatowice,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
# LK133__DabrowaGorniczaHutaKatowice__DabrowaGorniczaHutaKatowiceR7 = LineSection(
#     line=133,
#     from_station=stations.DabrowaGorniczaHutaKatowiceR7,
#     to_station=stations.DabrowaGorniczaHutaKatowice,
#     interlock_type=None,
#     tracks=2,
# )
LK133__DabrowaGorniczaHutaKatowice__DabrowaGorniczaPoludniowa = LineSection(
    line=133,
    from_station=stations.DabrowaGorniczaHutaKatowice,
    to_station=stations.DabrowaGorniczaPoludniowa,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK133__DabrowaGorniczaPoludniowa__Dorota = LineSection(
    line=133,
    from_station=stations.DabrowaGorniczaPoludniowa,
    to_station=stations.Dorota,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK133__Dorota__SosnowiecMaczki = LineSection(
    line=133,
    from_station=stations.Dorota,
    to_station=stations.SosnowiecMaczki,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)

LK137__Katowice__KatowiceTowarowaKTC = LineSection(
    line=137,
    from_station=stations.Katowice,
    to_station=stations.KatowiceTowarowaKTC,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK137__KatowiceTowarowaKTC__ChorzowBatory = LineSection(
    line=137,
    from_station=stations.KatowiceTowarowaKTC,
    to_station=stations.ChorzowBatory,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK137__ChorzowBatory__RudaChebzie = LineSection(
    line=137,
    from_station=stations.ChorzowBatory,
    to_station=stations.RudaChebzie,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK137__RudaChebzie__Zabrze = LineSection(
    line=137,
    from_station=stations.RudaChebzie,
    to_station=stations.Zabrze,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK137__Zabrze__Gliwice = LineSection(
    line=137,
    from_station=stations.Zabrze,
    to_station=stations.Gliwice,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)

# LK138
LK138__KatowiceZawodzie__Katowice = LineSection(
    line=138,
    from_station=stations.KatowiceZawodzie,
    to_station=stations.Katowice,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK138__Szabelnia__KatowiceZawodzie = LineSection(
    line=138,
    from_station=stations.Szabelnia,
    to_station=stations.KatowiceZawodzie,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)

# LK139
LK139__Katowice__Brynow = LineSection(
    line=139,
    from_station=stations.Katowice,
    to_station=stations.Brynow,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)


# LK142
LK142__Staszic__KatowiceKostuchna = LineSection(
    line=142,
    from_station=stations.Staszic,
    to_station=stations.KatowiceKostuchna,
    interlock_type=None,
    tracks=1,
)

# LK154
LK154__LazyLA__Lazy11 = LineSection(
    line=154,
    from_station=stations.LazyLA,
    to_station=stations.LazyL11,
    interlock_type=None,
    tracks=1,
)
LK154__Lazy11__Lazy = LineSection(
    line=154,
    from_station=stations.LazyL11,
    to_station=stations.Lazy,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK154__Lazy__LazyLC = LineSection(
    line=154,
    from_station=stations.Lazy,
    to_station=stations.LazyLC,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK154__LazyLC__Przemiarki = LineSection(
    line=154,
    from_station=stations.LazyLC,
    to_station=stations.Przemiarki,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK154__Przemiarki__DabrowaGorniczaDTAR5 = LineSection(
    line=154,
    from_station=stations.Przemiarki,
    to_station=stations.DabrowaGorniczaTowarowaDtaR5,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK154__DabrowaGorniczaDTAR5__DabrowaGorniczaDTA = LineSection(
    # @TODO: Can this be deleted and DTA R5 made skippable?
    line=154,
    from_station=stations.DabrowaGorniczaTowarowaDtaR5,
    to_station=stations.DabrowaGorniczaTowarowaDta,
    interlock_type=None,
    tracks=2,
)
LK154__DabrowaGorniczaDTA__DabrowaGorniczaTowarowa = LineSection(
    line=154,
    from_station=stations.DabrowaGorniczaTowarowaDta,
    to_station=stations.DabrowaGorniczaTowarowa,
    interlock_type=None,
    tracks=2,
)

# LK160
LK160__Zawiercie__LazyLA = LineSection(
    line=160,
    from_station=stations.Zawiercie,
    to_station=stations.LazyLA,
    interlock_type=None,
    tracks=1,
)
LK160__LazyLA__Lazy = LineSection(
    line=160,
    from_station=stations.LazyLA,
    to_station=stations.Lazy,
    interlock_type=None,
    tracks=1,
)
LK160__Lazy__LazyLC = LineSection(
    line=160,
    from_station=stations.Lazy,
    to_station=stations.LazyLC,
    interlock_type=None,
    tracks=1,
)
LK160__LazyLC__DabrowaGorniczaZabkowiceDZA = LineSection(
    line=160,
    from_station=stations.LazyLC,
    to_station=stations.DabrowaGorniczaZabkowiceDZA,
    interlock_type=enums.InterlockType.S,
    tracks=1,
)

# LK162
LK162__DabrowaGorniczaStrzemieszyce__DabrowaGorniczaStrzemieszyceR75 = LineSection(
    line=162,
    from_station=stations.DabrowaGorniczaStrzemieszyce,
    to_station=stations.DabrowaGorniczaStrzemieszyceR75,
    interlock_type=None,
    tracks=1,
)
LK162__DabrowaGorniczaStrzemieszyceR75__DabrowaGorniczaHutaKatowice = LineSection(
    line=162,
    from_station=stations.DabrowaGorniczaStrzemieszyceR75,
    to_station=stations.DabrowaGorniczaHutaKatowice,
    interlock_type=None,
    tracks=1,
)
LK162__DabrowaGorniczaHutaKatowice__DabrowaGorniczaHutaKatowiceR7 = LineSection(
    line=162,
    from_station=stations.DabrowaGorniczaHutaKatowice,
    to_station=stations.DabrowaGorniczaHutaKatowiceR7,
    interlock_type=None,
    tracks=1,
)

# LK163
LK163__SosnowiecKazimierz__SosnowiecMaczki = LineSection(
    line=163,
    from_station=stations.SosnowiecKazimierz,
    to_station=stations.SosnowiecMaczki,
    interlock_type=None,
    tracks=1,
)

# LK171
LK171__DabrowaGorniczaTowarowaDTA__Koziol = LineSection(
    line=171,
    from_station=stations.DabrowaGorniczaTowarowaDta,
    to_station=stations.Koziol,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK171__Koziol__DabrowaGorniczaWschodnia = LineSection(
    line=171,
    from_station=stations.Koziol,
    to_station=stations.DabrowaGorniczaWschodnia,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK171__DabrowaGorniczaWschodnia__Dorota = LineSection(
    line=171,
    from_station=stations.DabrowaGorniczaWschodnia,
    to_station=stations.Dorota,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK171__Dorota__Juliusz = LineSection(
    line=171,
    from_station=stations.Dorota,
    to_station=stations.Juliusz,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)
LK171__Juliusz__SosnowiecDandowka = LineSection(
    line=171,
    from_station=stations.Juliusz,
    to_station=stations.SosnowiecDandowka,
    interlock_type=enums.InterlockType.W24,
    tracks=2,
)
LK171__SosnowiecDandowka__Stawiska = LineSection(
    line=171,
    from_station=stations.SosnowiecDandowka,
    to_station=stations.Stawiska,
    interlock_type=enums.InterlockType.W24,
    tracks=2,
)
LK171__Stawiska__KatowiceMuchowiecKMB = LineSection(
    line=171,
    from_station=stations.Stawiska,
    to_station=stations.KatowiceMuchKmb,
    interlock_type=enums.InterlockType.PP,
    tracks=2,
)

# LK186
LK186__Zawiercie__LazyLA = LineSection(
    line=186,
    from_station=stations.Zawiercie,
    to_station=stations.LazyLA,
    interlock_type=None,
    tracks=1,
)
LK186__LazyLA__Lazy = LineSection(
    line=186,
    from_station=stations.LazyLA,
    to_station=stations.Lazy,
    interlock_type=enums.InterlockType.S,
    tracks=1,
)
LK186__Lazy__LazyLC = LineSection(
    line=186,
    from_station=stations.Lazy,
    to_station=stations.LazyLC,
    interlock_type=None,
    tracks=1,
)
LK186__LazyLC__DabrowaGorniczaZabkowiceDZA = LineSection(
    line=186,
    from_station=stations.LazyLC,
    to_station=stations.DabrowaGorniczaZabkowiceDZA,
    interlock_type=enums.InterlockType.S,
    tracks=1,
)

LK355__GrabownoWielkie__Twardogora = LineSection(
    line=355,
    from_station=stations.GrabownoWielkie,
    to_station=stations.Twardogora,
    tracks=1,
)
LK355__Twardogora__SosnieOstrowskie = LineSection(
    line=355,
    from_station=stations.Twardogora,
    to_station=stations.SosnieOstrowskie,
    tracks=1,
)
LK355__SosnieOstrowskie__Granowiec = LineSection(
    line=355,
    from_station=stations.SosnieOstrowskie,
    to_station=stations.Granowiec,
    tracks=1,
)
LK355__Granowiec__Odolanow = LineSection(
    line=355,
    from_station=stations.Granowiec,
    to_station=stations.Odolanow,
    tracks=1,
)
LK355__Odolanow__TopolaOsiedle = LineSection(
    line=355,
    from_station=stations.Odolanow,
    to_station=stations.TopolaOsiedle,
    tracks=1,
)
LK355__TopolaOsiedle__OstrowWielkopolski = LineSection(
    line=355,
    from_station=stations.TopolaOsiedle,
    to_station=stations.OstrowWielkopolski,
    tracks=1,
)

LK447__WarszawaZachodnia__WarszawaWlochy = LineSection(
    line=447,
    from_station=stations.WarszawaZachodnia,
    to_station=stations.WarszawaWlochy,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK447__WarszawaWlochy__Pruszkow = LineSection(
    line=447,
    from_station=stations.WarszawaWlochy,
    to_station=stations.Pruszkow,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK447__Pruszkow__GrodziskMazowiecki = LineSection(
    line=447,
    from_station=stations.Pruszkow,
    to_station=stations.GrodziskMazowiecki,
    interlock_type=enums.InterlockType.SS,
    tracks=2,
)
LK447__GrodziskMazowiecki__GrodziskMazowieckiR58 = LineSection(
    line=447,
    from_station=stations.GrodziskMazowiecki,
    to_station=stations.GrodziskMazowieckiR58,
    interlock_type=None,
    tracks=2,
)

LK570__Psary__Starzyny = LineSection(
    line=570,
    from_station=stations.Psary,
    to_station=stations.Starzyny,
    interlock_type=enums.InterlockType.S,
    tracks=1,
)
LK570__Starzyny__StarzynyR5 = LineSection(
    line=570,
    from_station=stations.Starzyny,
    to_station=stations.StarzynyR5,
    interlock_type=None,
    tracks=1,
)


LK571__Czarnca__Knapowka = LineSection(
    line=571,
    from_station=stations.Czarnca,
    to_station=stations.Knapowka,
    interlock_type=enums.InterlockType.S,
    tracks=1,
)

LK572__WloszczowaPolnoc__Zelislawice = LineSection(
    line=572,
    from_station=stations.WloszczowaPolnoc,
    to_station=stations.Zelislawice,
    interlock_type=enums.InterlockType.S,
    tracks=1,
)

LK573__Idzikowice__Radzice = LineSection(
    line=573,
    from_station=stations.Idzikowice,
    to_station=stations.Radzice,
    interlock_type=enums.InterlockType.S,
    tracks=1,
)

LK574__RadzicePzsR31__Idzikowice = LineSection(
    line=574,
    from_station=stations.RadzicePzsR31,
    to_station=stations.Idzikowice,
    interlock_type=enums.InterlockType.S,
    tracks=1,
)

LK652__KatowiceMRoz233__KatowiceMKmbR234 = LineSection(
    line=652,
    from_station=stations.KatowiceMRoz233,
    to_station=stations.KatowiceMKmbR234,
    interlock_type=None,
    tracks=1,
)
LK652__KatowiceMKmbR234__KatowiceMuchKmb = LineSection(
    line=652,
    from_station=stations.KatowiceMKmbR234,
    to_station=stations.KatowiceMuchKmb,
    interlock_type=None,
    tracks=1,
)
LK652__KatowiceMuchowiecKMB__Staszic = LineSection(
    line=652,
    from_station=stations.KatowiceMuchKmb,
    to_station=stations.Staszic,
    interlock_type=None,
    tracks=1,
)

LK657__Stawiska__KatowiceJanow = LineSection(
    line=657,
    from_station=stations.Stawiska,
    to_station=stations.KatowiceJanowPodg,
    interlock_type=enums.InterlockType.PP,
    tracks=1,
)
LK657__KatowiceJanow__KatowiceMuchowiecKMB = LineSection(
    line=657,
    from_station=stations.KatowiceJanowPodg,
    to_station=stations.KatowiceMuchKmb,
    interlock_type=enums.InterlockType.PP,
    tracks=1,
)

LK660__SosnowiecGlownyPZSR52__SosnowiecPoludniowy = LineSection(
    line=660,
    from_station=stations.SosnowiecPoludniowy,
    to_station=stations.SosnowiecGlownyPZSR52,
    interlock_type=None,
    tracks=1,
)

LK661__DabrowaGorniczaTowarowaR5__Koziol = LineSection(
    line=661,
    from_station=stations.DabrowaGorniczaTowarowaDtaR5,
    to_station=stations.Koziol,
    interlock_type=None,
    tracks=1,
)

LK766__Lukanow__OlesnicaRataje = LineSection(
    line=766,
    from_station=stations.Lukanow,
    to_station=stations.OlesnicaRataje,
    interlock_type=None,
    tracks=1,
)
LK766__OlesnicaRataje__DabrowaOlesnicka = LineSection(
    line=766,
    from_station=stations.OlesnicaRataje,
    to_station=stations.DabrowaOlesnicka,
    interlock_type=None,
    tracks=1,
)

LK815__Durzyn__Krotoszyn = LineSection(
    line=815,
    from_station=stations.Durzyn,
    to_station=stations.Krotoszyn,
    interlock_type=None,
    tracks=1,
)

LK839_WarszawaGrochowR5___WarszawaGrochow = LineSection(
    line=839,
    from_station=stations.WarszawaGrochowR5,
    to_station=stations.WarszawaGrochow,
    interlock_type=None,
    tracks=1,
)

# LK898
LK898__KatowiceMuchowiecStaszic__Staszic = LineSection(
    line=898,
    from_station=stations.Staszic,
    to_station=stations.KWKStaszic,
    interlock_type=None,
    tracks=1,
)
