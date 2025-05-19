"""
# Services module

 - This module defines the services, aka the command handlers called
 by the messagebus.
 - This init file links each handler with its command from the `commands` module.
"""


from architext.core.commands import (
    CreateConnectedRoom,
    CreateTemplate,
    CreateUser,
    EnterWorld,
    SendSocialInteraction,
    Setup,
    TraverseExit,
    RequestWorldCreationFromTemplate,
    RequestWorldImport,
    Command,
    EditWorld,
    CreateExit,
    EditExit,
    CreateItem,
    EditItem,
    DeleteItem,
    DeleteExit,
    DeleteRoom,
    EditRoom,
    MarkUserActive,
    CompleteMission,
    UpdateUserSettings,
    DeleteWorld,
)

from architext.core.services.setup import setup
from architext.core.services.send_social_interaction import send_social_interaction
from architext.core.services.edit_world import edit_world
from architext.core.services.create_template import create_template
from architext.core.services.create_user import create_user
from architext.core.services.create_connected_room import create_connected_room
from architext.core.services.traverse_exit import traverse_exit
from architext.core.services.enter_world import enter_world
from architext.core.services.request_world_creation_from_template import request_world_creation_from_template
from architext.core.services.request_world_import import request_world_import
from architext.core.services.create_exit import create_exit
from architext.core.services.edit_exit import edit_exit
from architext.core.services.create_item import create_item
from architext.core.services.edit_item import edit_item
from architext.core.services.delete_item import delete_item
from architext.core.services.delete_exit import delete_exit
from architext.core.services.delete_room import delete_room
from architext.core.services.edit_room import edit_room
from architext.core.services.mark_user_active import mark_user_active
from architext.core.services.complete_mission import complete_mission
from architext.core.services.update_user_settings import update_user_settings
from architext.core.services.delete_world import delete_world

from typing import Dict, Type, Callable

COMMAND_HANDLERS: Dict[Type[Command], Callable] = {
    CreateUser: create_user,
    CreateConnectedRoom: create_connected_room,
    TraverseExit: traverse_exit,
    EnterWorld: enter_world,
    RequestWorldCreationFromTemplate: request_world_creation_from_template,
    RequestWorldImport: request_world_import,
    CreateTemplate: create_template,
    EditWorld: edit_world,
    CreateExit: create_exit,
    EditExit: edit_exit,
    CreateItem: create_item,
    EditItem: edit_item,
    DeleteItem: delete_item,
    DeleteExit: delete_exit,
    DeleteRoom: delete_room,
    DeleteWorld: delete_world,
    EditRoom: edit_room,
    SendSocialInteraction: send_social_interaction,
    MarkUserActive: mark_user_active,
    Setup: setup,
    CompleteMission: complete_mission,
    UpdateUserSettings: update_user_settings,
}