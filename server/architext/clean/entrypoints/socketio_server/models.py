from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

D = TypeVar('D')

class ResponseModel(BaseModel, Generic[D]):
    success: bool
    data: Optional[D] = None
    error: Optional[str] = None