import re
from abc import ABC, abstractmethod


class TextCleaner(ABC):
    @abstractmethod
    def clean(self, text: str) -> str:
        pass


class TextCleanerDefault(TextCleaner):
    def clean(self, text: str) -> str:
        text = text.rstrip(" ")
        text = text.rstrip(".")
        return self.rename_areas(text)

    def rename_areas(self, text: str) -> str:
        text = self.rename_bio(text)
        text = self.rename_mus(text)
        text = self.rename_phy(text)
        return self.rename_spo(text)

    @staticmethod
    def rename_bio(text: str) -> str:
        pattern = re.compile(r"bio\b")
        return pattern.sub("Bio", text)

    @staticmethod
    def rename_mus(text: str) -> str:
        pattern = re.compile(r"Mus\b")
        return pattern.sub("Music", text)

    @staticmethod
    def rename_phy(text: str) -> str:
        pattern = re.compile(r"Phy\b")
        return pattern.sub("Phys", text)

    @staticmethod
    def rename_spo(text: str) -> str:
        pattern = re.compile(r"(Spo\b)|(Sport\b)")
        return pattern.sub("Sports", text)
