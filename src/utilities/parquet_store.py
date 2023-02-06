import os
from pathlib import Path


class ParquetStore:
    def __init__(self, section_key: str) -> None:
        self.dest = Path("data") / section_key.split(" ")[0]

    def make_store(self) -> Path:
        if not self.dest.exists():
            os.makedirs(self.dest)
        return self.dest
