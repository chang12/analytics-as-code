from datetime import date
from typing import List

from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates

from funnel.model.column_chart_request import ColumnChartRequest
from funnel.model.funnel_ import funnel_dict
from funnel.model.funnel_line_chart_request import FunnelLineChartRequest
from funnel.util.bigquery import query

app = FastAPI()

templates = Jinja2Templates(directory='funnel/template')
templates.env.auto_reload = True


@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'funnels': sorted(funnel_dict.values(), key=lambda f: f.name),
        },
    )


@app.get('/funnel')
async def read_funnel(request: Request, name: str = None):
    return templates.TemplateResponse(
        name='funnel.html',
        context={
            'request': request,
            'funnel': funnel_dict[name].dict(),
        },
    )


@app.post('/GetDataForColumnChart')
async def get_data_for_column_chart(data: ColumnChartRequest):
    sql = data.to_sql()
    return query(sql)


@app.get('/funnel-line-chart')
async def funnel_line_chart(request: Request):
    return templates.TemplateResponse(
        name='funnel-line-chart.html',
        context={
            'request': request,
        },
    )


@app.get('/GetDataForLineChart')
async def get_data_for_line_chart(date_s: date, date_e: date, event_names: List[str] = Query(...)):
    request = FunnelLineChartRequest(event_names=event_names, date_s=date_s, date_e=date_e)
    sql = request.to_sql()
    print(sql)
    # return query(sql)
    return [
        {
            "event_name1": "first_open",
            "event_name2": "sign_up",
            "data": [
                {
                    "date": "2023-05-01",
                    "value": 0.812
                },
                {
                    "date": "2023-05-02",
                    "value": 0.828
                },
                {
                    "date": "2023-05-03",
                    "value": 0.821
                }
            ]
        },
        {
            "event_name1": "sign_up",
            "event_name2": "tutorial_completed",
            "data": [
                {
                    "date": "2023-05-01",
                    "value": 0.711
                },
                {
                    "date": "2023-05-02",
                    "value": 0.729
                },
                {
                    "date": "2023-05-03",
                    "value": 0.736
                }
            ]
        }
    ]
