import pandas as pd

from .areas_cleaner import AreasCleaner


def get_clean_section(section: pd.DataFrame, cleaner: AreasCleaner) -> pd.DataFrame:
    section = section.copy()
    section["Area"] = cleaner.clean_col(section["Area"])
    return section
