import yaml
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from funnel.funnel import Funnel

app = FastAPI()

templates = Jinja2Templates(directory='funnel/template')

with open('funnel/funnel.yaml', 'r') as fp:
    funnels = yaml.load(fp, Loader=yaml.FullLoader)
    funnels_dict = {funnel['name']: Funnel(**funnel) for funnel in funnels}


@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'funnels': funnels,
        },
    )


@app.get("/funnels/{funnel_name}")
async def read_funnel(request: Request, funnel_name: str):
    funnel: Funnel = funnels_dict[funnel_name]
    return templates.TemplateResponse(
        'funnel.html',
        {
            'request': request,
            'funnel': funnel,
        }
    )
