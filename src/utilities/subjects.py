from __future__ import annotations

import json
from enum import Enum
from functools import cached_property
from typing import Dict


class MapNames(Enum):
    DEFAULT = "DEFAULT_MAP"
    THIRTEEN = "THIRTEEN_MAP"


class Subjects(Enum):
    ART = "Art"
    BK = "BK"
    BIO = "Bio"
    CA = "CA"
    CHEM = "Chem"
    ENG = "Eng"
    FRE = "French"
    GEO = "Geo"
    GK = "GK"
    HIS = "His"
    IT = "IT"
    JH = "JH"
    LIT = "Lit"
    MAT = "Math"
    MUS = "Music"
    PHY = "Phys"
    SPA = "Span"
    SPO = "Sports"
    THE = "The"

    @staticmethod
    def from_df_val(df_val: str, map_name: MapNames) -> Subjects:
        map_getter = MapGetter()
        season_subject_map = map_getter.mappers[map_name.value]
        return Subjects(season_subject_map[df_val])


class MapGetter:
    def __init__(self):
        self.map_src = "subject_mappers.json"

    @cached_property
    def mappers(self) -> Dict[str, Dict[str, str]]:
        with open(self.map_src) as subject_mapper:
            return json.load(subject_mapper)
