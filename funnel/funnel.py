import os
from typing import List, Dict, Any

import yaml
from google.cloud import bigquery
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

import config

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')))

funnel_sql_template = env.get_template('funnel.sql')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'funnel.yaml'), 'r') as fp:
    funnels = yaml.load(fp, Loader=yaml.FullLoader)


class Step(BaseModel):
    name: str

    def get_table_id(self) -> str:
        return f'{config.PROJECT_ID}.{config.DATASET_ID}.{self.name}'


class Funnel(BaseModel):
    name: str
    human_readable_name: str
    steps: List[str]

    def title(self) -> str:
        return f'{self.human_readable_name} ({self.name})'

    def to_dict(self) -> Dict:
        base = self.dict()
        base['steps'] = self.query_data()
        return base

    def list_steps(self) -> List[Step]:
        return [Step(name=step) for step in self.steps]

    def get_query(self) -> str:
        return funnel_sql_template.render(funnel=self)

    def query_data(self) -> List[Dict[str, Any]]:
        client = bigquery.Client(project=config.PROJECT_ID)
        query_job = client.query(self.get_query())
        return query_job.to_dataframe().to_dict('records')


if __name__ == '__main__':
    funnel = Funnel(**funnels[0])
    print(funnel.get_query())
