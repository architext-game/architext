"""
# Services module

 - This module defines the services, aka the command handlers called
 by the messagebus.
 - This init file links each handler with its command from the `commands` module.
"""


from architext.core.commands import (
    CreateConnectedRoom,
    CreateInitialData,
    CreateTemplate,
    CreateUser,
    EnterWorld,
    GetCurrentRoom,
    Login,
    TraverseExit,
    RequestWorldCreationFromTemplate,
    RequestWorldImport,
    Command,
    EditWorld,
    CreateExit,
)

from architext.core.services.edit_world import edit_world
from architext.core.services.create_template import create_template
from architext.core.services.create_user import create_user
from architext.core.services.create_connected_room import create_connected_room
from architext.core.services.create_initial_data import create_initial_data
from architext.core.services.get_current_room import get_current_room
from architext.core.services.login import login
from architext.core.services.traverse_exit import traverse_exit
from architext.core.services.enter_world import enter_world
from architext.core.services.request_world_creation_from_template import request_world_creation_from_template
from architext.core.services.request_world_import import request_world_import
from architext.core.services.create_exit import create_exit

from typing import Dict, Type, Callable

COMMAND_HANDLERS: Dict[Type[Command], Callable] = {
    CreateUser: create_user,
    CreateConnectedRoom: create_connected_room,
    CreateInitialData: create_initial_data,
    GetCurrentRoom: get_current_room,
    Login: login,
    TraverseExit: traverse_exit,
    EnterWorld: enter_world,
    RequestWorldCreationFromTemplate: request_world_creation_from_template,
    RequestWorldImport: request_world_import,
    CreateTemplate: create_template,
    EditWorld: edit_world,
    CreateExit: create_exit,
}