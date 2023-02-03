from typing import List

from ..cleaners.areas_cleaner import (
    AreasCleaner,
    AreasCleanerDefault,
    AreasCleanerThirteen,
)
from ..cleaners.season_cleaner import (
    SeasonCleaner,
    SeasonCleanerDefault,
    SeasonCleanerThirteen,
)

AREAS_CLEANER_FACTORIES = {
    "2013": AreasCleanerThirteen(),
    "2014": AreasCleanerDefault(),
    "2016": AreasCleanerDefault(),
}
SEASON_CLEANER_FACTORIES = {
    "2013": SeasonCleanerThirteen,
    "2014": SeasonCleanerDefault,
    "2016": SeasonCleanerDefault,
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
        text_cleaner = AreasCleanerFactory().create(key)
        return SEASON_CLEANER_FACTORIES[key](text_cleaner)

    @staticmethod
    def show_keys() -> List[str]:
        return list(SEASON_CLEANER_FACTORIES.keys())


def generate_key(section_keys: List[str]) -> str:
    return section_keys[0].split(" ")[0]
