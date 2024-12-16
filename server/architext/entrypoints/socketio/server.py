"""
run with 
python3 -m entrypoints.socketio.server
add --types to generate types
"""

import eventlet
eventlet.monkey_patch(socket=True, time=True)
import socketio
import atexit
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from architext.adapters.memory_uow import MemoryUnitOfWork
from architext.core.messagebus import MessageBus
from architext.entrypoints.socketio.jwt_tokens import generate_jwt, decode_jwt
from architext.core.commands import (
    CreateUser, CreateUserResult,
    GetCurrentRoom, GetCurrentRoomResult,
    CreateConnectedRoom, CreateConnectedRoomResult,
    TraverseExit, TraverseExitResult,
    Login, LoginResult,
    CreateInitialData, CreateInitialDataResult,
)
from architext.entrypoints.socketio.models import ResponseModel
from architext.entrypoints.socketio.sio_event import event, models
from architext.entrypoints.socketio.pydantic_to_typescript import generate_typescript_defs
import argparse
from architext.core.domain.events import UserChangedRoom
from bidict import bidict
from dataclasses import asdict
from architext.adapters.sio_notificator import SocketIONotificator



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--types', action='store_true', help='Generate typescript types')
    args = parser.parse_args()

    load_dotenv()

    #allowed = json.loads(os.environ['ALLOWED_ORIGINS'])
    allowed = ['http://amritb.github.io', 'https://firecamp.dev']
    sio = socketio.Server(cors_allowed_origins=allowed)
    # dictionary relating authenticated sockets with their user ids


    sid_to_user_id: bidict[str, str] = bidict()
    def auth(socket: str, user_id: str):
        """Links a socket with an user_id"""
        if sid_to_user_id.inverse.get(user_id, None) is not None:
            del sid_to_user_id.inverse[user_id]
        sid_to_user_id[socket] = user_id
    
    

    uow = MemoryUnitOfWork(notificator=SocketIONotificator(sio, sid_to_user_id.inverse))
    bus = MessageBus()

    bus.handle(uow, CreateInitialData())


    @sio.event
    def connect(sid, environ, auth):
        print(f'New connection, client_id {sid}')


    @sio.event
    def disconnect(sid):
        print(f'{sid} disconnected')


    class LoginResponse(BaseModel):
        jwt_token: str

    @event(sio=sio, on='login', In=Login, Out=ResponseModel[LoginResponse])
    def login_event(sid, command: Login) -> LoginResponse:
        out = bus.handle(uow, command)
        token = generate_jwt(**asdict(out))
        auth(sid, out.user_id)
        return LoginResponse(jwt_token=token)


    class AuthenticateParams(BaseModel):
        jwt_token: str

    class AuthenticateOutput(BaseModel):
        user_id: str

    @event(sio=sio, on='authenticate', In=AuthenticateParams, Out=ResponseModel[AuthenticateOutput])
    def authenticate(sid, params: AuthenticateParams) -> AuthenticateOutput:
        decoded = decode_jwt(params.jwt_token)
        auth(sid, decoded['user_id'])
        return AuthenticateOutput(user_id=decoded['user_id'])
    

    @event(sio=sio, on='signup', In=CreateUser, Out=ResponseModel[CreateUserResult])
    def signup(sid, command: CreateUser) -> CreateUserResult:
        return bus.handle(uow, command)


    @event(sio=sio, on='get_current_room', Out=ResponseModel[GetCurrentRoomResult])
    def get_current_room_event(sid) -> GetCurrentRoomResult:
        client_user_id = sid_to_user_id[sid]
        return bus.handle(uow, GetCurrentRoom(), client_user_id=client_user_id)  
        

    @event(sio=sio, on='create_connected_room', In=CreateConnectedRoom, Out=ResponseModel[CreateConnectedRoomResult])
    def create_connected_room_event(sid, params: CreateConnectedRoom) -> CreateConnectedRoomResult:  
        client_user_id = sid_to_user_id[sid]
        return bus.handle(uow, params, client_user_id=client_user_id)  


    @event(sio=sio, on='traverse_exit', In=TraverseExit, Out=ResponseModel[TraverseExitResult])
    def traverse_exit_event(sid, input: TraverseExit) -> TraverseExitResult:
        client_user_id = sid_to_user_id[sid]
        return bus.handle(uow, input, client_user_id=client_user_id)  
    

    if args.types:
        from architext.core.handlers.notify_other_entered_room import OtherEnteredRoomNotification
        from architext.core.handlers.notify_other_left_room import OtherLeftRoomNotification
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        from dataclasses import fields, is_dataclass
        from pydantic import BaseModel, create_model

        def dataclass_to_pydantic_model(dataclass_type):
            if not is_dataclass(dataclass_type):
                raise ValueError("Provided class is not a dataclass")
            
            # Extract fields from the dataclass
            pydantic_fields = {
                field.name: (field.type, ...)
                for field in fields(dataclass_type)
            }
            # Create a new Pydantic model dynamically
            return create_model(dataclass_type.__name__, **pydantic_fields)
        
        models += [dataclass_to_pydantic_model(OtherLeftRoomNotification), dataclass_to_pydantic_model(OtherEnteredRoomNotification)]
        generate_typescript_defs(models=models, output='./architext/entrypoints/socketio/generated_types.ts')
        import shutil
        shutil.copy(
            './architext/entrypoints/socketio/generated_types.ts',
            '/home/oliver/vps/apps/architext/server/test/e2e/types.ts'
        )  # too lazy to copy it myself
        print("Done")
    else:
        print("Hello, I am the server, nice to meet you.")
        atexit.register(lambda: print('server stopped'))

        # Create a simple server application
        app = socketio.WSGIApp(sio)
        
        # Use eventlet or gevent for asynchronous server
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
