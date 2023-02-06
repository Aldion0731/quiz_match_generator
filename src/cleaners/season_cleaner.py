from abc import ABC, abstractmethod

import pandas as pd

from .areas_cleaner import AreasCleaner
from .data_formatter import (
    DataFormatterSeventeen,
    DataFormatterThirteen,
    DataFormatterTwenty,
    DefaultFormatter,
)


class SeasonCleaner(ABC):
    @abstractmethod
    def get_clean_section(self, season_section: pd.DataFrame) -> pd.DataFrame:
        pass


class SeasonCleanerDefault(
    SeasonCleaner
):  # TODO: refactor so takes a formatter as an argument
    def __init__(self, areas_cleaner: AreasCleaner) -> None:
        self.areas_cleaner = areas_cleaner

    def get_clean_section(self, season_section: pd.DataFrame) -> pd.DataFrame:
        season_section = season_section.copy()
        formatter = DefaultFormatter(season_section)
        formatted_data = formatter.format_data()
        formatted_data["Area"] = self.get_clean_area_col(formatted_data["Area"])
        formatted_data = formatted_data[["Match", "Round", "Questions", "Area"]]
        return formatted_data

    def get_clean_area_col(self, area_col: pd.Series) -> pd.Series:
        return area_col.apply(self.areas_cleaner.clean)


class SeasonCleanerThirteen(SeasonCleanerDefault):
    def get_clean_section(self, season_section: pd.DataFrame) -> pd.DataFrame:
        formatter = DataFormatterThirteen(season_section)
        formatted_data = formatter.format_data()
        return super().get_clean_section(formatted_data)


class SeasonCleanerSeventeen(SeasonCleanerDefault):
    def get_clean_section(self, season_section: pd.DataFrame) -> pd.DataFrame:
        formatter = DataFormatterSeventeen(season_section)
        formatted_data = formatter.format_data()
        return super().get_clean_section(formatted_data)


class SeasonCleanerTwenty(SeasonCleanerDefault):
    def get_clean_section(self, season_section: pd.DataFrame) -> pd.DataFrame:
        formatter = DataFormatterTwenty(season_section)
        formatted_data = formatter.format_data()
        return super().get_clean_section(formatted_data)


class SeasonCleanerTwentyOne(SeasonCleanerTwenty):
    pass
