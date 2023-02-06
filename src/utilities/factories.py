from typing import List

from ..cleaners.areas_cleaner import (
    AreasCleaner,
    AreasCleanerDefault,
    AreasCleanerSeventeen,
    AreasCleanerThirteen,
    AreasCleanerTwenty,
    AreasCleanerTwentyOne,
)
from ..cleaners.season_cleaner import (
    SeasonCleaner,
    SeasonCleanerDefault,
    SeasonCleanerSeventeen,
    SeasonCleanerThirteen,
    SeasonCleanerTwenty,
    SeasonCleanerTwentyOne,
)

AREAS_CLEANER_FACTORIES = {
    "2013": AreasCleanerThirteen(),
    "2014": AreasCleanerDefault(),
    "2016": AreasCleanerDefault(),
    "2017": AreasCleanerSeventeen(),
    "2020": AreasCleanerTwenty(),
    "2021": AreasCleanerTwentyOne(),
}
SEASON_CLEANER_FACTORIES = {
    "2013": SeasonCleanerThirteen,
    "2014": SeasonCleanerDefault,
    "2016": SeasonCleanerDefault,
    "2017": SeasonCleanerSeventeen,
    "2020": SeasonCleanerTwenty,
    "2021": SeasonCleanerTwentyOne,
}


class AreasCleanerFactory:
    def create_from(self, section_keys: List[str]) -> AreasCleaner:
        key = generate_key(section_keys)
        return self.create(key)

    def create(self, key: str) -> AreasCleaner:
        return AREAS_CLEANER_FACTORIES[key]

    @staticmethod
    def show_keys() -> List[str]:
        return list(AREAS_CLEANER_FACTORIES.keys())


class SeasonCleanerFactory:
    def create_from(self, section_keys: List[str]) -> SeasonCleaner:
        key = generate_key(section_keys)
        return self.create(key)

    def create(self, key: str) -> SeasonCleaner:
        area_cleaner = AreasCleanerFactory().create(key)
        return SEASON_CLEANER_FACTORIES[key](area_cleaner)

    @staticmethod
    def show_keys() -> List[str]:
        return list(SEASON_CLEANER_FACTORIES.keys())


def generate_key(section_keys: List[str]) -> str:
    return section_keys[0].split(" ")[0]
