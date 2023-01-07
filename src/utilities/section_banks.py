from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from .configurations import load_config
from .quiz_seasons import QuizSeason
from .subjects import Subjects


@dataclass
class SectionBanks:
    alternate: pd.DataFrame = pd.DataFrame([])
    minutes: pd.DataFrame = pd.DataFrame([])
    buzzer: pd.DataFrame = pd.DataFrame([])

    def from_seasons(self, seasons: List[QuizSeason]) -> SectionBanks:
        alternates_bank = pd.concat([season.alternate for season in seasons])
        minutes_bank = pd.concat([season.minutes for season in seasons])
        buzzer_bank = pd.concat([season.buzzer for season in seasons])
        return SectionBanks(alternates_bank, minutes_bank, buzzer_bank)

    def from_round(self, round: int) -> SectionBanks:
        return SectionBanks(
            alternate=self.alternate[self.alternate["Round"] == round],
            minutes=self.minutes[self.minutes["Round"] == round],
            buzzer=self.buzzer[self.buzzer["Round"] == round],
        )


class SectionFilter:
    def __init__(self, questions: pd.DataFrame):
        self.questions = questions.copy()
        self.grouped_subjects = self.questions.groupby("Area")
        self.subjects = self.grouped_subjects.groups.keys()
        self.mean_freq_quotient = load_config().settings.mean_frequency_quotient

    def filter_infrequent_subjects(self) -> pd.DataFrame:
        self.questions = pd.concat(
            [
                self.grouped_subjects.get_group(subject)
                for subject in self.subjects
                if len(self.grouped_subjects.get_group(subject))
                > self.get_min_allowed_subject_freq()
            ],
            axis=0,
        )

    def filter_subject(self, subject: Subjects) -> pd.DataFrame:
        self.questions = self.questions[self.questions["Area"] == subject.value]

    def __get_mean_subject_freq(self):
        return self.questions["Area"].value_counts().mean()

    def get_min_allowed_subject_freq(self):
        return self.__get_mean_subject_freq() / self.mean_freq_quotient
