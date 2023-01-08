from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PairedQuestions:
    area: List[str]
    team_a: List[str]
    team_b: List[str]


@dataclass
class UnpairedQuestions:
    area: List[str]
    question: List[str]


class SectionBuilder:
    def __init__(self, section_questions: Dict[str, List[str]], num_teams: int = 2):
        self.section_questions = section_questions
        self.num_teams = num_teams
        self.num_questions_per_area = self.get_num_questions_per_area()

    def get_num_questions_per_area(self) -> int:
        return min(len(self.section_questions[area]) for area in self.section_questions)

    def get_paired_questions(self) -> PairedQuestions:
        ordered_questions = PairedQuestions(area=[], team_a=[], team_b=[])
        for i in range(0, self.num_questions_per_area, self.num_teams):
            for area in self.section_questions:
                ordered_questions.area.append(area)
                ordered_questions.team_a.append(self.section_questions[area][i])
                ordered_questions.team_b.append(self.section_questions[area][i + 1])
        return ordered_questions

    def get_unpaired_questions(self) -> UnpairedQuestions:
        questions = UnpairedQuestions(area=[], question=[])
        for i in range(0, self.num_questions_per_area):
            for area in self.section_questions:
                questions.area.append(area)
                questions.question.append(self.section_questions[area][i])
        return questions
