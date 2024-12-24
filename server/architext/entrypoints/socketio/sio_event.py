from functools import wraps
from pydantic import BaseModel
from architext.entrypoints.socketio.models import ResponseModel
from typing import Type, Optional, List, Dict, Any
from socketio import Server
import traceback
import dataclasses
from types import new_class

@dataclasses.dataclass
class Endpoint:
    function_name: str
    sio_event_name: str
    expected_input: Optional[Any]
    output: Any

models: List[Type] = []
model_to_facade_name: Dict[Type, str] = {}
endpoints: List[Endpoint] = []

def snake_to_pascal(snake_str):
    return ''.join(word.capitalize() for word in snake_str.split('_'))

def snake_to_camel(snake_str: str) -> str:
    words = snake_str.split('_')
    if not words:
        return ''
    
    # La primera parte en minúscula
    first_part = words[0].lower()
    # El resto se capitaliza y se concatena
    other_parts = [word.capitalize() for word in words[1:]]
    
    return first_part + ''.join(other_parts)

def event(
        sio: Server,  # The socketio server
        on: str,  # The event name
        Out: Type[ResponseModel[Any]], #EJ CreateUserOutput # The output pydantic model (TODO could be changed to dataclass)
        In: Optional[Type[BaseModel]] = None, #EJ CreateUserInput  # The input pydantic model to validate request JSON
    ):
    models.append(Out)
    model_to_facade_name[Out] = snake_to_pascal(on)+'Response'
    endpoint = Endpoint(function_name=snake_to_camel(on), sio_event_name=on, output=Out, expected_input=None)
    if In is not None:
        endpoint.expected_input = In
        models.append(In)
        model_to_facade_name[In] = snake_to_pascal(on)+'Params'
    endpoints.append(endpoint)

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
            return dataclasses.asdict(response)
        return wrapper
    return decorator
