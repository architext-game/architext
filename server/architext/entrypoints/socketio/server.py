"""
run with 
python3 -m entrypoints.socketio.server
add --types to generate types
"""

from typing import Dict, Type
import eventlet
from eventlet.greenthread import GreenThread
import re
from architext.chatbot.adapters.chatbot_notifier import ChatbotNotifier
from architext.chatbot.adapters.socketio_messaging_channel import SocketIOMessagingChannel
from architext.chatbot.adapters.stdout_logger import StdOutLogger
from architext.chatbot.session import Session
from architext.core.adapters.multi_notifier import MultiNotifier, multi_notifier_mapping_factory
from architext.core.adapters.sio_notifier import SioNotifier
from architext.core.adapters.sqlalchemy.session import db_connection
from architext.core.adapters.sqlalchemy.uow import SQLAlchemyUnitOfWork
from architext.core.facade import Architext
from architext.core.ports.notifier import Notification, WorldCreatedNotification
from architext.core.ports.unit_of_work import UnitOfWork
from architext.core.queries.available_missions import AvailableMissions, AvailableMissionsResult
from architext.core.queries.get_template import GetWorldTemplate, GetWorldTemplateResult
from architext.core.queries.list_world_templates import ListWorldTemplates, ListWorldTemplatesResult, WorldTemplateListItem
from architext.core.queries.me import Me, MeResult, UserNotFound
from architext.core.queries.get_world import GetWorld, GetWorldResult
from architext.core.queries.list_worlds import ListWorlds, ListWorldsResult
from architext.entrypoints.socketio.auth import get_clerk_user_details, user_id_from_clerk_token
from test.fixtures import add_test_data
eventlet.monkey_patch(socket=True, time=True)
import socketio
import atexit
from dotenv import load_dotenv
from pydantic import BaseModel
from architext.core.commands import (
    CompleteMission, CompleteMissionResult, CreateTemplate, CreateTemplateResult, CreateUser, EditWorld, EditWorldResult, EnterWorld, EnterWorldResult,
    CreateConnectedRoom, CreateConnectedRoomResult, MarkUserActive, RequestWorldCreationFromTemplate,
    RequestWorldCreationFromTemplateResult, RequestWorldImport, RequestWorldImportResult, Setup,
    TraverseExit, TraverseExitResult,
)
from architext.entrypoints.socketio.models import ResponseModel
from architext.entrypoints.socketio.sio_event import event, endpoints
import argparse
from bidict import bidict
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

    # App config
    channel = SocketIOMessagingChannel(sio, user_id_to_socket_id=sid_to_user_id.inverse)
    uow = SQLAlchemyUnitOfWork(session_factory=db_connection(at='file'))
    architext = Architext(uow=uow)    
    architext._uow.notifier = MultiNotifier(
        multi_notifier_mapping_factory(
            chatbot=ChatbotNotifier(channel),
            web=SioNotifier(sio=sio, user_id_to_socket_id=sid_to_user_id.inverse)
        )
    )

    architext.handle(Setup(uow=uow, client_user_id=None))

    user_id_to_session: Dict[str, Session] = {}


    @sio.event
    def connect(sid, environ, auth):
        print(f'New connection, socket id {sid}')

    @sio.event
    def disconnect(sid):
        print(f'{sid} disconnected')


    class AuthenticateParams(BaseModel):
        jwt_token: str

    @dataclass
    class AuthenticateOutput:
        user_id: str

    @event(sio=sio, on='authenticate', In=AuthenticateParams, Out=ResponseModel[AuthenticateOutput])
    def authenticate(sid, params: AuthenticateParams) -> AuthenticateOutput:
        user_id = user_id_from_clerk_token(params.jwt_token)
        try:
            architext.query(Me(), user_id)
        except UserNotFound:
            user = get_clerk_user_details(user_id)
            architext.handle(CreateUser(
                id=user.id,
                email=user.email,
                name=user.username,
            ))
        auth(sid, user_id)
        if user_id not in user_id_to_session:
            user_id_to_session[user_id] = Session(
                user_id=user_id,
                logger=StdOutLogger(),
                messaging_channel=SocketIOMessagingChannel(sio, user_id_to_socket_id=sid_to_user_id.inverse),
                architext=architext
            )
        return AuthenticateOutput(user_id=user_id)


    @event(sio=sio, on='create_connected_room', In=CreateConnectedRoom, Out=ResponseModel[CreateConnectedRoomResult])
    def create_connected_room_event(sid, params: CreateConnectedRoom) -> CreateConnectedRoomResult:  
        client_user_id = sid_to_user_id[sid]
        return architext.handle(params, client_user_id=client_user_id)  


    @event(sio=sio, on='traverse_exit', In=TraverseExit, Out=ResponseModel[TraverseExitResult])
    def traverse_exit_event(sid, input: TraverseExit) -> TraverseExitResult:
        client_user_id = sid_to_user_id[sid]
        return architext.handle(input, client_user_id=client_user_id)
    

    inactive_timers: Dict[str, GreenThread] = {}

    def register_user_activity(user_id: str):
        # print(f"Registered activity for user {user_id}")
        architext.handle(MarkUserActive(active=True), user_id)

        if user_id in inactive_timers:
            inactive_timers[user_id].cancel()

        inactive_timers[user_id] = eventlet.spawn_after(30, mark_user_inactive, user_id)

    def mark_user_inactive(user_id: str):
        # print(f"User {user_id} marked as inactive")
        architext.handle(MarkUserActive(active=False), user_id)


    class ChatbotMessage(BaseModel):
        message: str

    @event(sio=sio, on='chatbot_message', In=ChatbotMessage, Out=ResponseModel[None])
    def chatbot_message_event(sid, input: ChatbotMessage) -> None:
        client_user_id = sid_to_user_id[sid]
        register_user_activity(client_user_id)
        
        if client_user_id not in user_id_to_session:
            # TODO: create a session on the fly
            raise Exception("Received message from user without session")

        user_id_to_session[client_user_id].process_message(input.message)

    class Heartbeat(BaseModel):
        pass

    @event(sio=sio, on='heartbeat', In=Heartbeat, Out=ResponseModel[None])
    def heartbeat_event(sid, input: Heartbeat) -> None:
        client_user_id = sid_to_user_id[sid]
        register_user_activity(client_user_id)

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

    @event(sio=sio, on='get_available_missions', In=AvailableMissions, Out=ResponseModel[AvailableMissionsResult])
    def get_available_missions_event(sid, input: Me) -> MeResult:
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

    @event(sio=sio, on='complete_mission', In=CompleteMission, Out=ResponseModel[CompleteMissionResult])
    def complete_mission_event(sid, input: CompleteMission) -> CompleteMissionResult:
        client_user_id = sid_to_user_id[sid]
        return architext.handle(input, client_user_id)

    if args.types:
        from architext.entrypoints.socketio.sdk_generator import generate_sdk, Event
        from architext.chatbot.ports.messaging_channel import Message


        def sio_event_name(notification: Type[Notification]) -> str:
            """Convert PascalCase or camelCase to snake_case."""
            name = notification.__name__
            name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
            name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
            return name.lower()

        def event_entry(notification: Type[Notification]) -> Event:
            return Event(sio_event_name(notification), notification)
        
        events = [
            Event('chatbot_server_message', Message),
            event_entry(WorldCreatedNotification),
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
