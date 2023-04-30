import os
from datetime import date

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

import config
from funnel.model.entity import Entity
from funnel.model.funnel_ import funnel_dict

env = Environment(loader=FileSystemLoader(os.path.join(config.BASE_PATH, 'funnel/template')))
env.auto_reload = True
sql_template_column_chart = env.get_template('column_chart.sql')


class ColumnChartRequest(BaseModel):
    funnel_name: str
    date_s: date
    date_e: date
    entity: Entity

    class Config:
        # dict() 때 enum 을 value 로 serialize 하기 위함 이다.
        # https://stackoverflow.com/a/65211727
        use_enum_values = True

    def to_sql(self) -> str:
        funnel = funnel_dict[self.funnel_name]
        return sql_template_column_chart.render(
            steps=funnel.list_steps(),
            **self.dict(),
        )
