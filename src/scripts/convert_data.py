from pathlib import Path

from ..utilities.configurations import load_config
from ..utilities.factories import AreasCleanerFactory, FormatterFactory
from ..utilities.parquet_store import ParquetStore
from ..utilities.quiz_seasons import ExcelSeasons, QuizSeason


def run(data_dir: Path) -> None:
    excel_seasons = ExcelSeasons().load_from_files(data_dir)
    seasons = [QuizSeason().from_read_excel(season) for season in excel_seasons]

    cleaned_seasons = [
        season.with_clean_data(AreasCleanerFactory(), FormatterFactory())
        for i, season in enumerate(seasons)
    ]

    for season in cleaned_seasons:
        store = ParquetStore(season.section_keys[0])
        dest = store.make_store()
        season.convert_to_parquet(dest)


if __name__ == "__main__":
    config = load_config()
    run(config.filepaths.data_dir)
