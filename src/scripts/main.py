from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import pandas as pd

from ..utilities.cleaner import DfCleaner
from ..utilities.configurations import Config, load_config
from ..utilities.quiz_seasons import ExcelSeasons, QuizSeason
from ..utilities.section_banks import SectionBanks, SectionFilter
from ..utilities.sections_builder import SectionBuilder


def run(config: Config, match_round: int | None = None) -> None:
    if match_round is None:
        match_round = proj_config.settings.default_match_round

    excel_seasons = ExcelSeasons().load_from_files(config.filepaths.data_dir)
    seasons = [QuizSeason().from_read_excel(season) for season in excel_seasons]

    cleaner = DfCleaner()
    cleaned_seasons = [season.with_clean_data(cleaner) for season in seasons]

    section_banks = SectionBanks()
    section_banks = section_banks.from_seasons(cleaned_seasons)
    round_bank = section_banks.from_round(match_round)

    alternate_builder = get_section_builder(round_bank.alternate, 4, 2)
    alternate = pd.DataFrame(asdict(alternate_builder.get_paired_questions())).iloc[
        : config.num_round_questions.first
    ]

    minutes_builder = get_section_builder(round_bank.minutes, 6, 2)
    minutes = pd.DataFrame(asdict(minutes_builder.get_paired_questions())).iloc[
        : config.num_round_questions.second
    ]

    buzzer_builder = get_section_builder(round_bank.buzzer, 2, 1)
    buzzer = pd.DataFrame(asdict(buzzer_builder.get_unpaired_questions())).iloc[
        : config.num_round_questions.third
    ]

    match_path = get_match_path(config.filepaths.generated_matches, match_round)

    generate_match(alternate, minutes, buzzer, match_path)


def get_section_builder(
    section_df: pd.DataFrame, num_questions_per_area: int, num_teams: int = 2
) -> SectionBuilder:
    section_filter = SectionFilter(section_df)
    return SectionBuilder(
        section_filter.get_section_questions(num_questions_per_area), num_teams
    )


def generate_match(
    alternate: pd.DataFrame,
    minutes: pd.DataFrame,
    buzzer: pd.DataFrame,
    match_path: Path,
) -> None:
    with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
        match_path, engine="xlsxwriter"
    ) as writer:
        alternate.to_excel(writer, sheet_name="Alternate")
        minutes.to_excel(writer, sheet_name="Minutes")
        buzzer.to_excel(writer, sheet_name="Buzzer")


def get_match_path(dest_dir: Path, match_round) -> Path:
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return dest_dir / f"round-{match_round}_{date}.xlsx"


if __name__ == "__main__":
    proj_config = load_config()
    run(proj_config)
