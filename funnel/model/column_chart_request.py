import os
from datetime import date

import yaml
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

import config
from funnel.model.entity import Entity
from funnel.model.funnel import Funnel

env = Environment(loader=FileSystemLoader(os.path.join(config.BASE_PATH, 'funnel/template')))
funnel_sql_template = env.get_template('funnel.sql')


class ColumnChartRequest(BaseModel):
    funnel_name: str
    date_s: date
    date_e: date
    entity: Entity

    def to_sql(self) -> str:
        with open(os.path.join(config.BASE_PATH, f'funnel/funnel/{self.funnel_name}.yaml'), 'r') as fp:
            funnel = Funnel(**yaml.load(fp, Loader=yaml.FullLoader))
            return funnel_sql_template.render(funnel=funnel)
