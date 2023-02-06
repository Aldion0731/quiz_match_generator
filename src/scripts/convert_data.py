from pathlib import Path

from ..utilities.configurations import load_config
from ..utilities.factories import SeasonCleanerFactory
from ..utilities.parquet_store import ParquetStore
from ..utilities.quiz_seasons import ExcelSeasons, QuizSeason


def run(data_dir: Path) -> None:
    excel_seasons = ExcelSeasons().load_from_files(data_dir)
    seasons = [QuizSeason().from_read_excel(season) for season in excel_seasons]

    section_keys = [season.section_keys for season in seasons]
    cleaners = [SeasonCleanerFactory().create_from(keys) for keys in section_keys]
    cleaned_seasons = [
        season.with_clean_data(cleaners[i]) for i, season in enumerate(seasons)
    ]

    for season in cleaned_seasons:
        store = ParquetStore(season.section_keys[0])
        dest = store.make_store()
        season.convert_to_parquet(dest)


if __name__ == "__main__":
    config = load_config()
    run(config.filepaths.data_dir)
