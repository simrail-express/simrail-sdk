from __future__ import annotations

import decimal
import logging
from typing import List, Dict, Optional, Set

import simpleregistry

from simrail_sdk import enums, base

logger = logging.getLogger(__name__)


DEFAULT_SHORT_NAME_REPLACEMENTS = {
    "Warszawa": "Wwa",
}


station_registry = simpleregistry.Registry("stations", {simpleregistry.Index(["name"])})


@simpleregistry.register(station_registry)
class Station(base.BasePydanticModel):
    name: str
    lat: decimal.Decimal
    lon: decimal.Decimal
    mileage: Dict[int, decimal.Decimal]
    radio_channels: List[enums.RadioChannel]
    station_types: List[enums.StationType] = [enums.StationType.STATION]
    is_boundary: bool = False
    remote_control_facilities: bool = False
    remotely_controlled_from: Optional[str] = None
    remote_control_with_optional_local_control: bool = False
    shp: bool = True
    radio_recording: bool = True
    r307: bool = False
    belongs_to: Optional["Station"] = None
    skippable: bool = False
    short_name: Optional[str] = None

    class Config:
        pk_fields = ["name"]

    @property
    def printable_name(self) -> str:
        if self.short_name:
            return self.short_name
        words = self.name.split()
        words_with_replacements = [
            DEFAULT_SHORT_NAME_REPLACEMENTS.get(w, w) for w in words
        ]
        return " ".join(words_with_replacements)

    @property
    def branch_off_points(self) -> Set[Station]:
        return station_registry.filter(belongs_to=self)

    @property
    def is_junction(self) -> bool:
        lines = set(self.mileage.keys())
        for branch_off in self.branch_off_points:
            lines = lines.union(branch_off.mileage.keys())
        return len(lines) > 1

    @property
    def is_station(self) -> bool:
        return (
            enums.StationType.STATION in self.station_types
            or enums.StationType.TECHNICAL_STATION in self.station_types
        )

    @property
    def is_traffic_post(self) -> bool:
        applicable_types = {
            enums.StationType.BLOCK_POST,
            enums.StationType.JUNCTION,
            enums.StationType.PASSING_LOOP,
        }
        return self.is_station or bool(
            applicable_types.intersection(self.station_types)
        )

    @property
    def is_line_section_boundary(self):
        return (
            self.is_traffic_post
            and self.station_types != [enums.StationType.BLOCK_POST]
        ) or self.station_types == [enums.StationType.LINES_MERGING]

    def should_issue_r307_for_train(self, train_number: int) -> Optional["Station"]:
        if self not in R307_ISSUERS:
            logging.info(f"{self.name} is not issuing R307.")
            return None
        for lower, upper, to_station in R307_ISSUERS[self]:
            if lower <= train_number <= upper:
                logger.info(
                    f"{self.name} issuing R307 for train number {train_number} until {to_station.name}."
                )
                return to_station
        logger.info(f"{self.name} not issuing R307 for train number {train_number}.")
        return None


_LK001 = base.Bookmark()
Katowice = Station(
    name="Katowice",
    lat=50.2576,
    lon=19.0163,
    mileage={1: 318.378, 137: 0.700, 138: 32.970, 139: 0},
    radio_channels=[enums.RadioChannel.R2],
    r307=True,
)
KatowiceZawodzie = Station(
    name="Katowice Zawodzie",
    lat=50.257,
    lon=19.0576,
    mileage={1: 315.653, 138: 30.243},
    radio_channels=[enums.RadioChannel.R2],
)
KatowiceSzopienicePoludniowe = Station(
    name="Katowice Szopienice Południowe",
    short_name="Kat. Szopienice Płd.",
    lat=50.2589012,
    lon=19.0923178,
    mileage={1: 312.91, 138: 27.505},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
SosnowiecGlownyPZSR52 = Station(
    name="Sosnowiec Gł. pzs R52",
    lat=50.272162,
    lon=19.11472,
    mileage={1: 310.684, 660: 1.117},
    radio_channels=[],
    station_types=[enums.StationType.LINES_MERGING],
    radio_recording=False,
)
SosnowiecGlowny = Station(
    name="Sosnowiec Główny",
    lat=50.279183,
    lon=19.126741,
    mileage={1: 309.544, 62: 84.054},
    radio_channels=[enums.RadioChannel.R2],
)
Bedzin = Station(
    name="Będzin",
    lat=50.3092276,
    lon=19.1411448,
    mileage={1: 305.524},
    radio_channels=[enums.RadioChannel.R2],
)
BedzinMiasto = Station(
    lat=50.3196,
    lon=19.1355,
    name="Będzin Miasto",
    mileage={1: 304.385},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
BedzinKsawera = Station(
    lat=50.330597,
    lon=19.158311,
    name="Będzin Ksawera",
    mileage={1: 302.077},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
DabrowaGornicza = Station(
    name="Dąbrowa Górnicza",
    lat=50.33032,
    lon=19.184849,
    mileage={1: 300.125},
    radio_channels=[enums.RadioChannel.R2],
)
DabrowaGorniczaGolonog = Station(
    lat=50.343906,
    lon=19.226074,
    name="Dąbrowa Górnicza Gołonóg",
    short_name="Dąbr. G. Gołonóg",
    mileage={1: 296.726},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
DabrowaGorniczaPogoria = Station(
    lat=50.350486,
    lon=19.240869,
    name="Dąbrowa Górnicza Pogoria",
    short_name="Dąbr. G. Pogoria",
    mileage={1: 295.398},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
DabrowaGorniczaZabkowice = Station(
    name="Dąbrowa Górnicza Ząbkowice",
    short_name="Dąbr. G. Ząbkowice",
    lat=50.3665,
    lon=19.2646,
    mileage={1: 292.896, 133: 0, 186: 291.721},
    radio_channels=[enums.RadioChannel.R2],
)
DabrowaGorniczaZabkowiceDZA = Station(
    name="Dąbrowa Górnicza Ząbkowice DZA",
    short_name="Dąbr. G. Ząbk. DZA",
    lat=50.3665,
    lon=19.2646,
    mileage={1: 291.777, 133: -1.114, 160: 292.896, 186: 290.607},
    radio_channels=[enums.RadioChannel.R2],
)
DabrowaGorniczaSikorka = Station(
    lat=50.3889,
    lon=19.299,
    name="Dąbrowa Górnicza Sikorka",
    short_name="Dąbr. G. Sikorka",
    mileage={1: 289.202, 186: 289.447},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Chruszczobrod = Station(
    lat=50.3998056,
    lon=19.329232,
    name="Chruszczobród",
    mileage={1: 286.557, 186: 286.713},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Wiesiolka = Station(
    lat=50.414670960748,
    lon=19.349284172058,
    name="Wiesiółka",
    mileage={1: 284.313, 186: 284.490},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
LazyLC = Station(
    name="Łazy Łc",
    lat=50.4292,
    lon=19.3907,
    mileage={1: 283.340, 154: 2.686, 160: 283.340, 186: 283.340},
    radio_channels=[enums.RadioChannel.R2],
)
Lazy = Station(
    lat=50.4292,
    lon=19.3907,
    name="Łazy",
    mileage={1: 280.654, 154: 0, 160: 283.654, 186: 280.654},
    radio_channels=[enums.RadioChannel.R2],
)
LazyLA = Station(
    lat=50.4292,
    lon=19.3907,
    name="Łazy Ła",
    mileage={1: 277.230, 154: -3.176, 160: 277.507, 186: 277.230},
    radio_channels=[enums.RadioChannel.R2],
)
Zawiercie = Station(
    name="Zawiercie",
    lat=50.481,
    lon=19.423,
    mileage={1: 274.227, 4: 224.050, 160: 274.227},
    radio_channels=[enums.RadioChannel.R2],
)
ZawiercieBorowePole = Station(
    lat=50.5105,
    lon=19.3992,
    name="Zawiercie Borowe Pole",
    radio_channels=[],
    mileage={1: 270.3},
    station_types=[enums.StationType.HALT],
)
MyszkowMrzyglod = Station(
    lat=50.5435993,
    lon=19.3770075,
    name="Myszków Mrzygłód",
    radio_channels=[],
    mileage={1: 266.37},
    station_types=[enums.StationType.HALT],
)
MyszkowSwiatowit = Station(
    name="Myszków Światowit",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 263.442},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
MyszkowGt = Station(
    name="Myszków GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 261.797},
    radio_channels=[],
    station_types=[enums.StationType.FREIGHT_GROUP],
    skippable=True,
)
Myszkow = Station(
    name="Myszków",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 261.016},
    radio_channels=[],
    is_boundary=True,
)
MyszkowNowaWies = Station(
    name="Myszków Nowa Wieś",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 257.525},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Zarki_Letnisko = Station(
    name="Żarki-Letnisko",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 254.088},
    radio_channels=[],
)
MaslonskieNatalin = Station(
    name="Masłońskie Natalin",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 250.787},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Poraj = Station(
    name="Poraj",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 246.95},
    radio_channels=[],
)
PorajGt = Station(
    name="Poraj GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 245.85},
    radio_channels=[],
    station_types=[enums.StationType.FREIGHT_GROUP],
)
Korwinow = Station(
    name="Korwinów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 239.158},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
CzestochowaRakow = Station(
    name="Częstochowa Raków",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 233.379},
    radio_channels=[],
)
CzestochowaTowCtb = Station(
    name="Częstochowa Tow Ctb",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 233.04},
    radio_channels=[],
)
CzestochowaTowarowa = Station(
    name="Częstochowa Towarowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 232.02},
    radio_channels=[],
    r307=True,
)
Czestochowa = Station(
    name="Częstochowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 229.745},
    radio_channels=[],
    r307=True,
)
CzestochowaAniolow = Station(
    name="Częstochowa Aniołów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 225.816},
    radio_channels=[],
)
Wyczerpy = Station(
    name="Wyczerpy",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 222.755},
    radio_channels=[],
)
RudnikiKoloCzestochowy = Station(
    name="Rudniki koło Częstochowy",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 217.7},
    radio_channels=[],
)
Rzerzeczyce = Station(
    name="Rzerzęczyce",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 210.606},
    radio_channels=[],
)
Klomnice = Station(
    name="Kłomnice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 208.201},
    radio_channels=[],
)
Jackow = Station(
    name="Jacków",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 202.758},
    radio_channels=[],
)
WidzowTeklinow = Station(
    name="Widzów Teklinów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 200.525},
    radio_channels=[],
)
Bobry = Station(
    name="Bobry",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 194.756},
    radio_channels=[],
)
Radomsko = Station(
    name="Radomsko",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 189.133},
    radio_channels=[],
)
RadomskoGt = Station(
    name="Radomsko GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 188.135},
    radio_channels=[],
)
DobryszyceKoloRadomska = Station(
    name="Dobryszyce koło Radomska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 183.452},
    radio_channels=[],
)
Gomunice = Station(
    name="Gomunice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 177.694},
    radio_channels=[],
)
GomuniceGt = Station(
    name="Gomunice GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 177.055},
    radio_channels=[],
)
Kamiensk = Station(
    name="Kamieńsk",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 175.004},
    radio_channels=[],
)
Gorzedow = Station(
    name="Gorzędów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 171.66},
    radio_channels=[],
)
Gorzkowice = Station(
    name="Gorzkowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 166.718},
    radio_channels=[],
)
GorzkowiceGt = Station(
    name="Gorzkowice GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 166.057},
    radio_channels=[],
)
Wilkoszewice = Station(
    name="Wilkoszewice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 162.533},
    radio_channels=[],
)
Luciazanka = Station(
    name="Luciążanka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 159.433},
    radio_channels=[],
)
Rozprza = Station(
    name="Rozprza",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 156.539},
    radio_channels=[],
)
Milejow = Station(
    name="Milejów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 150.389},
    radio_channels=[],
)
PiotrkowTrybTow = Station(
    name="Piotrków Tryb Tow",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 145.0},
    radio_channels=[],
)
PiotrkowTrybunalski = Station(
    name="Piotrków Trybunalski",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 144.242},
    radio_channels=[],
)
Jarosty = Station(
    name="Jarosty",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 138.545},
    radio_channels=[],
)
Moszczenica = Station(
    name="Moszczenica",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 133.825},
    radio_channels=[],
)
Baby = Station(
    name="Baby",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 129.944},
    radio_channels=[],
)
BabyGt = Station(
    name="Baby GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 129.296},
    radio_channels=[],
)
Wolborka = Station(
    name="Wolbórka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 123.399},
    radio_channels=[],
)
Laznow = Station(
    name="Łaznów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 118.651},
    radio_channels=[],
)
Rokiciny = Station(
    name="Rokiciny",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 114.176},
    radio_channels=[],
)
RokicinyGt = Station(
    name="Rokiciny GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 113.454},
    radio_channels=[],
)
ChrustyNowe = Station(
    name="Chrusty Nowe",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 111.011},
    radio_channels=[],
)
KoluszkiPzsR154 = Station(
    name="Koluszki PZS R154",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 107.362},
    radio_channels=[],
)
Wagry = Station(
    name="Wągry",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 99.619},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Rogow = Station(
    name="Rogów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 95.723},
    radio_channels=[enums.RadioChannel.R2],
)
PrzylekDuzy = Station(
    name="Przyłęk Duży",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 92.345},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Krosnowa = Station(
    name="Krosnowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 89.822},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
LipceReymontowskie = Station(
    name="Lipce Reymontowskie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 84.71},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
PlycwiaGt = Station(
    name="Płyćwia GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 80.755},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.FREIGHT_GROUP],
)
Plycwia = Station(
    name="Płyćwia",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 80.131},
    radio_channels=[enums.RadioChannel.R2],
)
Makow = Station(
    name="Maków",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 75.372},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
DabrowiceSkierniewickie = Station(
    name="Dąbrowice Skierniewickie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 71.355},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
SkierniewicePPzs = Station(
    name="Skierniewice P PZS",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 67.831},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.LINES_MERGING],
)
Skierniewice = Station(
    name="Skierniewice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 65.926},
    radio_channels=[enums.RadioChannel.R2],
    r307=True,
)
SkierniewiceGt201_208 = Station(
    name="Skierniewice GT 201-208",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 64.381},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.FREIGHT_GROUP],
)
SkierniewiceMPzs = Station(
    name="Skierniewice M PZS",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 61.973},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.LINES_MERGING],
)
SuchaZyrardowska = Station(
    name="Sucha Żyrardowska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 50.033},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Jesionka = Station(
    name="Jesionka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 51.959},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
RadziwillowMazowiecki = Station(
    name="Radziwiłłów Mazowiecki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 55.403},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.HALT, enums.StationType.JUNCTION],
)
SkierniewiceRawka = Station(
    name="Skierniewice Rawka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 60.779},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Zyrardow = Station(
    name="Żyrardów",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={1: 43.141, 529: -18.314},  # @TODO: Issue with SimRail data
    radio_channels=[enums.RadioChannel.R2],
    is_boundary=True,
)
Jaktorow = Station(
    name="Jaktorów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 35.034},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Miedzyborow = Station(
    name="Międzyborów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 40.437},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Pruszkow = Station(
    name="Pruszków",
    lat=52.1683,
    lon=20.7987,
    mileage={1: 15.891, 447: 15.891},
    radio_channels=[enums.RadioChannel.R2],
)
Jozefinow = Station(
    name="Józefinów",
    lat=52.186014,
    lon=20.852936,
    mileage={1: 12.088, 19: 5.438},
    radio_recording=False,
    station_types=[enums.StationType.JUNCTION],
    radio_channels=[enums.RadioChannel.R2],
)
WarszawaWlochy = Station(
    name="Warszawa Włochy",
    lat=52.206206,
    lon=20.914761,
    mileage={1: 6.804, 3: 6.804, 447: 6.804},
    station_types=[enums.StationType.HALT, enums.StationType.JUNCTION],
    radio_channels=[enums.RadioChannel.R2],
)
WarszawaZachodnia = Station(
    name="Warszawa Zachodnia",
    lat=52.22,
    lon=20.9652,
    mileage={1: 3.082, 2: -3.082, 447: 3.082},
    radio_channels=[enums.RadioChannel.R2],
)
WarszawaZachodniaR10 = Station(
    name="Warszawa Zach. R10",
    lat=52.22,
    lon=20.9652,
    mileage={2: -2.515},
    radio_channels=[],
    radio_recording=False,
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=WarszawaZachodnia,
    skippable=True,
)
WarszawaZachodniaR19 = Station(
    name="Warszawa Zach. R19",
    lat=52.22,
    lon=20.9652,
    mileage={1: 2.620, 2: -2.620},
    radio_channels=[],
    radio_recording=False,
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=WarszawaZachodnia,
    skippable=True,
)
WarszawaCentralna = Station(
    name="Warszawa Centralna",
    lat=52.228765443166,
    lon=21.003338098526,
    mileage={2: 0},
    radio_channels=[enums.RadioChannel.R2],
)

_LK002 = base.Bookmark()
WarszawaWschodnia = Station(
    name="Warszawa Wschodnia",
    lat=52.2515628,
    lon=21.052267,
    mileage={2: 4.254, 9: 4.254, 45: 0},
    r307=True,
    radio_channels=[enums.RadioChannel.R2],
)
WarszawaWschodniaR34 = Station(
    name="Warszawa Wsch.R.34",
    lat=52.2515628,
    lon=21.052267,
    mileage={2: 4.407, 9: 4.407},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    radio_recording=False,
    belongs_to=WarszawaWschodnia,
    skippable=True,
)
WarszawaPodskarbinska = Station(
    name="Warszawa Podskarbińska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={2: 5.988},
    radio_channels=[enums.RadioChannel.R7],
    station_types=[enums.StationType.JUNCTION],
)

_LK004 = base.Bookmark()
GrodziskMazowiecki = Station(
    name="Grodzisk Mazowiecki",
    short_name="Grodz Maz",
    lat=52.1101,
    lon=20.6229,
    mileage={1: 29.548, 4: 0, 447: 29.548},
    radio_channels=[enums.RadioChannel.R2],
)
GrodziskMazowieckiR58 = Station(
    name="Grodzisk Maz. R58",
    lat=52.1101,
    lon=20.6229,
    mileage={1: 30.634, 4: 1.091},
    radio_channels=[],
    radio_recording=False,
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=GrodziskMazowiecki,
    skippable=True,
)
Korytow = Station(
    name="Korytów",
    lat=52.020283,
    lon=20.495038,
    mileage={4: 14.574},
    radio_channels=[enums.RadioChannel.R1],
)
Szeligi = Station(
    name="Szeligi",
    lat=51.948,
    lon=20.461,
    mileage={4: 23.542, 575: 2.974},
    radio_channels=[enums.RadioChannel.R1],
)
BialaRawska = Station(
    name="Biała Rawska",
    lat=51.795,
    lon=20.4394,
    mileage={4: 40.122},
    radio_channels=[enums.RadioChannel.R1],
    station_types=[enums.StationType.JUNCTION],
)
Strzalki = Station(
    name="Strzałki",
    lat=51.6431,
    lon=20.4048,
    mileage={4: 57.381},
    radio_channels=[enums.RadioChannel.R1],
)
Idzikowice = Station(
    name="Idzikowice",
    lat=51.4486,
    lon=20.3105,
    mileage={4: 80.738, 573: 0, 574: 4.597},
    radio_channels=[enums.RadioChannel.R1],
)
OpocznoPoludnie = Station(
    name="Opoczno Południe",
    lat=51.3591,
    lon=20.2323,
    mileage={4: 92.142},
    radio_channels=[enums.RadioChannel.R1],
)
Pilichowice = Station(
    name="Pilichowice",
    lat=51.253696561736,
    lon=20.120944976807,
    mileage={4: 106.588},
    radio_channels=[enums.RadioChannel.R1],
    station_types=[enums.StationType.JUNCTION],
)
Olszamowice = Station(
    name="Olszamowice",
    lat=51.0916,
    lon=20.066,
    mileage={4: 124.828},
    radio_channels=[enums.RadioChannel.R1],
)
WloszczowaPolnoc = Station(
    name="Włoszczowa Północ",
    short_name="Włoszczowa Płn",
    lat=50.8567035,
    lon=19.9461079,
    mileage={4: 154.390, 572: -0.740},
    radio_channels=[enums.RadioChannel.R1],
)
Knapowka = Station(
    name="Knapówka",
    lat=50.8023,
    lon=19.906,
    mileage={4: 160.588, 571: 3.830},
    radio_channels=[enums.RadioChannel.R1],
    station_types=[enums.StationType.JUNCTION],
)
KnapowkaR2 = Station(
    name="Knapówka R2",
    lat=50.8023,
    lon=19.906,
    mileage={4: 160.500, 571: 3.742},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    radio_recording=False,
    belongs_to=Knapowka,
    skippable=True,
)
Psary = Station(
    name="Psary",
    lat=50.7336,
    lon=19.8163,
    mileage={4: 170.479, 570: 0},
    radio_channels=[enums.RadioChannel.R1],
)
GoraWlodowska = Station(
    name="Góra Włodowska",
    lat=50.5846,
    lon=19.4651,
    mileage={4: 206.688},
    radio_channels=[enums.RadioChannel.R1],
)

_LK008 = base.Bookmark()
KrakowGlowny = Station(
    name="Kraków Główny",
    lat=50.0682894,
    lon=19.9479103,
    mileage={8: 319.440},
    radio_channels=[enums.RadioChannel.R1],
    r307=True,
)
KrakowPrzedmiescie = Station(
    name="Kraków Przedmieście",
    lat=50.0847,
    lon=19.9498,
    mileage={8: 317.426},
    radio_channels=[enums.RadioChannel.R1],
    station_types=[enums.StationType.JUNCTION],
)
KrakowBatowice = Station(
    name="Kraków Batowice",
    lat=50.1074511,
    lon=19.9955463,
    mileage={8: 313.275},
    radio_channels=[enums.RadioChannel.R1],
)
Raciborowice = Station(
    name="Raciborowice",
    lat=50.110836,
    lon=20.02813,
    mileage={8: 310.832},
    radio_channels=[enums.RadioChannel.R1],
    station_types=[enums.StationType.JUNCTION],
)
Zastow = Station(
    name="Zastów",
    lat=50.1237424,
    lon=20.0690603,
    mileage={8: 307.946},
    radio_channels=[enums.RadioChannel.R1],
)
Baranowka = Station(
    name="Baranówka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 304.18},
    radio_channels=[],
)
Luczyce = Station(
    name="Łuczyce",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 301.57},
    radio_channels=[],
)
Goszcza = Station(
    name="Goszcza",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 298.89},
    radio_channels=[],
)
Niedzwiedz = Station(
    name="Niedźwiedź",
    lat=50.2043191,
    lon=20.0809479,
    mileage={8: 295.782},
    radio_channels=[enums.RadioChannel.R1],
)
SlomnikiMiasto = Station(
    name="Słomniki Miasto",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 292.211},
    radio_channels=[],
)
Slomniki = Station(
    name="Słomniki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 290.541},
    radio_channels=[enums.RadioChannel.R1],
)
Smrokow = Station(
    name="Smroków",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 287.322},
    radio_channels=[],
)
Szczepanowice = Station(
    name="Szczepanowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 283.934},
    radio_channels=[],
)
Kamienczyce = Station(
    name="Kamieńczyce",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 280.724},
    radio_channels=[],
)
Dziadowki = Station(
    name="Dziadówki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 272.194},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Miechow = Station(
    name="Miechów",
    lat=50.353,
    lon=20.0104,
    mileage={8: 277.343},
    is_boundary=True,
    radio_channels=[enums.RadioChannel.R1],
)
Kozlow = Station(
    name="Kozłów",
    lat=50.4748,
    lon=20.0121,
    mileage={8: 262.098, 64: 0},
    radio_channels=[enums.RadioChannel.R4],
)
Klimontow = Station(
    name="Klimontów",
    lat=50.525388,
    lon=20.030168,
    mileage={8: 256.243},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Gniewiecin = Station(
    name="Gniewiecin",
    lat=50.540817,
    lon=20.044427,
    mileage={8: 254.285},
    station_types=[enums.StationType.BLOCK_POST],
    radio_channels=[enums.RadioChannel.R4],
    radio_recording=False,
)
Sedziszow = Station(
    name="Sędziszów",
    lat=50.5659,
    lon=20.0549,
    mileage={8: 251.232},
    radio_channels=[enums.RadioChannel.R4],
)
SedziszowTowarowy = Station(
    name="Sędziszów Towarowy",
    lat=50.5659,
    lon=20.0549,
    mileage={8: 250.520},
    radio_channels=[enums.RadioChannel.R4],
    is_boundary=True,
)
Potok = Station(
    name="Potok",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 238.263},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Krzciecice = Station(
    name="Krzcięcice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 244.543},
    station_types=[enums.StationType.BLOCK_POST, enums.StationType.HALT],
    radio_channels=[enums.RadioChannel.R4],
    radio_recording=False,
)
Jedrzejow = Station(
    name="Jędrzejów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 231.665},
    radio_channels=[enums.RadioChannel.R4],
)
Podchojny = Station(
    name="Podchojny",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 227.408},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.BLOCK_POST],
    radio_recording=False,
)
Miasowa = Station(
    name="Miąsowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 219.490},
    radio_channels=[enums.RadioChannel.R4],
)
Sobkow = Station(
    name="Sobków",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 211.877},
    radio_channels=[enums.RadioChannel.R4],
)
Wolica = Station(
    name="Wolica",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 207.761},
    radio_channels=[enums.RadioChannel.R4],
)
SitkowkaNowiny = Station(
    name="Sitkówka Nowiny",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 197.330},
    radio_channels=[enums.RadioChannel.R4],
)
KielceSlowik = Station(
    name="Kielce Słowik",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 195.368},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
KielceBialogon = Station(
    name="Kielce Białogon",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 191.870},
    radio_channels=[enums.RadioChannel.R4],
)
Kielce = Station(
    name="Kielce",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 187.672, 61: 0},
    radio_channels=[enums.RadioChannel.R4],
    r307=True,
)
PiaskiKoloKielc = Station(
    name="Piaski koło Kielc",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 185.500},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.JUNCTION],
)
Kostomloty = Station(
    name="Kostomłoty",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 182.060},
    radio_channels=[enums.RadioChannel.R4],
)
Zagnansk = Station(
    name="Zagnańsk",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 171.297},
    radio_channels=[enums.RadioChannel.R4],
)
Lekomin = Station(
    name="Lekomin",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 168.023},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.BLOCK_POST],
    radio_recording=False,
)
Ostojow = Station(
    name="Ostojow",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 163.303},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.BLOCK_POST],
    radio_recording=False,
)
Laczna = Station(
    name="Łączna",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 160.271},
    radio_channels=[enums.RadioChannel.R4],
)
Suchedniow = Station(
    name="Suchedniów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 152.404},
    radio_channels=[enums.RadioChannel.R4],
)
SuchedniowPolnocny = Station(
    name="Suchedniów Północny",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 150.037},
    radio_channels=[enums.RadioChannel.R4],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST, enums.StationType.HALT],
)
SkarzyskoKamienna = Station(
    name="Skarżysko-Kamienna",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 143.442},
    radio_channels=[enums.RadioChannel.R4],
    r307=True,
)

_LK009 = base.Bookmark()
WarszawaPraga = Station(
    name="Warszawa Praga",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={9: 10.100},
    radio_channels=[],
    is_boundary=True,
)

_LK014 = base.Bookmark()
LodzKaliskaTowarowaPzsLkt = Station(
    name="Łódź Kaliska Towarowa PZS ŁKT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 0.0, 25: 1.229},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.LINES_MERGING],
)
Retkinia = Station(
    name="Retkinia",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 2.35},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)
Lublinek = Station(
    name="Lublinek",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 7.14},
    radio_channels=[enums.RadioChannel.R5],
)
Pabianice = Station(
    name="Pabianice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 14.49},
    radio_channels=[enums.RadioChannel.R5],
)
Dobron = Station(
    name="Dobroń",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 21.17},
    radio_channels=[enums.RadioChannel.R5],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST, enums.StationType.HALT],
)
Lask = Station(
    name="Łask",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 30.849},
    radio_channels=[enums.RadioChannel.R5],
)
Borszewice = Station(
    name="Borszewice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 36.181},
    radio_channels=[enums.RadioChannel.R5],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST, enums.StationType.HALT],
)
Gajewniki = Station(
    name="Gajewniki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 39.842},
    radio_channels=[enums.RadioChannel.R5],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST],
)
ZdunskaWola = Station(
    name="Zduńska Wola",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 42.36},
    radio_channels=[enums.RadioChannel.R5],
)
Meka = Station(
    name="Męka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 53.49},
    radio_channels=[enums.RadioChannel.R5],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST],
)
Sieradz = Station(
    name="Sieradz",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 59.435},
    radio_channels=[enums.RadioChannel.R5],
)
Sedzice = Station(
    name="Sędzice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 70.614},
    radio_channels=[enums.RadioChannel.R5],
)
Blaszki = Station(
    name="Błaszki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 79.272},
    radio_channels=[enums.RadioChannel.R5],
)
Radliczyce = Station(
    name="Radliczyce",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 89.478},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)
Opatowek = Station(
    name="Opatówek",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 98.311},
    radio_channels=[enums.RadioChannel.R5],
)
Piwonice = Station(
    name="Piwonice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 107.954},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)
Kalisz = Station(
    name="Kalisz",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 112.133},
    radio_channels=[enums.RadioChannel.R5],
)
NoweSkalmierzyce = Station(
    name="Nowe Skalmierzyce",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 118.643},
    radio_channels=[enums.RadioChannel.R5],
)
Czekanow = Station(
    name="Czekanów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 129.071},
    radio_channels=[enums.RadioChannel.R5],
)
StaryStaw = Station(
    name="Stary Staw",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 132.275},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)
OstrowWielkopolski = Station(
    name="Ostrów Wielkopolski",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 136.121, 355: 0},
    radio_channels=[enums.RadioChannel.R5],
)
OstrowWielkopolskiZachodni = Station(
    name="Ostrów Wielkopolski Zachodni",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 138.582},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.TECHNICAL_STATION],
)
Biadki = Station(
    name="Biadki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 153.88},
    radio_channels=[enums.RadioChannel.R5],
)

_LK017 = base.Bookmark()
Koluszki = Station(
    name="Koluszki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 105.194, 17: 26.197},
    radio_channels=[enums.RadioChannel.R2, enums.RadioChannel.R7],
)
KoluszkiPzsR145 = Station(
    name="Koluszki PZS R145",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={17: 24.261},
    radio_channels=[enums.RadioChannel.R7],
    station_types=[enums.StationType.LINES_MERGING],
)
Zakowice = Station(
    name="Żakowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={17: 23.503},
    radio_channels=[],
)
Galkowek = Station(
    name="Gałkówek",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={17: 19.197},
    radio_channels=[enums.RadioChannel.R7],
)
Justynow = Station(
    name="Justynów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={17: 15.921},
    radio_channels=[],
)
Bedon = Station(
    name="Bedoń",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={17: 13.05},
    radio_channels=[],
)

_LK19 = base.Bookmark()
WarszawaGlTowSr18 = Station(
    name="Warszawa Gł.Tow.Sr18",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={19: 1.094},
    radio_channels=[],
    is_boundary=True,
)

_LK020 = base.Bookmark()
WarszawaGlownaTowarowa = Station(
    name="Warszawa Główna Towarowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={20: -0.600},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.TECHNICAL_STATION],
)
WarszawaGlTowWoa = Station(
    name="Warszawa Gł.Tow. WOA",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={20: 0.0},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.TECHNICAL_STATION],
    r307=True,
)
WarszawaCzyste = Station(
    name="Warszawa Czyste",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={20: 3.412},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.TECHNICAL_STATION],
)
WarszawaGdanska = Station(
    name="Warszawa Gdańska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={20: 10.534},
    radio_channels=[enums.RadioChannel.R2],
)

_LK022 = base.Bookmark()
TomaszowMazowieckiBialobrzegi = Station(
    name="Tomaszów Mazowiecki Białobrzegi",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={22: 3.585},
    radio_channels=[enums.RadioChannel.R1],
)
Antoniow = Station(
    name="Antoniów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={22: 15.894},
    radio_channels=[enums.RadioChannel.R1],
)
DebaOpoczynska = Station(
    name="Dęba Opoczyńska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={22: 20.028},
    radio_channels=[enums.RadioChannel.R1],
)
Radzice = Station(
    name="Radzice",
    lat=51.466734509069,
    lon=20.397191047668,
    mileage={22: 28.43, 573: 5.099},
    radio_channels=[enums.RadioChannel.R1],
    is_boundary=True,
)
RadzicePzsR31 = Station(
    name="Radzice PZS R31",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={22: 25.680, 574: -0.025},
    radio_channels=[],
    is_boundary=True,
    station_types=[enums.StationType.LINES_MERGING],
    belongs_to=Radzice,
)
RadziceR12 = Station(
    name="Radzice R12",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={22: 28.423, 573: 5.098},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=Radzice,
    skippable=True,
)
Drzewica = Station(
    name="Drzewica",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={22: 35.993},
    radio_channels=[enums.RadioChannel.R1],
    r307=True,
)

_LK025 = base.Bookmark()
LodzWidzew = Station(
    name="Łódź Widzew",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={17: 5.267, 540: 6.905},
    radio_channels=[enums.RadioChannel.R7],
)
LodzChojny = Station(
    name="Łódź Chojny",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={25: 6.926, 540: 0.832},
    radio_channels=[enums.RadioChannel.R7],
)
TomaszowMazowiecki = Station(
    name="Tomaszów Mazowiecki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={25: 55.7},
    radio_channels=[],
)

_LK045 = base.Bookmark()
WarszawaWschodniaR58 = Station(
    name="Warszawa Wsch. R.58",
    lat=52.2515628,
    lon=21.052267,
    mileage={9: 4.938, 45: 0.684},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    radio_recording=False,
    belongs_to=WarszawaWschodnia,
    skippable=True,
)

_LK061 = base.Bookmark()
KielceHerbskie = Station(
    name="Kielce Herbskie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 2.254},
    radio_channels=[enums.RadioChannel.R3],
)
KielceHerbskieKHA = Station(
    name="Kielce Herbskie Kha",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 3.299},
    radio_channels=[enums.RadioChannel.R3],
)
KielceHerbskieKHB = Station(
    name="Kielce Herbskie Khb",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 5.600},
    radio_channels=[enums.RadioChannel.R3],
)
GorkiSzczukowskie = Station(
    name="Górki Szczukowskie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 8.336},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.HALT, enums.StationType.JUNCTION],
)
Szczukowice = Station(
    name="Szczukowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 10.712},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.JUNCTION],
)
Rykoszyn = Station(
    name="Rykoszyn",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 18.235},
    radio_channels=[enums.RadioChannel.R3],
)
Malogoszcz = Station(
    name="Małogoszcz",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 27.306},
    radio_channels=[enums.RadioChannel.R3],
)
MalogoszczPZSR35 = Station(
    name="Małogoszcz PZS R35",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 28.058},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.LINES_MERGING],
)
Ludynia = Station(
    name="Ludynia",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 36.699},
    radio_channels=[enums.RadioChannel.R3],
)
Wloszczowa = Station(
    name="Włoszczowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 47.735},
    radio_channels=[enums.RadioChannel.R3],
)
Czarnca = Station(
    name="Czarnca",
    lat=50.8238578,
    lon=19.9446487,
    mileage={61: 53.035, 571: 0},
    is_boundary=True,
    radio_channels=[enums.RadioChannel.R1],
    station_types=[enums.StationType.HALT, enums.StationType.JUNCTION],
)
CzarncaR19 = Station(
    name="Czarnca R19",
    lat=50.8238578,
    lon=19.9446487,
    mileage={61: 53.700, 571: 0.439},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=Czarnca,
    radio_recording=False,
    skippable=True,
)
Zelislawice = Station(
    name="Żelisławice",
    lat=50.80373793,
    lon=19.858560562134,
    mileage={61: 59.716, 572: 8.409},
    radio_channels=[enums.RadioChannel.R1],
    is_boundary=True,
    r307=True,
)
Koniecpol = Station(
    name="Koniecpol",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 71.478},
    radio_channels=[],
)
KoniecpolMagdasz = Station(
    name="Koniecpol Magdasz",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 74.854},
    radio_channels=[],
)
Podlesie = Station(
    name="Podlesie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 78.508},
    radio_channels=[],
)
StaropoleCzestochowskie = Station(
    name="Staropole Częstochowskie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 83.935},
    radio_channels=[],
)
Julianka = Station(
    name="Julianka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 87.888},
    radio_channels=[],
)
Luslawice = Station(
    name="Lusławice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 93.962},
    radio_channels=[],
)
Turow = Station(
    name="Turów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 99.679},
    radio_channels=[],
)
Kucelinka = Station(
    name="Kucelinka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 110.251},
    radio_channels=[],
)
CzestochowaStradom = Station(
    name="Częstochowa Stradom",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={
        61: 117.223,
        703: 2.7,
    },  # @TODO: Bug in SimRail data? Stradom's not on line 703
    radio_channels=[],
)
CzestochowaGnaszyn = Station(
    name="Częstochowa Gnaszyn",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 122.963},
    radio_channels=[],
)
Blachownia = Station(
    name="Blachownia",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 127.777},
    radio_channels=[],
)
HerbyStare = Station(
    name="Herby Stare",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 134.666},
    radio_channels=[],
)
Liswarta = Station(
    name="Liswarta",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 138.615},
    radio_channels=[],
)
Lisow = Station(
    name="Lisów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 141.799},
    radio_channels=[],
)
Kochanowice = Station(
    name="Kochanowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 145.837},
    radio_channels=[],
)
Jawornica = Station(
    name="Jawornica",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 149.84},
    radio_channels=[],
)
Lubliniec = Station(
    name="Lubliniec",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 152.231},
    radio_channels=[],
)
Pawonkow = Station(
    name="Pawonków",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 161.223},
    radio_channels=[],
)
Pludry = Station(
    name="Pludry",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 168.443},
    radio_channels=[],
)

_LK062 = base.Bookmark()
Tunel = Station(
    name="Tunel",
    lat=50.433946533387,
    lon=19.991426467896,
    mileage={8: 267.778, 62: 0.750},
    radio_channels=[enums.RadioChannel.R4],
)
TunelR13 = Station(
    name="Tunel R13",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={8: 268.527, 62: 1.229},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    radio_recording=False,
    belongs_to=Tunel,
    skippable=True,
)
Charsznica = Station(
    name="Charsznica",
    lat=50.3962,
    lon=19.9408,
    mileage={62: 7.793},
    radio_channels=[enums.RadioChannel.R4],
)
Gajowka = Station(
    lat=50.394642,
    lon=19.878629,
    name="Gajówka",
    mileage={62: 12.5},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
GajowkaAPO = Station(
    name="Gajówka APO",
    lat=50.394642,
    lon=19.878629,
    mileage={62: 13.755},
    radio_channels=[enums.RadioChannel.R4],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST],
    remotely_controlled_from="Wb",
)
Jezowka = Station(
    lat=50.39931,
    lon=19.815715,
    name="Jeżówka",
    mileage={62: 16.894},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Wolbrom = Station(
    name="Wolbrom",
    lat=50.375983,
    lon=19.77229,
    mileage={62: 22.296},
    radio_channels=[enums.RadioChannel.R4],
    remote_control_facilities=True,
)
Zarzecze = Station(
    lat=50.363169,
    lon=19.698545,
    name="Zarzecze",
    mileage={62: 28.0},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
ZarzeczeAPO = Station(
    name="Zarzecze APO",
    lat=50.363169,
    lon=19.698545,
    mileage={62: 29.127},
    radio_channels=[enums.RadioChannel.R4],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST],
    remotely_controlled_from="Wb",
)
ChrzastowiceOlkuskie = Station(
    lat=50.343208,
    lon=19.68507,
    name="Chrząstowice Olkuskie",
    mileage={62: 30.56},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
JaroszowiecOlkuski = Station(
    name="Jaroszowiec Olkuski",
    lat=50.342235,
    lon=19.621598,
    mileage={62: 35.744},
    radio_channels=[enums.RadioChannel.R4],
)
Olkusz = Station(
    name="Olkusz",
    lat=50.274383,
    lon=19.570979,
    mileage={62: 45.021},
    radio_channels=[enums.RadioChannel.R4],
)
Bukowno = Station(
    name="Bukowno",
    lat=50.26390811538,
    lon=19.458825588226,
    mileage={62: 53.538},
    radio_channels=[enums.RadioChannel.R4],
)
BukownoPrzymiarki = Station(
    lat=50.27536,
    lon=19.409215,
    name="Bukowno Przymiarki",
    mileage={62: 57.338},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Slawkow = Station(
    name="Sławków",
    lat=50.295464,
    lon=19.373682,
    mileage={62: 61.261},
    radio_channels=[enums.RadioChannel.R4],
)
DabrowaGorniczaWschodnia = Station(
    name="Dąbrowa Górnicza Wschodnia",
    short_name="Dąbr. G. Wschodnia",
    lat=50.3033,
    lon=19.3104,
    mileage={62: 65.941, 171: 12.290},
    radio_channels=[enums.RadioChannel.R4],
)
DabrowaGorniczaStrzemieszyce = Station(
    name="Dąbrowa Górnicza Strzemieszyce",
    short_name="Dąbr. G. Strzem.",
    lat=50.3109,
    lon=19.2681,
    mileage={62: 69.221, 162: 0},
    radio_channels=[enums.RadioChannel.R4],
)
SosnowiecKazimierz = Station(
    name="Sosnowiec Kazimierz",
    short_name="Sosn. Kazimierz",
    lat=50.2882425,
    lon=19.2316961,
    mileage={62: 73.608, 163: 0},
    radio_channels=[enums.RadioChannel.R4],
)
SosnowiecKazimierzPZSSKZ2 = Station(
    name="Sosnowiec Kazimierz PZS SKZ2",
    lat=50.2882425,
    lon=19.2316961,
    mileage={62: 74.698, 663: 0},
    radio_channels=[],
    station_types=[enums.StationType.LINES_MERGING],
    radio_recording=False,
    skippable=True,
)
SosnowiecPorabka = Station(
    lat=50.272042,
    lon=19.216252,
    name="Sosnowiec Porąbka",
    mileage={62: 75.685},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
SosnowiecDandowka = Station(
    name="Sosnowiec Dańdówka",
    short_name="Sosn. Dańdówka",
    lat=50.2655,
    lon=19.1736,
    mileage={62: 78.930, 171: 24.549},
    radio_channels=[enums.RadioChannel.R5],
)
SosnowiecPoludniowy = Station(
    name="Sosnowiec Południowy",
    short_name="Sosnowiec Płd.",
    lat=50.269723712063,
    lon=19.125287532806,
    mileage={62: 82.737, 660: -0.399},
    radio_channels=[enums.RadioChannel.R5],
)

_LK064 = base.Bookmark()
Sprowa = Station(
    name="Sprowa",
    lat=50.5926,
    lon=19.8828,
    mileage={64: 17.675},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)
Starzyny = Station(
    name="Starzyny",
    lat=50.715,
    lon=19.8002,
    mileage={64: 32.570, 570: 2.932},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)

_LK073 = base.Bookmark()
Brzeziny = Station(
    name="Brzeziny",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={73: 4.771},
    radio_channels=[],
)
Nida = Station(
    name="Nida",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={73: 6.822},
    radio_channels=[],
)
Wloszczowice = Station(
    name="Włoszczowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={73: 19.542},
    radio_channels=[],
)
Kije = Station(
    name="Kije",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={73: 24.74},
    radio_channels=[],
)
Busko_Zdroj = Station(
    name="Busko-Zdrój",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={73: 43.3},
    radio_channels=[],
)

_LK095 = base.Bookmark()
Dlubnia = Station(
    name="Dłubnia",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={95: 13.15},
    radio_channels=[],
    is_boundary=True,
)
KrakowNowaHutaNha = Station(
    name="Kraków Nowa Huta Nha",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={95: 20.48},
    radio_channels=[],
)
KrakowNowaHutaNhaGttr = Station(
    name="Kraków Nowa Huta NHA GTTR",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={95: 21.176},
    radio_channels=[],
)

_LK132 = base.Bookmark()
WroclawGlownyWgb = Station(
    name="Wrocław Główny Wgb",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 178.707},
    radio_channels=[],
)
WroclawBrochowPodg = Station(
    name="Wrocław Brochów PODG",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 173.124},
    radio_channels=[],
)
SwietaKatarzyna = Station(
    name="Święta Katarzyna",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 170.974},
    radio_channels=[],
)
Olawa = Station(
    name="Oława",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 154.513},
    radio_channels=[],
)
Brzeg = Station(
    name="Brzeg",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 139.447},
    radio_channels=[],
)
LewinBrzeski = Station(
    name="Lewin Brzeski",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 124.715},
    radio_channels=[],
)
DabrowaNiemodlinska = Station(
    name="Dąbrowa Niemodlińska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 112.385},
    radio_channels=[],
)
OpoleZachodnie = Station(
    name="Opole Zachodnie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 102.085, 280: 0},  # 280 is a mistake on SimRail's side it seems?
    radio_channels=[],
)
OpoleGroszowice = Station(
    name="Opole Groszowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 95.769},
    radio_channels=[],
)
OpoleGroszowiceOga = Station(
    name="Opole Groszowice OGA",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 95.241},
    radio_channels=[],
)
OpoleGlowne = Station(
    name="Opole Główne",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 99.322, 144: 75.924},
    radio_channels=[],
)
TarnowOpolski = Station(
    name="Tarnów Opolski",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 84.585},
    radio_channels=[],
)
KamienSlaski = Station(
    name="Kamień Śląski",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 80.523},
    radio_channels=[],
)
Szymiszow = Station(
    name="Szymiszów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 73.004},
    radio_channels=[],
)
StrzelceOpolskie = Station(
    name="Strzelce Opolskie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 66.931},
    radio_channels=[],
)
BlotnicaStrzelecka = Station(
    name="Błotnica Strzelecka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 59.118},
    radio_channels=[],
)
Kotulin = Station(
    name="Kotulin",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 56.249},
    radio_channels=[],
)
LigotaToszecka = Station(
    name="Ligota Toszecka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 53.837},
    radio_channels=[],
)
Toszek = Station(
    name="Toszek",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 49.92},
    radio_channels=[],
)
Paczyna = Station(
    name="Paczyna",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 44.767},
    radio_channels=[],
)

_LK133 = base.Bookmark()
DabrowaGorniczaZabkowiceGTB = Station(
    name="Dąbrowa Górnicza Ząbkowice GTB",
    short_name="Dąbr. G. Ząbk. GTB",
    lat=50.3665,
    lon=19.2646,
    mileage={133: 1.0},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.FREIGHT_GROUP],
)
DabrowaGorniczaHutaKatowice = Station(
    name="Dąbrowa Górnicza Huta Katowice",
    short_name="Dąbr. G. Huta Katowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 3.677, 162: 3.237},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.JUNCTION],
)
DabrowaGorniczaHutaKatowiceR7 = Station(
    name="Dąbrowa Górnicza Huta Katowice R7",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 3.564, 162: 3.350},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=DabrowaGorniczaHutaKatowice,
    skippable=True,
)
DabrowaGorniczaPoludniowa = Station(
    name="Dąbrowa Górnicza Południowa",
    short_name="Dąbr. G. Południowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 7.537},
    radio_channels=[enums.RadioChannel.R3],
)
JaworznoSzczakowa = Station(
    name="Jaworzno Szczakowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 15.81, 134: 0},
    radio_channels=[],
)
SosnowiecMaczki = Station(
    name="Sosnowiec Maczki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={
        133: 13.276,
        163: 4.528,
        668: 0,
    },  # @TODO: This is a mistake in SimRail data, should be 667
    radio_channels=[],
    is_boundary=True,
)
Pieczyska = Station(
    name="Pieczyska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 18.949},
    radio_channels=[],
)
JaworznoCiezkowice = Station(
    name="Jaworzno Ciężkowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 20.877},
    radio_channels=[],
)
Balin = Station(
    name="Balin",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 26.091},
    radio_channels=[],
)
TrzebiniaTsa = Station(
    name="Trzebinia TSA",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 30.4},
    radio_channels=[],
)
Trzebinia = Station(
    name="Trzebinia",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 31.716},
    radio_channels=[],
)
Dulowa = Station(
    name="Dulowa",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 36.789},
    radio_channels=[],
)
WolaFilipowska = Station(
    name="Wola Filipowska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 41.112},
    radio_channels=[],
)
Krzeszowice = Station(
    name="Krzeszowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={133: 45.097},
    radio_channels=[],
)

_LK134 = base.Bookmark()
Dlugoszyn = Station(
    name="Długoszyn",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={134: 2.852, 667: 1.864, 668: 1.824},
    radio_channels=[],
    station_types=[enums.StationType.JUNCTION],
)

_LK135 = base.Bookmark()
Pyskowice = Station(
    name="Pyskowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={135: 5.309},
    radio_channels=[],
)
GliwiceKuznica = Station(
    name="Gliwice Kuźnica",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={135: 1.977},
    radio_channels=[],
)

_LK137 = base.Bookmark()
KatowiceTowarowaKTC = Station(
    name="Katowice Tow. KTC",
    lat=50.2576,
    lon=19.0163,
    mileage={
        137: 2.913,
        651: 2.185,  # Bug in Simrail data, real line 713
    },
    radio_channels=[enums.RadioChannel.R5],
    is_boundary=True,
)
KatowiceZaleze = Station(
    name="Katowice Załęże",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={137: 2.528},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
ChorzowBatory = Station(
    name="Chorzów Batory",
    lat=50.278559,
    lon=18.945054,
    mileage={137: 6.166, 164: 0.100},
    radio_channels=[enums.RadioChannel.R5],
)
Swietochlowice = Station(
    name="Świętochłowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={137: 8.413},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
RudaChebzie = Station(
    name="Ruda Chebzie",
    lat=50.303725,
    lon=18.877553,
    mileage={137: 11.740},
    radio_channels=[enums.RadioChannel.R2],
)
RudaSlaska = Station(
    name="Ruda Śląska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={137: 14.068},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Zabrze = Station(
    name="Zabrze",
    lat=50.305349,
    lon=18.787184,
    mileage={137: 18.926},
    radio_channels=[enums.RadioChannel.R2],
)
Gliwice = Station(
    name="Gliwice",
    lat=50.300826,
    lon=18.676232,
    mileage={137: 27.100},
    radio_channels=[enums.RadioChannel.R2],
)
GliwiceLabedy = Station(
    name="Gliwice Łabędy",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={137: 32.985},
    radio_channels=[],
)
Szobiszowice = Station(
    name="Szobiszowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={137: 28.53},
    radio_channels=[],
)

_LK138 = base.Bookmark()
Myslowice = Station(
    name="Mysłowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={138: 22.948},
    radio_channels=[],
)
MyslowiceMwa = Station(
    name="Mysłowice MwA",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={138: 23.55},
    radio_channels=[],
)
MyslowiceMwb = Station(
    name="Mysłowice MwB",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={138: 24.2},
    radio_channels=[],
)
MyslowiceMwbPzsR166 = Station(
    name="Mysłowice MwB pzs R166",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={138: 25.086},
    radio_channels=[],
)
Szabelnia = Station(
    name="Szabelnia",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={138: 26.255},
    radio_channels=[],
    is_boundary=True,
    station_types=[enums.StationType.JUNCTION],
)

_LK139 = base.Bookmark()
Brynow = Station(
    name="Brynów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={139: 3.193},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.JUNCTION],
    is_boundary=True,
)
KatowiceBrynow = Station(
    name="Katowice Brynów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={139: 3.77},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
KatowiceLigota = Station(
    name="Katowice Ligota",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={139: 6.08},
    radio_channels=[],
)
KatowicePiotrowice = Station(
    name="Katowice Piotrowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={139: 7.753},
    radio_channels=[],
)
KatowicePodlesie = Station(
    name="Katowice Podlesie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={139: 11.483},
    radio_channels=[],
)
Makolowiec = Station(
    name="Mąkołowiec",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={139: 14.044, 142: 12.247},
    radio_channels=[],
)

_LK140 = base.Bookmark()
Kamien = Station(
    name="Kamień",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={140: 35.032},
    radio_channels=[enums.RadioChannel.R6],
    station_types=[enums.StationType.JUNCTION],
)
Rybnik = Station(
    name="Rybnik",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={140: 39.702},
    radio_channels=[enums.RadioChannel.R6],
)
RybnikTowarowyPZSRTB11 = Station(
    name="Rybnik Towarowy pzs RTB11",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={140: 42.065},
    radio_channels=[enums.RadioChannel.R6],
    station_types=[enums.StationType.LINES_MERGING],
)
RybnikTowarowy = Station(
    name="Rybnik Towarowy",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={140: 43.383, 158: 0},
    radio_channels=[enums.RadioChannel.R6],
)

_LK141 = base.Bookmark()
RudaWirek = Station(
    name="Ruda Wirek",
    lat=50.2598,
    lon=18.8622,
    mileage={141: 10.386},
    radio_channels=[enums.RadioChannel.R5],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST],
)
RudaBielszowice = Station(
    name="Ruda Bielszowice",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={141: 13.396},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.TECHNICAL_STATION],
)
ZabrzeMakoszowy = Station(
    name="Zabrze Makoszowy",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={141: 17.960, 149: 0.281},
    radio_channels=[enums.RadioChannel.R5],
)

_LK142 = base.Bookmark()
KatowiceKostuchna = Station(
    name="Katowice Kostuchna",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={142: 8.344},
    radio_channels=[],
    is_boundary=True,
)

_LK143 = base.Bookmark()
OlesnicaRataje = Station(
    name="Oleśnica Rataje",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={281: 2.730, 766: 2.641},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.HALT],
)
Lukanow = Station(
    name="Łukanów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={143: 137.017, 766: 0.001},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.JUNCTION],
)
BorowaOlesnicka = Station(
    name="Borowa Oleśnicka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={143: 141.717},
    radio_channels=[enums.RadioChannel.R4],
)
Dlugoleka = Station(
    name="Długołęka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={143: 147.628},
    radio_channels=[enums.RadioChannel.R4],
)
WroclawPsiePole = Station(
    name="Wrocław Psie Pole",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={143: 153.742},
    radio_channels=[enums.RadioChannel.R4],
)
WroclawSoltysowice = Station(
    name="Wrocław Sołtysowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={143: 156.609},
    radio_channels=[enums.RadioChannel.R4],
)
WroclawNadodrze = Station(
    name="Wrocław Nadodrze",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={143: 160.536},
    radio_channels=[enums.RadioChannel.R4],
)

_LK144 = base.Bookmark()
Fosowskie = Station(
    name="Fosowskie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 176.335, 144: 44.474},
    radio_channels=[],
)
Ozimek = Station(
    name="Ozimek",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={144: 55.357},
    radio_channels=[],
)
Chrzastowice = Station(
    name="Chrząstowice",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={144: 65.432},
    radio_channels=[],
)

_LK149 = base.Bookmark()
Mizerow = Station(
    name="Mizerów",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={149: 1.715, 677: 2.137},
    radio_channels=[enums.RadioChannel.R6],
    station_types=[enums.StationType.JUNCTION],
)
Gieraltowice = Station(
    name="Gierałtowice",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={149: 5.822},
    radio_channels=[enums.RadioChannel.R6],
    station_types=[enums.StationType.JUNCTION, enums.StationType.PASSING_LOOP],
)
Knurow = Station(
    name="Knurów",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={149: 11.872},
    radio_channels=[enums.RadioChannel.R6],
)
Szczyglowice = Station(
    name="Szczygłowice",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={149: 18.486},
    radio_channels=[enums.RadioChannel.R6],
    station_types=[enums.StationType.JUNCTION],
)
Leszczyny = Station(
    name="Leszczyny",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={140: 31.776, 149: 22.935},
    radio_channels=[enums.RadioChannel.R6],
)

_LK154 = base.Bookmark()
LazyGrupaWeglarkowaLgw = Station(
    name="Łazy Grupa Węglarkowa ŁGW",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={154: -2.571, 160: 278.507},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.FREIGHT_GROUP],
    skippable=True,
)
LazyL11 = Station(
    name="Łazy Ł11",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={154: -1.177},
    radio_channels=[enums.RadioChannel.R2],
    skippable=True,
)
DabrowaGorniczaZabkowiceDzaR4_7 = Station(
    name="Dąbrowa Górn. Ząbkowice DZA R.4/7",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 290.544, 133: -1.224, 160: 291.663},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=DabrowaGorniczaZabkowiceDZA,
    skippable=True,
)
Przemiarki = Station(
    name="Przemiarki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={154: 7.717},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.JUNCTION],
)
DabrowaGorniczaTowarowaDtaR5 = Station(
    name="Dąbrowa Górnicza Towarowa DTA R5",
    short_name="Dąbr. G. Tow. DTA R5",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={154: 15.192, 661: 0},
    radio_channels=[enums.RadioChannel.R4],
)
DabrowaGorniczaTowarowa = Station(
    name="Dąbrowa Górnicza Towarowa",
    short_name="Dąbr. G. Tow.",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={154: 20.297, 171: 0},
    radio_channels=[],
    is_boundary=True,
)

_LK155 = base.Bookmark()
CzestochowaMirow = Station(
    name="Częstochowa Mirów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={155: 2.057},
    radio_channels=[],
)

_LK158 = base.Bookmark()
RadlinObszary = Station(
    name="Radlin Obszary",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={158: 3.860},
    radio_channels=[enums.RadioChannel.R6],
    station_types=[enums.StationType.JUNCTION],
)
WodzislawSlaski = Station(
    name="Wodzisław Śląski",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={158: 7.828},
    radio_channels=[enums.RadioChannel.R6],
)
Olza = Station(
    name="Olza",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={158: 20.514},
    radio_channels=[enums.RadioChannel.R6],
)
OlzaOLB = Station(
    name="Olza Olb",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={151: 50.790, 158: 23.839},
    radio_channels=[enums.RadioChannel.R6],
)
Chalupki = Station(
    name="Chałupki",
    lat=50.2598,  # @TODO: placeholder
    lon=18.8622,  # @TODO: placeholder
    mileage={151: 52.568, 158: 25.035, 479: 279.628, 592: 4.297},
    radio_channels=[enums.RadioChannel.R6],
)

_LK160 = base.Bookmark()
LazyR52 = Station(
    name="Łazy R52",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={160: 277.507},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=Lazy,
    skippable=True,
)

_LK162 = base.Bookmark()
DabrowaGorniczaStrzemieszyceR75 = Station(
    name="Dąbr.Gór.Strzem. R75",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={62: 69.643, 162: 0.422},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=DabrowaGorniczaStrzemieszyce,
    skippable=True,
)

_LK163 = base.Bookmark()
SosnowiecKazimierzPzsSkz1 = Station(
    name="Sosnowiec Kazimierz PZS SKZ1",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={163: 0.616},
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=SosnowiecKazimierz,
    radio_recording=False,
    radio_channels=[],
    skippable=True,
)

_LK164 = base.Bookmark()
RudaKochlowice = Station(
    name="Ruda Kochłowice",
    lat=50.2566445,
    lon=18.908329,
    mileage={141: 6.643, 164: 4.675},
    radio_channels=[enums.RadioChannel.R5],
)

_LK171 = base.Bookmark()
DabrowaGorniczaTowarowaDta = Station(
    name="Dąbrowa Górnicza Towarowa DTA",
    short_name="Dąbr. G. Tow. DTA",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={154: 17.250, 171: 3.907},
    radio_channels=[],
)
Koziol = Station(
    name="Kozioł",
    lat=50.3078,
    lon=19.3796,
    mileage={171: 6.833, 661: 2.966},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.JUNCTION],
)
KoziolR12 = Station(
    name="Kozioł R12",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={171: 6.873, 661: 2.966},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=Koziol,
    skippable=True,
)
Dorota = Station(
    name="Dorota",
    lat=50.2815,
    lon=19.2792,
    mileage={133: 10.7, 171: 16.224},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.JUNCTION],
)
Juliusz = Station(
    name="Juliusz",
    lat=50.272186,
    lon=19.225194,
    mileage={171: 20.746},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)
Stawiska = Station(
    name="Stawiska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={171: 30.097, 657: 1.996},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)
KatowiceJanowOdst = Station(
    name="Katowice Janów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={171: 32.496},
    radio_channels=[enums.RadioChannel.R5],
    radio_recording=False,
    station_types=[enums.StationType.BLOCK_POST],
)
KatowiceMuchKmb = Station(
    name="Katowice Much. KMB",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={171: 37.74, 652: 0.107},
    radio_channels=[enums.RadioChannel.R5],
)

_LK179 = base.Bookmark()
Tychy = Station(
    name="Tychy",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={142: 15.172, 179: 16.97},
    radio_channels=[],
    r307=True,
)
TychyZachodnie = Station(
    name="Tychy Zachodnie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={179: 2.348},
    radio_channels=[],
)
TychyAlejaBielska = Station(
    name="Tychy Aleja Bielska",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={179: 2.853},
    radio_channels=[],
)
TychyGrotaRoweckiego = Station(
    name="Tychy Grota Roweckiego",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={179: 3.282},
    radio_channels=[],
)

_LK186 = base.Bookmark()
ZawiercieGt = Station(
    name="Zawiercie GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={4: 224.676, 186: 274.856},
    radio_channels=[],
)

_LK271 = base.Bookmark()
WroclawPopowiceWp3Pzs = Station(
    name="Wrocław Popowice Wp3 PZS",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={143: 163.640, 271: 162.607, 755: 0.622},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.LINES_MERGING],
)
WroclawMikolajow = Station(
    name="Wrocław Mikołajów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={143: 163.504, 271: 3.945},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.HALT],
)
WroclawPopowiceWp2 = Station(
    name="Wrocław Popowice Wp2",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={271: 3.298},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.JUNCTION],
)
Grabiszyn = Station(
    name="Grabiszyn",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={271: 2.048},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.JUNCTION],
)
WroclawGlowny = Station(
    name="Wrocław Główny",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={132: 181.041, 271: 0, 276: 0},
    radio_channels=[enums.RadioChannel.R4],
)

_LK281 = base.Bookmark()
Krotoszyn = Station(
    name="Krotoszyn",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={281: 63.959, 815: 2.324},
    radio_channels=[enums.RadioChannel.R4],
)
Zduny = Station(
    name="Zduny",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={281: 56.606},
    radio_channels=[enums.RadioChannel.R4],
)
Milicz = Station(
    name="Milicz",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={281: 41.887},
    radio_channels=[enums.RadioChannel.R4],
)
GrabownoWielkie = Station(
    name="Grabowno Wielkie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={281: 17.644, 355: 17.644},
    radio_channels=[enums.RadioChannel.R4],
)
Dobroszyce = Station(
    name="Dobroszyce",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={281: 8.841},
    radio_channels=[enums.RadioChannel.R4],
)

_LK301 = base.Bookmark()
Bolko = Station(
    name="Bolko",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={144: 73.769, 301: 2.203},
    radio_channels=[],
)

_LK355 = base.Bookmark()
Twardogora = Station(
    name="Twardogóra",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={355: 47.682},
    radio_channels=[enums.RadioChannel.R3],
)
SosnieOstrowskie = Station(
    name="Sośnie Ostrowskie",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={355: 25.037},
    radio_channels=[enums.RadioChannel.R3],
)
Granowiec = Station(
    name="Granowiec",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={355: 20.484},
    radio_channels=[enums.RadioChannel.R3],
)
Odolanow = Station(
    name="Odolanów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={355: 13.122},
    radio_channels=[enums.RadioChannel.R3],
)
TopolaOsiedle = Station(
    name="Topola-Osiedle",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={355: 5.282},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.HALT, enums.StationType.PASSING_LOOP],
)

_LK447 = base.Bookmark()
WarszawaUrsus = Station(
    name="Warszawa Ursus",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={447: 9.165},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
WarszawaUrsusNiedzwiadek = Station(
    name="Warszawa Ursus Niedźwiadek",
    short_name="Wwa Ursus Niedź.",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={447: 10.345},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Piastow = Station(
    name="Piastów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={447: 12.457},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Parzniew = Station(
    name="Parzniew",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={447: 18.631},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Brwinow = Station(
    name="Brwinów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={447: 22.057},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
Milanowek = Station(
    name="Milanówek",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={447: 26.005},
    radio_channels=[],
    station_types=[enums.StationType.HALT],
)
GrodziskMazowieckiR64 = Station(
    name="Grodzisk Mazowiecki R64",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={1: 31.196, 447: 31.196},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=GrodziskMazowiecki,
    skippable=True,
)

_LK479 = base.Bookmark()
Bohumin = Station(
    name="Bohumin",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={479: 276.492},
    radio_channels=[enums.RadioChannel.R3],
)

_LK507 = base.Bookmark()
WarszawaGolabki = Station(
    name="Warszawa Gołąbki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={507: 2.351},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.JUNCTION, enums.StationType.HALT],
)

_LK509 = base.Bookmark()
WarszawaJelonki = Station(
    name="Warszawa Jelonki",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={509: 3.5},
    radio_channels=[],
)
WarszawaGdanskaGt = Station(
    name="Warszawa Gdańska GT",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={509: 8.7},
    radio_channels=[],
)
WarszawaGdanskaWg = Station(
    name="Warszawa Gdańska WG",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={509: 9.172},
    radio_channels=[],
)

_LK570 = base.Bookmark()
PsaryR40 = Station(
    name="Psary Roz.40",
    lat=50.7336,
    lon=19.8163,
    mileage={4: 170.861, 570: 0.252},
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    radio_channels=[],
    radio_recording=False,
    belongs_to=Psary,
    skippable=True,
)
StarzynyR5 = Station(
    name="Starzyny R5",
    lat=50.715,
    lon=19.8002,
    mileage={64: 32.499, 570: 3.005},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    radio_recording=False,
    belongs_to=Starzyny,
    skippable=True,
)

_LK572 = base.Bookmark()
ZelislawiceR6 = Station(
    name="Żelisławice R.6",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={61: 59.037, 572: 7.73},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=Zelislawice,
    skippable=True,
)

_LK573 = base.Bookmark()
IdzikowiceRoz18 = Station(
    name="Idzikowice Roz.18",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={4: 79.981, 573: 0.132},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=Idzikowice,
    skippable=True,
)

_LK574 = base.Bookmark()
IdzikowiceRoz12 = Station(
    name="Idzikowice Roz.12",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={4: 79.919, 574: 4.220},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=Idzikowice,
    skippable=True,
)

_LK575 = base.Bookmark()
Markow = Station(
    name="Marków",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={575: 2.974},
    radio_channels=[enums.RadioChannel.R1],
    station_types=[enums.StationType.JUNCTION],
)

_LK592 = base.Bookmark()
BohuminVrbice = Station(
    name="Bohumin Vrbice",
    lat=49.882,
    lon=18.3231,
    mileage={592: 0},
    radio_channels=[enums.RadioChannel.R6],
)

_LK651 = base.Bookmark()
Hajduki = Station(
    name="Hajduki",
    lat=50.262818,
    lon=18.941401,
    mileage={164: 2.820, 651: 1.443},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)

_LK652 = base.Bookmark()
KatowiceMRoz233 = Station(
    name="Katowice M. Roz. 233",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={652: 0.0, 657: 9.564},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=KatowiceMuchKmb,
    skippable=True,
)
KatowiceMKmbR234 = Station(
    name="Katowice M. Kmb R234",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={652: 0.072},
    radio_channels=[],
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    belongs_to=KatowiceMuchKmb,
    skippable=True,
)

_LK657 = base.Bookmark()
KatowiceJanowPodg = Station(
    name="Katowice Janów",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={657: 4.447},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)

_LK696 = base.Bookmark()
TychyMiasto = Station(
    name="Tychy Miasto",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={696: 3.73},
    radio_channels=[],
)
TychyLodowisko = Station(
    name="Tychy Lodowisko",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={696: 0.336},
    radio_channels=[],
)

_LK713 = base.Bookmark()
Gottwald = Station(
    name="Gottwald",
    lat=50.271973,
    lon=18.9617372,
    mileage={651: 3.289, 713: 3.989},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.JUNCTION],
)

_LK766 = base.Bookmark()
DabrowaOlesnicka = Station(
    name="Dąbrowa Oleśnicka",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={281: 4.397, 766: 4.397},
    radio_channels=[enums.RadioChannel.R4],
    station_types=[enums.StationType.HALT, enums.StationType.JUNCTION],
)

_LK815 = base.Bookmark()
Durzyn = Station(
    name="Durzyn",
    lat=0,  # @TODO: placeholder
    lon=0,  # @TODO: placeholder
    mileage={14: 162.443, 815: 162.443},
    radio_channels=[enums.RadioChannel.R5],
    station_types=[enums.StationType.TECHNICAL_STATION],
    r307=True,
)

_LK839 = base.Bookmark()
WarszawaGrochow = Station(
    name="Warszawa Grochów",
    lat=52.256232,
    lon=21.082431,
    mileage={45: 7.500, 839: 3.333},
    radio_channels=[enums.RadioChannel.R2],
    station_types=[enums.StationType.TECHNICAL_STATION],
    is_boundary=True,
)
WarszawaGrochowR5 = Station(
    name="Warszawa Grochów R5",
    lat=52.256232,
    lon=21.082431,
    mileage={45: 2.297, 839: 2.297},
    station_types=[enums.StationType.BRANCH_OFF_POINT],
    radio_channels=[],
    radio_recording=False,
    belongs_to=WarszawaGrochow,
    skippable=True,
)

_LK898 = base.Bookmark()
KWKStaszic = Station(
    name="KATOWICE MUCHOWIEC STASZIC",
    short_name="Kat. Much. Staszic",
    lat=50.227,
    lon=19.0474,
    mileage={898: 3.700},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.TECHNICAL_STATION],
    is_boundary=True,
    r307=True,
)
Staszic = Station(
    name="Staszic",
    lat=50.218679,
    lon=19.0013,
    mileage={142: 2.901, 652: 1.450, 898: 0.072},
    radio_channels=[enums.RadioChannel.R3],
    station_types=[enums.StationType.JUNCTION],
)


R307_ISSUERS = {
    Czestochowa: [
        [40101, 40149, Katowice],
        [40601, 40649, Katowice],
    ],
    CzestochowaStradom: [
        [73101, 73199, JaworznoSzczakowa],
        [6100, 6148, WarszawaWschodnia],
        [61100, 61148, WarszawaWschodnia],
    ],
    CzestochowaTowarowa: [
        [421000, 421098, Jedrzejow],
        [441001, 441099, Tychy],
        [442001, 442099, SosnowiecMaczki],
        [447001, 447099, Tychy],
    ],
    DabrowaGorniczaTowarowa: [
        [414000, 414098, Czestochowa],
        [443901, 443999, CzestochowaMirow],
    ],
    Drzewica: [
        [243331, 243399, Koniecpol],
    ],
    Gliwice: [
        [644000, 644098, RudnikiKoloCzestochowy],
    ],
    JaworznoSzczakowa: [
        [37100, 37198, CzestochowaStradom],
        [44301, 44399, Katowice],
        [412000, 412048, Kozlow],
        [413000, 413098, Kielce],
        [445000, 445098, CzestochowaTowarowa],
    ],
    Jedrzejow: [
        [245021, 245099, CzestochowaTowarowa],
    ],
    Katowice: [
        [4100, 4148, WarszawaWschodnia],
        [40150, 40198, Czestochowa],
        [40650, 40698, Czestochowa],
        [41100, 41148, WarszawaWschodnia],
        [42100, 42148, Kielce],
        [42150, 42198, Kielce],
        [42900, 42998, Kielce],
        [43300, 43398, KrakowGlowny],
        [45250, 45298, Koluszki],
        [412050, 412098, Czestochowa],
        [629000, 629048, Wloszczowa],
        [649050, 649098, Myszkow],
    ],
    Kielce: [
        [24101, 24149, Katowice],
        [24151, 24199, Katowice],
        [24901, 24999, Katowice],
        [144251, 144299, Tychy],
        [243501, 243599, Myslowice],
    ],
    Koluszki: [
        [9100, 9148, WarszawaWschodnia],
        [113050, 113098, WarszawaGlTowWoa],
        [414000, 414098, WarszawaGlTowWoa],
    ],
    Koniecpol: [
        [423400, 423498, DebaOpoczynska],
    ],
    Kozlow: [
        [412000, 412048, Koluszki],
    ],
    KrakowGlowny: [
        [3100, 3148, WarszawaWschodnia],
        [31100, 31148, WarszawaWschodnia],
    ],
    KWKStaszic: [
        [424000, 424098, Jedrzejow],
        [444000, 444098, Czestochowa],
        [464000, 464098, CzestochowaTowarowa],
    ],
    Ludynia: [
        [244001, 244099, SosnowiecMaczki],
    ],
    Skierniewice: [
        [91300, 91398, WarszawaWschodnia],
        [91900, 91998, WarszawaWschodnia],
    ],
    WarszawaGdanska: [
        [146001, 146049, Katowice],
    ],
    WarszawaGdanskaWg: [
        [142001, 142099, Koluszki],
    ],
    WarszawaGlTowWoa: [
        [132001, 132049, KrakowNowaHutaNhaGttr],
        [145051, 145099, Koluszki],
        [146051, 146099, Katowice],
    ],
    WarszawaWschodnia: [
        [1301, 1349, KrakowGlowny],
        [1401, 1449, Katowice],
        [1601, 1649, CzestochowaStradom],
        [1901, 1949, Koluszki],
        [13101, 13149, KrakowGlowny],
        [13251, 13299, KrakowGlowny],
        [14101, 14149, Katowice],
        [16101, 16149, CzestochowaStradom],
        [19301, 19399, Skierniewice],
        [19901, 19999, Skierniewice],
    ],
    Wloszczowa: [
        [242201, 242249, ChorzowBatory],
    ],
    Zelislawice: [
        [223000, 223048, Drzewica],
    ],
}
