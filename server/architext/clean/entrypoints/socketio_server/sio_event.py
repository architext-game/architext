from functools import wraps
from pydantic import BaseModel
from architext.clean.entrypoints.socketio_server.models import ResponseModel
from typing import Type, Optional, List, Dict
from socketio import Server
import traceback

models: List[Type] = []

def snake_to_pascal(snake_str):
    return ''.join(word.capitalize() for word in snake_str.split('_'))

def event(
        sio: Server,  # The socketio server
        on: str,  # The event name
        Out: Type[ResponseModel], #EJ CreateUserOutput # The output pydantic model (TODO could be changed to dataclass)
        In: Optional[Type[BaseModel]] = None, #EJ CreateUserInput  # The input pydantic model to validate request JSON
    ):
    models.append(type(snake_to_pascal(on)+'Response', (Out,), {}))
    if In is not None:
        models.append(type(snake_to_pascal(on)+'Params', (In,), {}))
    def decorator(func):

        @sio.on(on)
        @wraps(func)
        def wrapper(sid, data: Dict):
            try:
                if In is None:
                    response_data = func(sid)
                else:
                    input_data = In(**data)
                    response_data = func(sid, input_data)
                response = Out(success=True, data=response_data, error=None)
            except Exception as error:
                print(traceback.format_exc())
                response = Out(success=False, error=str(error), data=None)
            return response.model_dump()
        return wrapper
    return decorator
