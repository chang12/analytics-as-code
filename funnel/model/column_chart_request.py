from datetime import date
from enum import Enum

from pydantic import BaseModel


class Entity(str, Enum):
    USER = 'user'
    SESSION = 'session'


class ColumnChartRequest(BaseModel):
    date_s: date
    date_e: date
    entity: Entity
