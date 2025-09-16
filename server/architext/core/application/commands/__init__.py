"""
# Services module

 - This module defines the services, aka the command handlers called
 by the messagebus.
 - This init file links each handler with its command from the per-service packages.
"""


from architext.core.application.commands.base import Command

from architext.core.application.commands.create_connected_room import CreateConnectedRoom, create_connected_room, CreateConnectedRoomResult
from architext.core.application.commands.create_template import CreateTemplate, create_template, CreateTemplateResult
from architext.core.application.commands.create_user import CreateUser, create_user, CreateUserResult
from architext.core.application.commands.enter_world import EnterWorld, enter_world, EnterWorldResult
from architext.core.application.commands.send_social_interaction import SendSocialInteraction, send_social_interaction, SendSocialInteractionResult
from architext.core.application.commands.setup import Setup, setup, SetupResult
from architext.core.application.commands.traverse_exit import TraverseExit, traverse_exit, TraverseExitResult
from architext.core.application.commands.request_world_creation_from_template import RequestWorldCreationFromTemplate, request_world_creation_from_template, RequestWorldCreationFromTemplateResult
from architext.core.application.commands.request_world_import import RequestWorldImport, request_world_import, RequestWorldImportResult
from architext.core.application.commands.edit_world import EditWorld, edit_world, EditWorldResult
from architext.core.application.commands.create_exit import CreateExit, create_exit, CreateExitResult
from architext.core.application.commands.edit_exit import EditExit, edit_exit, EditExitResult
from architext.core.application.commands.create_item import CreateItem, create_item, CreateItemResult
from architext.core.application.commands.edit_item import EditItem, edit_item, EditItemResult
from architext.core.application.commands.delete_item import DeleteItem, delete_item, DeleteItemResult
from architext.core.application.commands.delete_exit import DeleteExit, delete_exit, DeleteExitResult
from architext.core.application.commands.delete_room import DeleteRoom, delete_room, DeleteRoomResult
from architext.core.application.commands.edit_room import EditRoom, edit_room, EditRoomResult
from architext.core.application.commands.mark_user_active import MarkUserActive, mark_user_active, MarkUserActiveResult
from architext.core.application.commands.complete_mission import CompleteMission, complete_mission, CompleteMissionResult, MissionUnavailable
from architext.core.application.commands.update_user_settings import UpdateUserSettings, update_user_settings, UpdateUserSettingsResult, NameAlreadyTaken
from architext.core.application.commands.delete_world import DeleteWorld, delete_world, DeleteWorldResult
from architext.core.application.commands.edit_template import EditTemplate, edit_template, EditTemplateResult
from architext.core.application.commands.delete_template import DeleteTemplate, delete_template, DeleteTemplateResult

from typing import Dict, Type, Callable

COMMAND_HANDLERS: Dict[Type[Command], Callable] = {
    CreateUser: create_user,
    CreateConnectedRoom: create_connected_room,
    TraverseExit: traverse_exit,
    EnterWorld: enter_world,
    RequestWorldCreationFromTemplate: request_world_creation_from_template,
    RequestWorldImport: request_world_import,
    CreateTemplate: create_template,
    EditTemplate: edit_template,
    DeleteTemplate: delete_template,
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
    UpdateUserSettings: update_user_settings,
    CompleteMission: complete_mission,
}

__all__ = [
    "COMMAND_HANDLERS",
    # Command classes
    "CreateConnectedRoom",
    "CreateTemplate",
    "CreateUser",
    "EnterWorld",
    "SendSocialInteraction",
    "Setup",
    "TraverseExit",
    "RequestWorldCreationFromTemplate",
    "RequestWorldImport",
    "EditWorld",
    "CreateExit",
    "EditExit",
    "CreateItem",
    "EditItem",
    "DeleteItem",
    "DeleteExit",
    "DeleteRoom",
    "DeleteWorld",
    "EditRoom",
    "MarkUserActive",
    "CompleteMission",
    "UpdateUserSettings",
    "EditTemplate",
    "DeleteTemplate",
    # Result classes
    "CreateConnectedRoomResult",
    "CreateTemplateResult",
    "CreateUserResult",
    "EnterWorldResult",
    "SendSocialInteractionResult",
    "SetupResult",
    "TraverseExitResult",
    "RequestWorldCreationFromTemplateResult",
    "RequestWorldImportResult",
    "EditWorldResult",
    "CreateExitResult",
    "EditExitResult",
    "CreateItemResult",
    "EditItemResult",
    "DeleteItemResult",
    "DeleteExitResult",
    "DeleteRoomResult",
    "DeleteWorldResult",
    "EditRoomResult",
    "MarkUserActiveResult",
    "CompleteMissionResult",
    "UpdateUserSettingsResult",
    "EditTemplateResult",
    "DeleteTemplateResult",
    # Exceptions
    "MissionUnavailable",
    "NameAlreadyTaken",
]