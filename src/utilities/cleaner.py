import re
from typing import List, Tuple

import pandas as pd


class Cleaner:
    def clean(self, text: str, remove_chars: Tuple[str]) -> str:
        text = self.remove_unwanted_terminal_chars(text, remove_chars)
        return self.rename_areas(text)

    def remove_unwanted_terminal_chars(
        self, text: str, chars: Tuple[str] = ("",)
    ) -> str:
        text = text.rstrip(" ")
        for char in chars:
            text = text.rstrip(char)
        return text

    def rename_areas(self, text: str) -> str:
        text = self.rename_bio(text)
        text = self.rename_mus(text)
        text = self.rename_phy(text)
        return self.rename_spo(text)

    def rename_bio(self, text: str) -> str:
        pattern = re.compile(r"bio\b")
        return pattern.sub("Bio", text)

    def rename_phy(self, text: str) -> str:
        pattern = re.compile(r"Phy\b")
        return pattern.sub("Phys", text)

    def rename_spo(self, text: str) -> str:
        pattern = re.compile(r"(Spo\b)|(Sport\b)")
        return pattern.sub("Sports", text)

    def rename_mus(self, text: str) -> str:
        pattern = re.compile(r"Mus\b")
        return pattern.sub("Music", text)


class DfCleaner(Cleaner):
    def get_clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.dropna()
        df.columns = self.get_clean_col_names(df)
        df["Area"] = self.get_clean_area_col(df)
        return df

    def get_clean_col_names(self, df: pd.DataFrame) -> List[str]:
        return [self.remove_unwanted_terminal_chars(col) for col in df.columns]

    def get_clean_area_col(self, df: pd.DataFrame) -> pd.Series:
        return df["Area"].apply(lambda x: self.clean(x, remove_chars=(".",)))
