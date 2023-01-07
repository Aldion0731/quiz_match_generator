from dataclasses import dataclass
from pathlib import Path

from serde import Strict, serde
from serde.toml import from_toml


@serde(type_check=Strict)
@dataclass(frozen=True)
class Settings:
    mean_frequency_quotient: int


@serde(type_check=Strict)
@dataclass(frozen=True)
class Filepaths:
    data_dir: Path


@serde(type_check=Strict)
@dataclass(frozen=True)
class Config:
    settings: Settings
    filepaths: Filepaths


def load_config(config_file: Path = Path("config.toml")) -> Config:
    with open(config_file) as file:
        return from_toml(Config, file.read())
