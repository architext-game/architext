"""
run with 
python3 -m architext.clean.entrypoints.socketio_server.socketio_server
add --types to generate types
"""

import eventlet
eventlet.monkey_patch(socket=True, time=True)
import socketio
import atexit
import os
import json
from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel
from architext.clean.domain.unit_of_work.fake.fake_uow import FakeUnitOfWork
from architext.clean.entrypoints.socketio_server.jwt_tokens import generate_jwt, decode_jwt
from architext.clean.domain.services.create_user.create_user import create_user, CreateUserInput, CreateUserOutput
from architext.clean.domain.services.get_current_room.get_current_room import get_current_room, GetCurrentRoomOutput
from architext.clean.domain.services.create_connected_room.create_connected_room import create_connected_room, CreateConnectedRoomInput, CreateConnectedRoomOutput
from architext.clean.domain.services.traverse_exit.traverse_exit import traverse_exit, TraverseExitInput, TraverseExitOutput
from architext.clean.domain.services.login.login import login, LoginInput
from architext.clean.domain.services.setup.setup import setup
from typing import Dict, Generic, Optional, TypeVar
import dataclasses
from architext.clean.entrypoints.socketio_server.models import ResponseModel
from architext.clean.entrypoints.socketio_server.sio_event import event, models
from architext.clean.entrypoints.socketio_server.pydantic_to_typescript import generate_typescript_defs
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--types', action='store_true', help='Generate typescript types')
    args = parser.parse_args()

    load_dotenv()

    uow = FakeUnitOfWork()
    setup(uow)  # run setup according to domain rules

    #allowed = json.loads(os.environ['ALLOWED_ORIGINS'])
    allowed = ['http://amritb.github.io', 'https://firecamp.dev']
    sio = socketio.Server(cors_allowed_origins=allowed)
    # dictionary relating authenticated sockets with their user ids
    sid_to_user_id: Dict[str, str] = {}

    @sio.event
    def connect(sid, environ, auth):
        print(f'New connection, client_id {sid}')


    class LoginOutput(BaseModel):
        jwt_token: str

    @event(sio=sio, on='login', In=LoginInput, Out=ResponseModel[LoginOutput])
    def login_event(sid, params: LoginInput) -> LoginOutput:
        user_data = login(uow=uow, input=params)
        token = generate_jwt(**user_data.model_dump())
        sid_to_user_id[sid] = user_data.user_id
        return LoginOutput(jwt_token=token)


    class AuthenticateParams(BaseModel):
        jwt_token: str

    class AuthenticateOutput(BaseModel):
        user_id: str

    @event(sio=sio, on='authenticate', In=AuthenticateParams, Out=ResponseModel[AuthenticateOutput])
    def authenticate(sid, params: AuthenticateParams) -> AuthenticateOutput:
        decoded = decode_jwt(params.jwt_token)
        sid_to_user_id[sid] = decoded['user_id']
        return AuthenticateOutput(user_id=decoded['user_id'])
    

    @event(sio=sio, on='signup', In=CreateUserInput, Out=ResponseModel[CreateUserOutput])
    def signup(sid, params: CreateUserInput) -> CreateUserOutput:
        return create_user(uow=uow, input=params)
    

    @event(sio=sio, on='get_current_room', Out=ResponseModel[GetCurrentRoomOutput])
    def get_current_room_event(sid) -> GetCurrentRoomOutput:
        client_user_id = sid_to_user_id[sid]
        return get_current_room(uow, client_user_id=client_user_id)  
        

    @event(sio=sio, on='create_connected_room', In=CreateConnectedRoomInput, Out=ResponseModel[CreateConnectedRoomOutput])
    def create_connected_room_event(sid, params: CreateConnectedRoomInput) -> CreateConnectedRoomOutput:  
        client_user_id = sid_to_user_id[sid]
        return create_connected_room(uow, input=params, client_user_id=client_user_id)  


    @event(sio=sio, on='traverse_exit', In=TraverseExitInput, Out=ResponseModel[TraverseExitOutput])
    def traverse_exit_event(sid, input: TraverseExitInput) -> TraverseExitOutput:
        client_user_id = sid_to_user_id[sid]
        return traverse_exit(uow, input=input, client_user_id=client_user_id)  


    @sio.event
    def disconnect(sid):
        print(f'{sid} disconnected')
    

    if args.types:
        generate_typescript_defs(models=models, output='./architext/clean/entrypoints/socketio_server/generated_types.ts')
        import shutil
        shutil.copy(
            './architext/clean/entrypoints/socketio_server/generated_types.ts',
            './architext/clean/entrypoints/socketio_server/test_e2e/types.ts'
        )
        print("Done")
    else:
        print("Hello, I am the server, nice to meet you.")
        atexit.register(lambda: print('server stopped'))

        # Create a simple server application
        app = socketio.WSGIApp(sio)
        
        # Use eventlet or gevent for asynchronous server
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
