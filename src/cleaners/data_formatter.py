from abc import ABC, abstractmethod
from typing import List

import numpy as np
import pandas as pd


class DataFormatter(ABC):
    @abstractmethod
    def format_data(self) -> pd.DataFrame:
        pass


class DefaultFormatter(DataFormatter):
    def __init__(self, section_df: pd.DataFrame) -> None:
        self.section_df = section_df.copy()
        self.section_df.columns = self.__get_clean_col_names()

    def __get_clean_col_names(self) -> List[str]:
        try:
            return [col.strip(" ") for col in self.section_df.columns]
        except Exception:
            return list(self.section_df.columns)

    def format_data(self) -> pd.DataFrame:
        return self.get_necessary_data()

    def get_necessary_data(self) -> pd.DataFrame:
        self.section_df = self.section_df[["Match", "Round", "Questions", "Area"]]
        return self.section_df.dropna()


class DataFormatterThirteen(DefaultFormatter):
    def format_data(self) -> pd.DataFrame:
        if self.__is_clean():
            return self.section_df
        self.__add_column_names(self.__get_col_names())
        self.section_df = self.__create_single_question_col_df()
        self.__calculate_round_from_match()
        self.section_df = self.section_df.reset_index(drop=True)
        return self.get_necessary_data()

    def __is_clean(self) -> bool:
        return (
            list(self.section_df.columns) == ["Match", "Area", "Questions", "Round"]
            and self.section_df["Round"].isnull().sum() == 0
        )

    def __add_column_names(self, col_names: List[str]) -> None:
        transposed_df = self.section_df.T.reset_index()
        self.section_df = transposed_df.T.reset_index(drop=True)
        self.section_df.columns = col_names

    def __get_col_names(self) -> List[str]:
        if self.__is_4_col_section():
            return ["Match", "Area", "Questions A", "Questions B"]
        return ["Match", "Area", "Questions"]

    def __is_4_col_section(self) -> bool:
        return self.section_df.shape[1] == 4

    def __create_single_question_col_df(self) -> pd.DataFrame:
        if not self.__is_4_col_section():
            return self.section_df
        question_a = self.section_df.loc[:, ["Match", "Area", "Questions A"]]
        question_b = self.section_df.loc[:, ["Match", "Area", "Questions B"]]
        question_a = question_a.rename(columns={"Questions A": "Questions"})
        question_b = question_b.rename(columns={"Questions B": "Questions"})
        combined = pd.concat([question_a, question_b], axis=0)
        return combined.sort_index()

    def __calculate_round_from_match(self) -> None:
        self.__amend_match_column()
        self.section_df["Round"] = self.section_df["Match"].apply(calculate_round)

    def __amend_match_column(self) -> None:
        self.section_df["Match"] = self.section_df["Match"].replace(
            r"\w", np.nan, regex=True
        )
        self.section_df["Match"] = (
            self.section_df["Match"].fillna(method="ffill").apply(int)
        )


class DataFormatterSeventeen(DefaultFormatter):
    def format_data(self) -> pd.DataFrame:
        self.section_df = self.section_df.rename(columns={"Question": "Questions"})
        return self.get_necessary_data()


class DataFormatterTwenty(DefaultFormatter):
    def format_data(self) -> pd.DataFrame:
        self.section_df = self.section_df.rename(columns={"Question": "Questions"})
        return self.get_necessary_data()


class DataFormatterTwentyOne(DataFormatterTwenty):
    pass


def calculate_round(match_num: int) -> int:
    if match_num < 33:
        return 1
    if match_num < 49:
        return 2
    if match_num < 57:
        return 3
    if match_num < 61:
        return 4
    if match_num < 65:
        return 5
    return 6
