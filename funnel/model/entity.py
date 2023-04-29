from enum import Enum


class Entity(str, Enum):
    USER = 'user'
    SESSION = 'session'
