import os
from typing import Dict

import yaml
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import config
from funnel.funnel import Funnel
from funnel.model.column_chart_request import ColumnChartRequest

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.PATH_TO_KEYFILE_JSON

app = FastAPI()

templates = Jinja2Templates(directory='funnel/template')

with open('funnel/funnel.yaml', 'r') as fp:
    funnels = yaml.load(fp, Loader=yaml.FullLoader)
    funnels_dict: Dict[str, Funnel] = {funnel['name']: Funnel(**funnel) for funnel in funnels}


@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'funnels': funnels,
        },
    )


@app.get('/funnels/{funnel_name}')
async def read_funnel(request: Request, funnel_name: str):
    return templates.TemplateResponse(
        name='funnel.html',
        context={
            'request': request,
            'funnel': funnels_dict[funnel_name].to_data().dict(),
        },
    )


@app.post('/GetDataForColumnChart')
async def get_data_for_column_chart(data: ColumnChartRequest):
    print(data)
    return data
