import os
from datetime import date
from typing import List

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pydantic import BaseModel

import config

env = Environment(loader=FileSystemLoader(os.path.join(config.BASE_PATH, 'funnel/template')), undefined=StrictUndefined)
env.auto_reload = True


class FunnelLineChartRequest(BaseModel):
    event_names: List[str]
    date_s: date
    date_e: date

    def to_sql(self):
        event_name_pairs = list(zip(self.event_names, self.event_names[1:]))

        return env.get_template('line_chart_step_wise_conversions.sql').render(
            event_name_pairs=event_name_pairs,
            date1=self.date_s.isoformat(),
            date2=self.date_e.isoformat(),
        )
