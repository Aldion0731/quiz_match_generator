from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .cleaner import DfCleaner


@dataclass
class QuizSeason:
    alternate: pd.DataFrame = pd.DataFrame()
    minutes: pd.DataFrame = pd.DataFrame()
    buzzer: pd.DataFrame = pd.DataFrame()

    def from_read_excel(self, read_excel: Dict) -> QuizSeason:
        section_keys: List[str] = list(read_excel.keys())
        return QuizSeason(
            alternate=read_excel[section_keys[0]],
            minutes=read_excel[section_keys[1]],
            buzzer=read_excel[section_keys[2]],
        )

    def with_clean_data(self, df_cleaner: DfCleaner) -> QuizSeason:
        return QuizSeason(
            alternate=df_cleaner.get_clean_df(self.alternate),
            minutes=df_cleaner.get_clean_df(self.minutes),
            buzzer=df_cleaner.get_clean_df(self.buzzer),
        )


class ExcelSeasons:
    def load_from_files(self, data_dir: Path) -> List[Dict]:
        season_files = self.__get_season_files(data_dir)
        return self.__load_excel_seasons(season_files)

    def __load_excel_seasons(self, season_files: List[Path]) -> List[Dict]:
        excel_seasons: List[Dict] = []
        for file in season_files:
            try:
                excel_season = pd.read_excel(file, sheet_name=None, header=0)
                excel_seasons.append(excel_season)
            except Exception:
                continue
        return excel_seasons

    def __get_season_files(self, data_dir: Path) -> List[Path]:
        return [data_dir / file for file in os.listdir(data_dir)]
