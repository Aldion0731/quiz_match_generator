from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from .text_cleaner import TextCleaner


class SeasonCleaner(ABC):
    @abstractmethod
    def get_clean_section(self, season_section: pd.DataFrame) -> pd.DataFrame:
        pass


class SeasonCleanerDefault(SeasonCleaner):
    def __init__(self, cleaner: TextCleaner) -> None:
        self.cleaner = cleaner

    def get_clean_section(self, season_section: pd.DataFrame) -> pd.DataFrame:
        season_section = season_section.copy()
        season_section = season_section.dropna()
        season_section.columns = self.get_clean_col_names(season_section)
        season_section["Area"] = self.get_clean_area_col(season_section["Area"])
        return season_section

    def get_clean_col_names(self, df: pd.DataFrame) -> List[str]:
        return [col.strip(" ") for col in df.columns]

    def get_clean_area_col(self, area_col: pd.Series) -> pd.Series:
        return area_col.apply(self.cleaner.clean)
