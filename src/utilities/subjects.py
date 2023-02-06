from __future__ import annotations

import json
from enum import Enum
from functools import cached_property
from typing import Dict


class MapNames(Enum):
    DEFAULT = "DEFAULT_MAP"
    THIRTEEN = "THIRTEEN_MAP"
    SEVENTEEN = "SEVENTEEN_MAP"
    TWENTY = "TWENTY_MAP"
    TWENTY_ONE = "TWENTY_ONE_MAP"


class Subjects(Enum):
    BK = "BK"
    BIO = "Bio"
    ENG = "Eng"
    CA = "CA"
    CHEM = "Chem"
    MUS = "Music"
    GK = "GK"
    SPA = "Span"
    GEO = "Geo"
    THE = "The"
    IT = "IT"
    HIS = "His"
    MAT = "Math"
    PHY = "Phys"
    ART = "Art"
    JH = "JH"
    FRE = "French"
    LIT = "Lit"
    SPO = "Sports"

    @staticmethod
    def from_df_val(df_val: str, map_name: MapNames) -> Subjects:
        map_getter = MapGetter()
        season_subject_map = map_getter.mappers[map_name.value]
        return Subjects(season_subject_map[df_val])


class MapGetter:
    def __init__(self) -> None:
        self.map_src = "subject_mappers.json"

    @cached_property
    def mappers(self) -> Dict[str, Dict[str, str]]:
        with open(self.map_src) as subject_mapper:
            return json.load(subject_mapper)
