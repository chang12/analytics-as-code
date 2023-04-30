import glob
import os
from typing import List, Dict

import yaml
from pydantic import BaseModel

import config
from funnel.model.step import Step


class Funnel(BaseModel):
    name: str
    human_readable_name: str
    steps: List[str]

    def title(self) -> str:
        return f'{self.human_readable_name} ({self.name})'

    def list_steps(self) -> List[Step]:
        return [Step(name=step) for step in self.steps]


funnel_dict: Dict[str, Funnel] = {}
for file in glob.glob(os.path.join(config.BASE_PATH, 'funnel/funnel/*.yaml')):
    with open(file) as fp:
        funnel = Funnel(**yaml.load(fp, Loader=yaml.FullLoader))
        funnel_dict[funnel.name] = funnel
