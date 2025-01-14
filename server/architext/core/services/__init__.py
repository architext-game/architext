"""
# Services module

 - This module defines the services, aka the command handlers called
 by the messagebus.
 - This init file links each handler with its command from the `commands` module.
"""


from architext.core.commands import (
    CreateConnectedRoom,
    CreateInitialData,
    CreateUser,
    CreateWorld,
    EnterWorld,
    GetCurrentRoom,
    Login,
    TraverseExit,
    Command
)

from architext.core.services.create_world import create_world
from architext.core.services.create_user import create_user
from architext.core.services.create_connected_room import create_connected_room
from architext.core.services.create_initial_data import create_initial_data
from architext.core.services.get_current_room import get_current_room
from architext.core.services.login import login
from architext.core.services.traverse_exit import traverse_exit
from architext.core.services.enter_world import enter_world

from typing import Dict, Type, Callable

COMMAND_HANDLERS: Dict[Type[Command], Callable] = {
    CreateUser: create_user,
    CreateConnectedRoom: create_connected_room,
    CreateInitialData: create_initial_data,
    GetCurrentRoom: get_current_room,
    Login: login,
    TraverseExit: traverse_exit,
    CreateWorld: create_world,
    EnterWorld: enter_world,
}