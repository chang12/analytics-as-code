import os
from typing import Dict, List

from google.cloud import bigquery
from google.cloud.bigquery import QueryJob

import config

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.PATH_TO_KEYFILE_JSON
client = bigquery.Client()


def query(sql: str) -> List[Dict]:
    query_job: QueryJob = client.query(sql)
    return list(query_job.result())
