from typing import Type, Optional, List, Dict, Any
import dataclasses
from py_writes_ts import (
    generate_typescript_interfaces, rename_interfaces, generate_typescript_function, 
    generate_typescript_import, ts_name
)


@dataclasses.dataclass
class Endpoint:
    sio_event_name: str
    expected_input: Optional[Any]
    output: Any

@dataclasses.dataclass
class Event:
    sio_event_name: str
    data: Any

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

def replace_type_names(ts_code: str, endpoints: List[Endpoint]):
    model_to_facade_name: Dict[Type, str] = {}

    for endpoint in endpoints:
        model_to_facade_name[endpoint.output] = snake_to_pascal(endpoint.sio_event_name)+'Response'
        if endpoint.expected_input is not None:
            model_to_facade_name[endpoint.expected_input] = snake_to_pascal(endpoint.sio_event_name)+'Params'

    renamed_code = rename_interfaces(ts_code, model_to_facade_name)

    return renamed_code


def generate_endpoint_function(event_name: str, expected_input: Any, output: Any, valid_refs: List[Any]):
    function_name = snake_to_camel(event_name)

    function_body = f"""
return new Promise((resolve, reject) => {{
    socket.emit("{event_name}", params, (response: {ts_name(output)}) => {{
        resolve(response)
    }});
}});
"""
    ts_code = generate_typescript_function(
        function_name=function_name,
        parameters={
            "socket": "Socket",
            "params": expected_input
        },
        return_type=f"Promise<{ts_name(output)}>",
        body=function_body,
        valid_refs=valid_refs,
        is_async=True,
    )

    return ts_code


def generate_event_function(event_name: str, data: Any, valid_refs: List[Any]):
    function_name = 'on' + snake_to_pascal(event_name)

    function_body = f"""
socket.on('{event_name}', callback)
"""
    ts_code = generate_typescript_function(
        function_name=function_name,
        parameters={
            "socket": "Socket",
            "callback": f"(event: {ts_name(data)}) => void"
        },
        return_type=None,
        body=function_body,
        valid_refs=valid_refs,
        is_async=False,
    )

    return ts_code

def generate_sdk(endpoints: List[Endpoint], events: List[Event], extra_models: List[Type]) -> str:
    code = ""
    code += generate_typescript_import("socket.io-client", ["Socket"])
    code += "\n"

    models = [model 
        for endpoint in endpoints 
        for model in (endpoint.expected_input, endpoint.output)
        if model is not None
    ]

    models += [event.data for event in events]

    models += extra_models

    code += generate_typescript_interfaces(models) + "\n"

    for endpoint in endpoints:
        code += generate_endpoint_function(
            event_name=endpoint.sio_event_name,
            expected_input=endpoint.expected_input,
            output=endpoint.output,
            valid_refs=models
        )

    for event in events:
        code += generate_event_function(
            event_name=event.sio_event_name,
            data=event.data,
            valid_refs=models
        )

    code = replace_type_names(code, endpoints)

    return code