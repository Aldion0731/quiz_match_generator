from dataclasses import asdict

import numpy as np
import pandas as pd

from ..utilities.areas_cleaner import AreasCleanerDefault
from ..utilities.configurations import load_config
from ..utilities.factories import SeasonCleanerFactory
from ..utilities.question_generator import RandomQuestionsGenerator
from ..utilities.quiz_seasons import ExcelSeasons, QuizSeason
from ..utilities.season_cleaner import SeasonCleanerDefault
from ..utilities.section_banks import SectionBanks, SectionFilter
from ..utilities.sections_builder import SectionBuilder
from ..utilities.subjects import Subjects

DATA_DIR = load_config().filepaths.data_dir
EXCEL_SEASONS = ExcelSeasons().load_from_files(DATA_DIR)
SEASONS = [QuizSeason().from_read_excel(season) for season in EXCEL_SEASONS]
SECTION_KEYS = [season.section_keys for season in SEASONS]
CLEANERS = [SeasonCleanerFactory().create_from(keys) for keys in SECTION_KEYS]
CLEANED_SEASONS = [
    season.with_clean_data(CLEANERS[i]) for i, season in enumerate(SEASONS)
]
SECTION_BANKS = SectionBanks().from_seasons(CLEANED_SEASONS)
ALTERNATE_FILTER = SectionFilter(SECTION_BANKS.alternate)


def test_load_excel_season() -> None:
    assert len(EXCEL_SEASONS) > 0
    assert [isinstance(item, dict) for item in EXCEL_SEASONS]


def test_text_season_cleaner_default() -> None:
    df = pd.DataFrame(
        {
            "Area    ": ["bio", "Phy", "Spo", "Sport", "Mus", "Sports"],
            "Test ": ["test", "test", "test", "test", "test", None],
        }
    )
    areas_cleaner = AreasCleanerDefault()
    cleaner = SeasonCleanerDefault(areas_cleaner)
    clean_df = cleaner.get_clean_section(df)
    assert clean_df.equals(
        pd.DataFrame(
            {
                "Area": ["Bio", "Phys", "Sports", "Sports", "Music"],
                "Test": ["test", "test", "test", "test", "test"],
            }
        )
    )


def test_clean_banks() -> None:
    for section in SECTION_BANKS.alternate, SECTION_BANKS.minutes, SECTION_BANKS.buzzer:
        assert section["Area"].isin(["bio", "Phy", "Spo", "Sport", "Mus"]).sum() == 0
        for col in section.columns:
            assert not col.endswith(" ")

    for section in SECTION_BANKS.alternate, SECTION_BANKS.minutes, SECTION_BANKS.buzzer:
        assert (
            section["Area"].isin(["Bio", "Phys", "Sports", "Sports", "Music"]).sum()
            != 0
        )


def test_round() -> None:
    for round_num in range(1, 7):
        match_round = SECTION_BANKS.from_round(round_num)
        for section in match_round.alternate, match_round.minutes, match_round.buzzer:
            assert np.array_equal(section["Round"].unique(), np.array([round_num]))


def test_alternate_filter() -> None:
    alternate_filter = SectionFilter(SECTION_BANKS.alternate)
    assert alternate_filter.get_min_allowed_subject_freq() > 10
    assert (
        alternate_filter.questions_frequent_areas["Area"].value_counts()
        < alternate_filter.get_min_allowed_subject_freq()
    ).sum() == 0


def test_subject_filter() -> None:
    alternate_filter = SectionFilter(SECTION_BANKS.alternate)
    for subject in Subjects:
        subject_df = alternate_filter.get_subject_frequent_only(subject)
        if len(subject_df) == 0:
            continue
        assert np.array_equal(
            subject_df["Area"].unique(),
            np.array([subject.value]),
        )


def test_random_question_generator_empty() -> None:
    test_questions = pd.DataFrame(
        {"Area": ["Bio"] * 2, "Questions": [f"question {i}" for i in range(2)]}
    )
    question_generator = RandomQuestionsGenerator(test_questions, 3)
    questions = question_generator.generate_questions()
    assert questions == ["", "", ""]


def test_random_question_generator_non_empty() -> None:
    test_questions = pd.DataFrame(
        {"Area": ["Bio"] * 2, "Questions": [f"question {i}" for i in range(2)]}
    )
    question_generator = RandomQuestionsGenerator(test_questions, 2)
    questions = question_generator.generate_questions()
    assert questions in [
        ["question 0", "question 1"],
        [
            "question 1",
            "question 0",
        ],
    ]


def test_section_questions_filter() -> None:
    test_questions = pd.DataFrame(
        {
            "Area": ["Bio"] * 10 + ["BK"] * 10 + ["Art"],
            "Questions": [f"question {i}" for i in range(21)],
        }
    )
    section_filter = SectionFilter(test_questions)
    assert section_filter.get_frequent_subjects() == [Subjects.BK, Subjects.BIO]


def test_num_questions_per_area() -> None:
    section_questions = {
        "Bio": [f"Bio {i}" for i in range(4)],
        "BK": [f"BK {i}" for i in range(4)],
    }
    section_builder = SectionBuilder(section_questions, 2)
    assert section_builder.num_questions_per_area == 4


def test_paired_questions() -> None:
    section_questions = {
        "Bio": [f"Bio {i}" for i in range(4)],
        "BK": [f"BK {i}" for i in range(4)],
    }
    section_builder = SectionBuilder(section_questions, 2)
    question_pairs = section_builder.get_paired_questions()
    assert question_pairs.area == ["Bio", "BK", "Bio", "BK"]
    assert question_pairs.team_a == ["Bio 0", "BK 0", "Bio 2", "BK 2"]
    assert question_pairs.team_b == ["Bio 1", "BK 1", "Bio 3", "BK 3"]


def test_unpaired_questions() -> None:
    section_questions = {
        "Bio": [f"Bio {i}" for i in range(2)],
        "BK": [f"BK {i}" for i in range(2)],
        "Sports": [f"Sports {i}" for i in range(2)],
    }
    section_builder = SectionBuilder(section_questions, 1)
    questions = section_builder.get_unpaired_questions()
    assert questions.area == ["Bio", "BK", "Sports", "Bio", "BK", "Sports"]
    assert questions.question == [
        "Bio 0",
        "BK 0",
        "Sports 0",
        "Bio 1",
        "BK 1",
        "Sports 1",
    ]


def test_section_print() -> None:
    section_questions = {
        "BK": [f"BK {i}" for i in range(2)],
        "Bio": [f"Bio {i}" for i in range(2)],
        "Sports": [f"Sports {i}" for i in range(2)],
    }
    section_builder = SectionBuilder(section_questions, 2)
    paired_questions = section_builder.get_paired_questions()
    assert pd.DataFrame(asdict(paired_questions)).equals(
        pd.DataFrame(
            {
                "area": ["BK", "Bio", "Sports"],
                "team_a": ["BK 0", "Bio 0", "Sports 0"],
                "team_b": ["BK 1", "Bio 1", "Sports 1"],
            }
        )
    )
