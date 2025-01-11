"""
run with 
python3 -m entrypoints.socketio.server
add --types to generate types
"""

import eventlet

from architext.core.domain.entities.user import User
from architext.core.services.create_user import create_user
eventlet.monkey_patch(socket=True, time=True)
import socketio
import atexit
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from architext.core.adapters.memory_uow import MemoryUnitOfWork
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
from architext.entrypoints.socketio.sio_event import event, endpoints
import argparse
from architext.core.domain.events import UserChangedRoom
from bidict import bidict
from dataclasses import asdict
from architext.core.adapters.sio_notificator import SocketIONotificator
from dataclasses import dataclass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--types', action='store_true', help='Generate typescript types')
    args = parser.parse_args()

    load_dotenv()

    # allowed = json.loads(os.environ['ALLOWED_ORIGINS'])
    # allowed = ['http://207.180.194.96:3000', 'http://amritb.github.io', 'https://firecamp.dev']
    sio = socketio.Server(cors_allowed_origins='*')
    # dictionary relating authenticated sockets with their user ids


    sid_to_user_id: bidict[str, str] = bidict()
    def auth(socket: str, user_id: str):
        """Links a socket with an user_id"""
        if sid_to_user_id.inverse.get(user_id, None) is not None:
            del sid_to_user_id.inverse[user_id]
        sid_to_user_id[socket] = user_id
    
    

    uow = MemoryUnitOfWork(notificator=SocketIONotificator(sio, sid_to_user_id.inverse))
    create_user(uow=uow, command=CreateUser(email='oli@sanz.com', name='oliver', password='oliver'))
    bus = MessageBus()

    bus.handle(uow, CreateInitialData())


    @sio.event
    def connect(sid, environ, auth):
        print(f'New connection, client_id {sid}')


    @sio.event
    def disconnect(sid):
        print(f'{sid} disconnected')

    @dataclass
    class LoginResponse:
        jwt_token: str

    @event(sio=sio, on='login', In=Login, Out=ResponseModel[LoginResponse])
    def login_event(sid, command: Login) -> LoginResponse:
        out = bus.handle(uow, command)
        token = generate_jwt(**asdict(out))
        auth(sid, out.user_id)
        return LoginResponse(jwt_token=token)


    class AuthenticateParams(BaseModel):
        jwt_token: str

    @dataclass
    class AuthenticateOutput:
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
        from architext.entrypoints.socketio.sdk_generator import generate_sdk, Event

        events = [
            Event('other_left_room', OtherLeftRoomNotification),
            Event('other_entered_room', OtherEnteredRoomNotification)
        ]

        sdk_code = generate_sdk(endpoints, events)
        
        print(sdk_code)
        
        with open('./architext/entrypoints/socketio/generated_sdk.ts', "w") as f:
            f.write(sdk_code)
        
        import shutil
        shutil.copy(
            './architext/entrypoints/socketio/generated_sdk.ts',
            '/home/oliver/vps/apps/architext/server/test/e2e/architextSDK.ts'
        )  # too lazy to copy it myself

        shutil.copy(
            './architext/entrypoints/socketio/generated_sdk.ts',
            '/home/oliver/vps/apps/architext/web/src/architextSDK.ts'
        )  # too lazy to copy it myself
        
        print("Done")
    else:
        print("Hello, I am the server, nice to meet you.")
        atexit.register(lambda: print('server stopped'))

        # Create a simple server application
        app = socketio.WSGIApp(sio)
        
        # Use eventlet or gevent for asynchronous server
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
