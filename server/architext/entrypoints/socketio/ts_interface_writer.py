from py_writes_ts.class_to_interface import generate_typescript_interfaces

from architext.domain.services.login.login import LoginInput, LoginOutput
from architext.entrypoints.socketio.models import ResponseModel
from architext.entrypoints.socketio.server import OtherEnteredRoomData



"""
EVENTO MANDADO POR EL SERVIDOR
                'other_entered_room', 
                OtherEnteredRoomData(user_name=user_who_moved.name).model_dump()

EVENTO MANDADO POR EL CLIENTE 
                @event(sio=sio, on='login', In=LoginInput, Out=ResponseModel[LoginOutput])
"""


typescript = ""

typescript += generate_typescript_interfaces(interface_names_and_classes=[
    LoginInput,
    ResponseModel[LoginOutput],
    OtherEnteredRoomData
])

print(typescript)