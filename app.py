import glob
import os

import yaml
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import config
from funnel.model.column_chart_request import ColumnChartRequest
from funnel.model.funnel import Funnel
from funnel.util.bigquery import query

app = FastAPI()

templates = Jinja2Templates(directory='funnel/template')

funnel_dict = {}
for file in glob.glob(os.path.join(config.BASE_PATH, 'funnel/funnel/*.yaml')):
    with open(file) as fp:
        funnel = Funnel(**yaml.load(fp, Loader=yaml.FullLoader))
        funnel_dict[funnel.name] = funnel


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
    print(data)
    sql = data.to_sql()
    return query(sql)
