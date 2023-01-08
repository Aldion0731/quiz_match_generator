from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .configurations import load_config
from .question_generator import RandomQuestionsGenerator
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

    def from_round(self, match_round: int) -> SectionBanks:
        return SectionBanks(
            alternate=self.alternate[self.alternate["Round"] == match_round],
            minutes=self.minutes[self.minutes["Round"] == match_round],
            buzzer=self.buzzer[self.buzzer["Round"] == match_round],
        )


class SectionFilter:
    def __init__(self, section_questions: pd.DataFrame):
        self.section_questions = section_questions
        self.grouped_subjects = self.section_questions.groupby("Area")
        self.subjects = self.grouped_subjects.groups.keys()
        self.mean_freq_quotient = load_config().settings.mean_frequency_quotient
        self.questions_frequent_areas = self.__get_questions_frequent_areas()

    def __get_questions_frequent_areas(self) -> pd.DataFrame:
        return pd.concat(
            [
                self.grouped_subjects.get_group(subject)
                for subject in self.subjects
                if len(self.grouped_subjects.get_group(subject))
                > self.get_min_allowed_subject_freq()
            ],
            axis=0,
        )

    def get_min_allowed_subject_freq(self) -> float:
        return self.__get_mean_subject_freq() / self.mean_freq_quotient

    def __get_mean_subject_freq(self) -> float:
        return self.section_questions["Area"].value_counts().mean()

    def get_subject_frequent_only(self, subject: Subjects) -> pd.DataFrame:
        return self.questions_frequent_areas[
            self.questions_frequent_areas["Area"] == subject.value
        ]

    def get_section_questions(
        self, num_questions_per_area: int
    ) -> Dict[str, List[str]]:
        """
        Returns a dictionary of the form {"BK": [ques 1, ques 1], "Bio": [ques1 , ques 2]}
        """
        section_questions: Dict[str, List[str]] = {}
        for subject in self.get_frequent_subjects():
            subject_bank = self.get_subject_frequent_only(subject)
            question_generator = RandomQuestionsGenerator(
                subject_bank, num_questions_per_area
            )
            section_questions[subject.value] = question_generator.generate_questions()
        return section_questions

    def get_frequent_subjects(self) -> List[Subjects]:
        return [
            Subjects(subject)
            for subject in self.questions_frequent_areas["Area"].unique()
        ]
