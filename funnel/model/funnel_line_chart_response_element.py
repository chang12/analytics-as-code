from typing import List

from pydantic import BaseModel

from funnel.model.funnel_line_chart_response_element_datum import FunnelLineChartResponseElementDatum


class FunnelLineChartResponseElement(BaseModel):
    event_name1: str
    event_name2: str
    data: List[FunnelLineChartResponseElementDatum]
