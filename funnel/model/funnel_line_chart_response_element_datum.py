import datetime

from pydantic import BaseModel


class FunnelLineChartResponseElementDatum(BaseModel):
    date: datetime.date
    value: float
