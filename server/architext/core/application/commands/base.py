from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class Command(BaseModel, Generic[T]):
    pass