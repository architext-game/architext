"""
# Commands module

 - This module defines all commands and command results.
 - Therefore, this module defines de outward facing facade of the `core` module.
 - Commands and results are simple data containers.
 - Each command defines the intent of an user or external system to
 drive this system, and all the needed input params.
 - Results are the object returned by each command as response.
 - Commands perform validation, enforcing some restraints on the input data and
 ensuring that the passed values _seem_ valid (there may still be ids of things
 that do not exist, for example). They use pydantic for that.
 - Responses are simple dataclasses.
"""

from typing import Dict, List, Literal, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, EmailStr
from dataclasses import dataclass
from architext.core.domain.primitives import Visibility
from architext.core.settings import EMAIL_MAX_LENGTH, ROOM_DESCRIPTION_MAX_LENGTH, ROOM_NAME_MAX_LENGTH, EXIT_NAME_MAX_LENGTH, EXIT_DESCRIPTION_MAX_LENGTH, ITEM_NAME_MAX_LENGTH, ITEM_DESCRIPTION_MAX_LENGTH, SOCIAL_INTERACTION_MAX_LENGTH, USER_ID_MAX_LENGTH, USER_NAME_MAX_LENGTH, WORLD_DESCRIPTION_MAX_LENGTH, WORLD_NAME_MAX_LENGTH

T = TypeVar('T')

class Command(BaseModel, Generic[T]):
    pass

@dataclass
class CreateConnectedRoomResult:
    room_id: str

class CreateConnectedRoom(Command[CreateConnectedRoomResult]):
    name: str = Field(min_length=1, max_length=ROOM_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=ROOM_DESCRIPTION_MAX_LENGTH)
    exit_to_new_room_name: str = Field(min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    exit_to_new_room_description: str = Field(min_length=1, max_length=EXIT_DESCRIPTION_MAX_LENGTH)
    exit_to_old_room_name: str = Field(min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    exit_to_old_room_description: str = Field(min_length=1, max_length=EXIT_DESCRIPTION_MAX_LENGTH)


@dataclass
class CreateExitResult:
    pass

class CreateExit(Command[CreateExitResult]):
    in_room_id: str
    name: str = Field(min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=EXIT_DESCRIPTION_MAX_LENGTH)
    destination_room_id: str = Field(min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    visibility: Visibility


@dataclass
class CreateItemResult:
    pass

class CreateItem(Command[CreateItemResult]):
    name: str = Field(min_length=1, max_length=ITEM_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=ITEM_DESCRIPTION_MAX_LENGTH)
    visibility: Visibility


@dataclass
class TraverseExitResult:
    new_room_id: str

class TraverseExit(Command[TraverseExitResult]):
    exit_name: str


@dataclass
class CreateUserResult:
    user_id: str

class CreateUser(Command[CreateUserResult]):
    id: str = Field(min_length=1, max_length=USER_ID_MAX_LENGTH)
    email: EmailStr = Field(max_length=EMAIL_MAX_LENGTH)
    name: str = Field(min_length=1, max_length=USER_NAME_MAX_LENGTH)


@dataclass
class EnterWorldResult:
    pass

class EnterWorld(Command[EnterWorldResult]):
    world_id: str


@dataclass
class CreateTemplateResult:
    template_id: str

class CreateTemplate(Command[CreateTemplateResult]):
    name: str = Field(min_length=1, max_length=WORLD_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=WORLD_DESCRIPTION_MAX_LENGTH)
    base_world_id: str


@dataclass
class RequestWorldImportResult:
    future_world_id: str

class RequestWorldImport(Command[RequestWorldImportResult]):
    name: str = Field(min_length=1, max_length=WORLD_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=WORLD_DESCRIPTION_MAX_LENGTH)
    format: Literal["plain", "encoded"]
    text_representation: str


@dataclass
class RequestWorldCreationFromTemplateResult:
    future_world_id: str

class RequestWorldCreationFromTemplate(Command[RequestWorldCreationFromTemplateResult]):
    name: str = Field(min_length=1, max_length=WORLD_NAME_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=WORLD_DESCRIPTION_MAX_LENGTH)
    template_id: str


@dataclass
class EditWorldResult:
    pass

class EditWorld(Command[EditWorldResult]):
    world_id: str
    name: Optional[str] = Field(min_length=1, max_length=WORLD_NAME_MAX_LENGTH)
    description: Optional[str] = Field(min_length=1, max_length=WORLD_DESCRIPTION_MAX_LENGTH)


@dataclass
class EditExitResult:
    pass

class EditExit(Command[EditExitResult]):
    room_id: str
    exit_name: str
    new_name: Optional[str] = Field(None, min_length=1, max_length=EXIT_NAME_MAX_LENGTH)
    new_description: Optional[str] = Field(None, min_length=1, max_length=EXIT_DESCRIPTION_MAX_LENGTH)
    new_destination: Optional[str] = Field(None)
    new_visibility: Optional[Visibility] = Field(None)


@dataclass
class EditItemResult:
    pass

class EditItem(Command[EditItemResult]):
    room_id: str
    item_name: str
    new_name: Optional[str] = Field(None, min_length=1, max_length=ITEM_NAME_MAX_LENGTH)
    new_description: Optional[str] = Field(None, min_length=1, max_length=ITEM_DESCRIPTION_MAX_LENGTH)
    new_visibility: Optional[Visibility] = Field(None)


@dataclass
class EditRoomResult:
    pass

class EditRoom(Command[EditRoomResult]):
    room_id: str
    new_name: Optional[str] = Field(None, min_length=1, max_length=ROOM_NAME_MAX_LENGTH)
    new_description: Optional[str] = Field(None, min_length=1, max_length=ROOM_DESCRIPTION_MAX_LENGTH)


@dataclass
class DeleteExitResult:
    pass

class DeleteExit(Command[DeleteExitResult]):
    room_id: str
    exit_name: str


@dataclass
class DeleteItemResult:
    pass

class DeleteItem(Command[DeleteItemResult]):
    room_id: str
    item_name: str


@dataclass
class DeleteRoomResult:
    pass

class DeleteRoom(Command[DeleteRoomResult]):
    pass


@dataclass
class SendSocialInteractionResult:
    pass

class SendSocialInteraction(Command[SendSocialInteractionResult]):
    content: str = Field(min_length=1, max_length=SOCIAL_INTERACTION_MAX_LENGTH)
    type: Literal['talk', 'emote']


@dataclass
class MarkUserActiveResult:
    pass

class MarkUserActive(Command[MarkUserActiveResult]):
    active: bool


@dataclass
class SetupResult:
    pass

class Setup(Command[SetupResult]):
    pass


@dataclass
class CompleteMissionResult:
    pass

class CompleteMission(Command[CompleteMissionResult]):
    mission_id: str


@dataclass
class UpdateUserSettingsResult:
    pass

class UpdateUserSettings(Command[UpdateUserSettingsResult]):
    new_name: Optional[str] = Field(min_length=1, max_length=USER_NAME_MAX_LENGTH)