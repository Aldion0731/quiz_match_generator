from typing import List

from .season_cleaner import SeasonCleaner, SeasonCleanerDefault, SeasonCleanerThirteen
from .text_cleaner import TextCleaner, TextCleanerDefault, TextCleanerThirteen

TEXT_CLEANER_FACTORIES = {
    "2013": TextCleanerThirteen(),
    "2014": TextCleanerDefault(),
    "2016": TextCleanerDefault(),
}
SEASON_CLEANER_FACTORIES = {
    "2013": SeasonCleanerThirteen,
    "2014": SeasonCleanerDefault,
    "2016": SeasonCleanerDefault,
}


class TextCleanerFactory:
    def create_from(self, section_keys: List[str]) -> TextCleaner:
        key = generate_key(section_keys)
        return self.create(key)

    def create(self, key: str) -> TextCleaner:
        return TEXT_CLEANER_FACTORIES[key]

    @staticmethod
    def show_keys() -> List[str]:
        return list(TEXT_CLEANER_FACTORIES.keys())


class SeasonCleanerFactory:
    def create_from(self, section_keys: List[str]) -> SeasonCleaner:
        key = generate_key(section_keys)
        return self.create(key)

    def create(self, key: str) -> SeasonCleaner:
        text_cleaner = TextCleanerFactory().create(key)
        return SEASON_CLEANER_FACTORIES[key](text_cleaner)

    @staticmethod
    def show_keys() -> List[str]:
        return list(SEASON_CLEANER_FACTORIES.keys())


def generate_key(section_keys: List[str]) -> str:
    return section_keys[0].split(" ")[0]
