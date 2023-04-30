from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from funnel.model.column_chart_request import ColumnChartRequest
from funnel.model.funnel_ import funnel_dict
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


@app.get('/funnels/{funnel_name}')
async def read_funnel(request: Request, funnel_name: str):
    return templates.TemplateResponse(
        name='funnel.html',
        context={
            'request': request,
            'funnel': funnel_dict[funnel_name].dict(),
        },
    )


@app.post('/GetDataForColumnChart')
async def get_data_for_column_chart(data: ColumnChartRequest):
    sql = data.to_sql()
    return query(sql)
