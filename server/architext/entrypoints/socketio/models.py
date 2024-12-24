from dataclasses import dataclass
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

D = TypeVar('D')

@dataclass
class ResponseModel(Generic[D]):
    success: bool
    data: Optional[D] = None
    error: Optional[str] = None