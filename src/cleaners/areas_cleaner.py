from abc import ABC, abstractmethod

import pandas as pd

from ..utilities.subjects import MapNames, Subjects


class AreasCleaner(ABC):
    def clean_col(self, area_col: pd.Series) -> pd.Series:
        return area_col.apply(self.clean)

    def clean(self, text: str) -> str:
        text = text.rstrip(" ")
        text = text.rstrip(".")
        return self.rename_area(text)

    @abstractmethod
    def rename_area(self, text: str) -> str:
        pass


class AreasCleanerDefault(AreasCleaner):
    def rename_area(self, text: str) -> str:
        return Subjects.from_df_val(text, MapNames.DEFAULT).value


class AreasCleanerThirteen(AreasCleanerDefault):
    def rename_area(self, text: str) -> str:
        try:
            return super().rename_area(text)
        except Exception:
            return Subjects.from_df_val(text, MapNames.THIRTEEN).value


class AreasCleanerTwenty(AreasCleanerDefault):
    def rename_area(self, text: str) -> str:
        try:
            return super().rename_area(text)
        except Exception:
            return Subjects.from_df_val(text, MapNames.TWENTY).value


class AreasCleanerTwentyOne(AreasCleanerDefault):
    def rename_area(self, text: str) -> str:
        try:
            return super().rename_area(text)
        except Exception:
            return Subjects.from_df_val(text, MapNames.TWENTY_ONE).value
