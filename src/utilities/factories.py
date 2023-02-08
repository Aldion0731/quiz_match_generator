from typing import List

import pandas as pd

from ..cleaners.areas_cleaner import (
    AreasCleaner,
    AreasCleanerDefault,
    AreasCleanerThirteen,
    AreasCleanerTwenty,
    AreasCleanerTwentyOne,
)
from ..cleaners.data_formatter import (
    DataFormatter,
    DataFormatterSeventeen,
    DataFormatterThirteen,
    DataFormatterTwenty,
    DataFormatterTwentyOne,
    DefaultFormatter,
)

AREAS_CLEANER_FACTORIES = {
    "2013": AreasCleanerThirteen(),
    "2014": AreasCleanerDefault(),
    "2016": AreasCleanerDefault(),
    "2017": AreasCleanerDefault(),
    "2020": AreasCleanerTwenty(),
    "2021": AreasCleanerTwentyOne(),
}
FORMATTER_FACTORIES = {
    "2013": DataFormatterThirteen,
    "2014": DefaultFormatter,
    "2016": DefaultFormatter,
    "2017": DataFormatterSeventeen,
    "2020": DataFormatterTwenty,
    "2021": DataFormatterTwentyOne,
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


class FormatterFactory:
    def create_from(self, section_keys: List[str], df: pd.DataFrame) -> DataFormatter:
        key = generate_key(section_keys)
        return self.create(key, df)

    def create(self, key: str, df: pd.DataFrame) -> DataFormatter:
        return FORMATTER_FACTORIES[key](df)

    @staticmethod
    def show_keys() -> List[str]:
        return list(FORMATTER_FACTORIES.keys())


def generate_key(section_keys: List[str]) -> str:
    return section_keys[0].split(" ")[0]
