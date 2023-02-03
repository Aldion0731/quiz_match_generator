from abc import ABC, abstractmethod

from .subjects import MapNames, Subjects


class AreasCleaner(ABC):
    @abstractmethod
    def clean(self, text: str) -> str:
        pass


class AreasCleanerDefault(AreasCleaner):
    def clean(self, text: str) -> str:
        text = text.rstrip(" ")
        text = text.rstrip(".")
        return self.rename_area(text)

    def rename_area(self, text: str) -> str:
        return Subjects.from_df_val(text, MapNames.DEFAULT).value


class AreasCleanerThirteen(AreasCleanerDefault):
    def rename_area(self, text: str) -> str:
        try:
            return super().rename_area(text)
        except Exception:
            return Subjects.from_df_val(text, MapNames.THIRTEEN).value
