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
from architext.domain.unit_of_work.fake.fake_uow import FakeUnitOfWork
from architext.entrypoints.socketio.jwt_tokens import generate_jwt, decode_jwt
from architext.domain.services.create_user.create_user import create_user, CreateUserInput, CreateUserOutput
from architext.domain.services.get_current_room.get_current_room import get_current_room, GetCurrentRoomOutput
from architext.domain.services.create_connected_room.create_connected_room import create_connected_room, CreateConnectedRoomInput, CreateConnectedRoomOutput
from architext.domain.services.traverse_exit.traverse_exit import traverse_exit, TraverseExitInput, TraverseExitOutput
from architext.domain.services.login.login import login, LoginInput
from architext.domain.services.setup.setup import setup

from architext.entrypoints.socketio.models import ResponseModel
from architext.entrypoints.socketio.sio_event import event, models
from architext.entrypoints.socketio.pydantic_to_typescript import generate_typescript_defs
import argparse
from architext.domain.events.events import UserChangedRoom
from bidict import bidict


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

    uow = FakeUnitOfWork()
    setup(uow)  # run setup according to domain rules

    class OtherEnteredRoomEvent(BaseModel):
        user_name: str

    models.append(OtherEnteredRoomEvent)

    def notify_other_entered_room(event: UserChangedRoom):
        user_who_moved = uow.users.get_user_by_id(event.user_id)
        assert user_who_moved is not None
        users = uow.users.get_users_in_room(event.room_entered)
        for user in users:
            socket_id = sid_to_user_id.inverse[user.id]
            sio.emit(
                'other_entered_room', 
                OtherEnteredRoomEvent(user_name=user_who_moved.name).model_dump(), 
                socket_id
            )

    class OtherLeftRoomEvent(BaseModel):
        user_name: str

    models.append(OtherLeftRoomEvent)

    def notify_other_left_room(event: UserChangedRoom):
        user_who_moved = uow.users.get_user_by_id(event.user_id)
        assert user_who_moved is not None
        users = uow.users.get_users_in_room(event.room_left)
        for user in users:
            print("EMITED")
            socket_id = sid_to_user_id.inverse[user.id]
            sio.emit(
                'other_left_room',
                OtherLeftRoomEvent(user_name=user_who_moved.name).model_dump(),
                socket_id
            )

    uow.messagebus.add_handlers({
        UserChangedRoom: [notify_other_left_room, notify_other_entered_room],
    })
        

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
        out = create_user(uow=uow, input=params)
        print("==================================")
        print(out)
        print('________________________')
        return out    

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
        generate_typescript_defs(models=models, output='./architext/clean/entrypoints/socketio/generated_types.ts')
        import shutil
        shutil.copy(
            './architext/clean/entrypoints/socketio/generated_types.ts',
            './architext/clean/entrypoints/socketio/test_e2e/types.ts'
        )
        print("Done")
    else:
        print("Hello, I am the server, nice to meet you.")
        atexit.register(lambda: print('server stopped'))

        # Create a simple server application
        app = socketio.WSGIApp(sio)
        
        # Use eventlet or gevent for asynchronous server
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
