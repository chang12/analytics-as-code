import os
from datetime import date
from typing import List

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pydantic import BaseModel

import config

env = Environment(loader=FileSystemLoader(os.path.join(config.BASE_PATH, 'funnel/template')), undefined=StrictUndefined)
env.auto_reload = True
line_chart_template_sql = env.get_template('line_chart_step_wise_conversion.sql')


class FunnelLineChartRequest(BaseModel):
    event_names: List[str]
    date_s: date
    date_e: date

    def to_sql(self):
        event_name1 = 'first_open'
        event_name2 = 'sign_up'

        return line_chart_template_sql.render(
            event_name1=event_name1,
            event_name2=event_name2,
            date1=self.date_s.isoformat(),
            date2=self.date_e.isoformat(),
        )
