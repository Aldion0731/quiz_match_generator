from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy

from .quiz_seasons import QuizSeason
from .subjects import Subjects


@dataclass
class SectionBanks:
    alternate: pd.DataFrame = pd.DataFrame([])
    minutes: pd.DataFrame = pd.DataFrame([])
    buzzer: pd.DataFrame = pd.DataFrame([])

    def from_seasons(self, seasons: List[QuizSeason]) -> SectionBanks:
        alternates_bank = pd.concat([season.alternate for season in seasons])
        minutes_bank = pd.concat([season.minutes for season in seasons])
        buzzer_bank = pd.concat([season.buzzer for season in seasons])
        return SectionBanks(alternates_bank, minutes_bank, buzzer_bank)

    def from_round(self, round: int) -> SectionBanks:
        return SectionBanks(
            alternate=self.alternate[self.alternate["Round"] == round],
            minutes=self.minutes[self.minutes["Round"] == round],
            buzzer=self.buzzer[self.buzzer["Round"] == round],
        )

    # def group_alternate(self) -> pd.DataFrame:
    #     return self.alternate.

    # def filter_minutes(self, subjects: Subjects) -> pd.DataFrame:
    #     return filter_by_area_col(self.minutes, subjects)

    # def filter_buzzer(self, subjects: Subjects) -> pd.DataFrame:
    #     return filter_by_area_col(self.buzzer, subjects)

    # def without_infrequent_areas(self, freq_checker: FrequencyChecker):
    #     return SectionBanks(
    #         alternate=drop_infrequent_values(self.alternate, "Area", freq_checker),
    #         minutes=drop_infrequent_values(self.minutes, "Area", freq_checker),
    #         buzzer=drop_infrequent_values(self.buzzer, "Area", freq_checker),
    #     )


def filter_by_area_col(df: pd.DataFrame, subjects: Subjects) -> pd.DataFrame:
    return df[df["Area"] == subjects.value]


def filter_section(section: pd.DataFrame, subjects: Subjects) -> pd.DataFrame:
    return section[section["Area"] == subjects.value]


# class FrequencyChecker:
#     def __init__(self, ser: pd.Series, drop_ratio: float = 0.1):
#         self.ser = ser
#         self.cutoff_freq = self.get_expected_ser_freq()
#         self.drop_ratio = drop_ratio

#     def get_expected_ser_freq(self) -> float:
#         return 1 / len(np.unique(self.ser))

#     def get_infrequent_series_values(self) -> List[str]:
#         frequenies = self.ser.value_counts(normalize=True)
#         allowed_frequenies = frequenies[frequenies > self.cutoff_freq * self.drop_ratio]
#         return [area for area in allowed_frequenies.index]


# def drop_infrequent_values(
#     df: pd.DataFrame, col: str, freq_checker: FrequencyChecker
# ) -> pd.DataFrame:
#     infrequent_cols = freq_checker.get_infrequent_series_values(df[col])
#     return df.drop(infrequent_cols)


# @dataclass
# class GroupedSectionBanks:
#     alternate: DataFrameGroupBy = DataFrameGroupBy(pd.DataFrame([]))
#     minutes: DataFrameGroupBy = DataFrameGroupBy(pd.DataFrame([]))
#     buzzer: DataFrameGroupBy = DataFrameGroupBy(pd.DataFrame([]))

#     def from_section_bank(self, bank: SectionBanks) -> GroupedSectionBanks:
#         return GroupedSectionBanks(
#             alternate=bank.alternate.groupby("Area"),
#             minutes=bank.minutes.groupby("Area"),
#             buzzer=bank.buzzer.groupby("Area"),
#         )


# def get_subject_questions(subject: Subjects, section: DataFrameGroupBy) -> pd.DataFrame:
#     return section.get_group(subject.value)
