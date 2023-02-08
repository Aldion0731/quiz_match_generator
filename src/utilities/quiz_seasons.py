from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from typing import Dict, List

import pandas as pd

from ..cleaners.section_cleaner import get_clean_section
from ..utilities.factories import AreasCleanerFactory, FormatterFactory


@dataclass
class QuizSeason:
    alternate: pd.DataFrame = pd.DataFrame()
    minutes: pd.DataFrame = pd.DataFrame()
    buzzer: pd.DataFrame = pd.DataFrame()
    section_keys: List[str] = field(default_factory=lambda: [""])

    def from_read_excel(self, read_excel: Dict) -> QuizSeason:
        section_keys = list(read_excel.keys())
        return QuizSeason(
            alternate=read_excel[section_keys[0]],
            minutes=read_excel[section_keys[1]],
            buzzer=read_excel[section_keys[2]],
            section_keys=section_keys,
        )

    def with_clean_data(
        self, cleaner_factory: AreasCleanerFactory, formatter_factory: FormatterFactory
    ) -> QuizSeason:
        season = self.with_formatted_data(formatter_factory)
        cleaner = cleaner_factory.create_from(self.section_keys)
        return QuizSeason(
            alternate=get_clean_section(season.alternate, cleaner),
            minutes=get_clean_section(season.minutes, cleaner),
            buzzer=get_clean_section(season.buzzer, cleaner),
            section_keys=season.section_keys,
        )

    def with_formatted_data(self, factory: FormatterFactory) -> QuizSeason:
        formatter = partial(factory.create_from, section_keys=self.section_keys)
        alt_formatter = formatter(df=self.alternate)
        min_formatter = formatter(df=self.minutes)
        buzzer_formatter = formatter(df=self.buzzer)
        return QuizSeason(
            alternate=alt_formatter.format_data(),
            minutes=min_formatter.format_data(),
            buzzer=buzzer_formatter.format_data(),
            section_keys=self.section_keys,
        )

    def compare_formatted_data(self, factory: FormatterFactory) -> Dict[str, int]:
        formatted_season = self.with_formatted_data(factory)
        dropped_alternate = len(self.alternate) - len(formatted_season.alternate)
        dropped_minutes = len(self.minutes) - len(formatted_season.minutes)
        dropped_buzzer = len(self.buzzer) - len(formatted_season.buzzer)
        return {
            "alternate": dropped_alternate,
            "minutes": dropped_minutes,
            "buzzer": dropped_buzzer,
        }

    def convert_to_parquet(self, dest: Path) -> None:
        self.alternate.to_parquet(dest / f"{self.section_keys[0]}.parquet")
        self.minutes.to_parquet(dest / f"{self.section_keys[1]}.parquet")
        self.buzzer.to_parquet(dest / f"{self.section_keys[2]}.parquet")

    def from_clean_parquet_store(self, parquet_store: Path) -> QuizSeason:
        section_files = [parquet_store / file for file in os.listdir(parquet_store)]
        return QuizSeason(
            alternate=pd.read_parquet(section_files[0]),
            minutes=pd.read_parquet(section_files[1]),
            buzzer=pd.read_parquet(section_files[2]),
            section_keys=self.section_keys,
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
