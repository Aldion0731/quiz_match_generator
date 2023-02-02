from __future__ import annotations

from enum import Enum
from typing import Dict

THIRTEEN_MAP = {
    "Art": "Art",
    "Bible Knowledge": "BK",
    "Biology": "Bio",
    "Chemistry": "Chem",
    "English Language": "Eng",
    "French": "French",
    "General Knowledge": "GK",
    "Geography": "Geo",
    "History": "His",
    "Info Tech": "IT",
    "Information Technology": "IT",
    "Jamaican Heritage": "JH",
    "Literature": "Lit",
    "Local & Int'l Affairs": "CA",
    "Local and Int'l Affairs": "CA",
    "Local and International Affairs": "CA",
    "Math": "Math",
    "Mathematics": "Math",
    "Music": "Music",
    "Physics": "Phys",
    "Religious Knowledge": "GK",
    "Spanish": "Span",
    "Sport": "Sports",
    "Sports": "Sports",
    "TV & Cinema": "The",
    "Theatre and Cinema": "The",
    "Theatre & Cinema": "The",
}


class Subjects(Enum):
    ART = "Art"
    BK = "BK"
    BIO = "Bio"
    CA = "CA"
    CHEM = "Chem"
    ENG = "Eng"
    FRE = "French"
    GEO = "Geo"
    GK = "GK"
    HIS = "His"
    IT = "IT"
    JH = "JH"
    LIT = "Lit"
    MAT = "Math"
    MUS = "Music"
    PHY = "Phys"
    SPA = "Span"
    SPO = "Sports"
    THE = "The"

    @staticmethod
    def from_df_val(df_val: str, mapper: Dict[str, str]) -> Subjects:
        return Subjects(mapper[df_val])
