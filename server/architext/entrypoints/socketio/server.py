"""
run with 
python3 -m entrypoints.socketio.server
add --types to generate types
"""

from typing import Dict
import eventlet

from architext.chatbot.adapters.socketio_sender import SocketIOSender
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core import Architext
from architext.core.handlers.notify_world_created_to_owner import WorldCreatedNotification
from architext.core.queries.get_current_room import GetCurrentRoomResult, GetCurrentRoom
from architext.core.queries.get_template import GetWorldTemplate, GetWorldTemplateResult
from architext.core.queries.list_world_templates import ListWorldTemplates, ListWorldTemplatesResult, WorldTemplateListItem
from architext.core.queries.me import Me, MeResult
from architext.core.queries.get_world import GetWorld, GetWorldResult
from architext.core.services.create_user import create_user
from architext.core.queries.list_worlds import ListWorlds, ListWorldsResult
from test.fixtures import createTestData
eventlet.monkey_patch(socket=True, time=True)
import socketio
import atexit
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from architext.core.adapters.memory_uow import MemoryUnitOfWork
from architext.entrypoints.socketio.jwt_tokens import generate_jwt, decode_jwt
from architext.core.commands import (
    CreateTemplate, CreateTemplateResult, CreateUser, CreateUserResult, EditWorld, EditWorldResult, EnterWorld, EnterWorldResult,
    CreateConnectedRoom, CreateConnectedRoomResult, RequestWorldCreationFromTemplate, RequestWorldCreationFromTemplateResult, RequestWorldImport, RequestWorldImportResult,
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
    
    
    architext = createTestData()
    architext._uow.notifications = SocketIONotificator(sio, sid_to_user_id.inverse)
    architext.handle(CreateUser(email='oli@sanz.com', name='oliver', password='oliver'))
    # uow = MemoryUnitOfWork(notificator=SocketIONotificator(sio, sid_to_user_id.inverse))
    # create_user(uow=uow, command=CreateUser(email='oli@sanz.com', name='oliver', password='oliver'))
    # architext = Architext(uow=uow)

    architext.handle(CreateInitialData())

    user_id_to_session: Dict[str, Session] = {}


    @sio.event
    def connect(sid, environ, auth):
        print(f'New connection, socket id {sid}')


    @sio.event
    def disconnect(sid):
        print(f'{sid} disconnected')

    @dataclass
    class LoginResponse:
        jwt_token: str

    @event(sio=sio, on='login', In=Login, Out=ResponseModel[LoginResponse])
    def login_event(sid, command: Login) -> LoginResponse:
        out = architext.handle(command)
        if out.user_id not in user_id_to_session:
            user_id_to_session[out.user_id] = Session(
                user_id=out.user_id,
                logger=StdOutLogger(),
                sender=SocketIOSender(sio, user_id_to_socket_id=sid_to_user_id.inverse),
                architext=architext
            )
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
        return architext.handle(command) 


    @event(sio=sio, on='create_connected_room', In=CreateConnectedRoom, Out=ResponseModel[CreateConnectedRoomResult])
    def create_connected_room_event(sid, params: CreateConnectedRoom) -> CreateConnectedRoomResult:  
        client_user_id = sid_to_user_id[sid]
        return architext.handle(params, client_user_id=client_user_id)  


    @event(sio=sio, on='traverse_exit', In=TraverseExit, Out=ResponseModel[TraverseExitResult])
    def traverse_exit_event(sid, input: TraverseExit) -> TraverseExitResult:
        client_user_id = sid_to_user_id[sid]
        return architext.handle(input, client_user_id=client_user_id)
    

    class ChatbotMessage(BaseModel):
        message: str

    @event(sio=sio, on='chatbot_message', In=ChatbotMessage, Out=ResponseModel[None])
    def chatbot_message_event(sid, input: ChatbotMessage) -> None:
        client_user_id = sid_to_user_id[sid]
        if client_user_id in user_id_to_session:
            user_id_to_session[client_user_id].process_message(input.message)

    @event(sio=sio, on='get_worlds', In=ListWorlds, Out=ResponseModel[ListWorldsResult])
    def get_worlds_event(sid, input: ListWorlds) -> ListWorldsResult:
        client_user_id = sid_to_user_id[sid]
        return architext.query(input, client_user_id)

    @event(sio=sio, on='get_world_templates', In=ListWorldTemplates, Out=ResponseModel[ListWorldTemplatesResult])
    def get_world_templates_event(sid, input: ListWorldTemplates) -> ListWorldTemplatesResult:
        client_user_id = sid_to_user_id[sid]
        return architext.query(input, client_user_id)

    @event(sio=sio, on='get_world', In=GetWorld, Out=ResponseModel[GetWorldResult])
    def get_world(sid, input: GetWorld) -> GetWorldResult:
        client_user_id = sid_to_user_id[sid]
        return architext.query(input, client_user_id)
    
    @event(sio=sio, on='get_world_template', In=GetWorldTemplate, Out=ResponseModel[GetWorldTemplateResult])
    def get_world_template_event(sid, input: GetWorldTemplate) -> GetWorldTemplateResult:
        client_user_id = sid_to_user_id[sid]
        return architext.query(input, client_user_id)

    @event(sio=sio, on='edit_world', In=EditWorld, Out=ResponseModel[EditWorldResult])
    def edit_world(sid, input: EditWorld) -> EditWorldResult:
        client_user_id = sid_to_user_id[sid]
        return architext.handle(input, client_user_id)

    @event(sio=sio, on='get_me', In=Me, Out=ResponseModel[MeResult])
    def get_me_event(sid, input: Me) -> MeResult:
        client_user_id = sid_to_user_id[sid]
        return architext.query(input, client_user_id)

    @event(sio=sio, on='enter_world', In=EnterWorld, Out=ResponseModel[EnterWorldResult])
    def enter_world_event(sid, input: EnterWorld) -> EnterWorldResult:
        client_user_id = sid_to_user_id[sid]
        return architext.handle(input, client_user_id)

    @event(sio=sio, on='create_template', In=CreateTemplate, Out=ResponseModel[CreateTemplateResult])
    def create_template_event(sid, input: CreateTemplate) -> CreateTemplateResult:
        client_user_id = sid_to_user_id[sid]
        return architext.handle(input, client_user_id)

    @event(sio=sio, on='request_world_import', In=RequestWorldImport, Out=ResponseModel[RequestWorldImportResult])
    def request_world_import_event(sid, input: RequestWorldImport) -> RequestWorldImportResult:
        client_user_id = sid_to_user_id[sid]
        return architext.handle(input, client_user_id)

    @event(sio=sio, on='request_world_creation_from_template', In=RequestWorldCreationFromTemplate, Out=ResponseModel[RequestWorldCreationFromTemplateResult])
    def request_world_creation_from_template_event(sid, input: RequestWorldCreationFromTemplate) -> RequestWorldCreationFromTemplateResult:
        client_user_id = sid_to_user_id[sid]
        return architext.handle(input, client_user_id)

    if args.types:
        from architext.core.handlers.notify_other_entered_room import OtherEnteredRoomNotification
        from architext.core.handlers.notify_other_left_room import OtherLeftRoomNotification
        from architext.entrypoints.socketio.sdk_generator import generate_sdk, Event
        from architext.chatbot.ports.sender import Message

        events = [
            Event('other_left_room', OtherLeftRoomNotification),
            Event('other_entered_room', OtherEnteredRoomNotification),
            Event('chatbot_server_message', Message),
            Event('world_created', WorldCreatedNotification)
        ]

        extra_models = [
            WorldTemplateListItem
        ]

        sdk_code = generate_sdk(endpoints, events, extra_models)
        
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
