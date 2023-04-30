from typing import Optional

from pydantic import BaseModel

import config


class Step(BaseModel):
    name: str
    value: Optional[int]
    value_prev: Optional[int]
    value_init: Optional[int]
    idx: Optional[int]

    def get_table_id(self) -> str:
        return f'{config.DATASET_ID}.{self.name}'
