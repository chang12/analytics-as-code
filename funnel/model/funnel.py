from typing import List

from pydantic import BaseModel

from funnel.model.step import Step


class Funnel(BaseModel):
    name: str
    human_readable_name: str
    steps: List[str]

    def title(self) -> str:
        return f'{self.human_readable_name} ({self.name})'

    def list_steps(self) -> List[Step]:
        return [Step(name=step) for step in self.steps]
