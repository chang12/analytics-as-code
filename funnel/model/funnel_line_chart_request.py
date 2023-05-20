from datetime import date
from typing import List

from pydantic import BaseModel


class FunnelLineChartRequest(BaseModel):
    event_names: List[str]
    date_s: date
    date_e: date
