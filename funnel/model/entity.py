from enum import Enum


class Entity(str, Enum):
    USER = 'user_id'
    SESSION = 'session_id'
