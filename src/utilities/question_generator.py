import traceback
from typing import List

import numpy as np
import pandas as pd


class RandomQuestionsGenerator:
    def __init__(
        self, subject_questions: pd.DataFrame, num_questions_per_area: int
    ) -> None:
        self.subject_questions = subject_questions
        self.num_questions_per_area = num_questions_per_area

    def generate_questions(self) -> List[str]:
        if not self.validate_num_questions():
            return [""] * self.num_questions_per_area
        questions = self.subject_questions["Questions"].iloc[
            self.get_question_indices()
        ]
        return [question for question in questions.values]

    def validate_num_questions(self) -> bool:
        return len(self.subject_questions) >= self.num_questions_per_area

    def get_question_indices(self) -> np.ndarray:
        try:
            return np.random.choice(
                range(len(self.subject_questions)),
                size=self.num_questions_per_area,
                replace=False,
            )
        except Exception:
            return np.arange(self.num_questions_per_area)
