import os
from typing import Dict, List

import pandas as pd
from google.cloud import bigquery
from google.cloud.bigquery import QueryJob

import config

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.PATH_TO_KEYFILE_JSON
client = bigquery.Client()


def query(sql: str) -> List[Dict]:
    query_job: QueryJob = client.query(sql)
    # null -> None 으로 replace 한다.
    return query_job.to_dataframe().replace({pd.NaT: None}).to_dict('records')
