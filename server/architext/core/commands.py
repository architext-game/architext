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

from typing import Dict, List, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, EmailStr
from dataclasses import dataclass

T = TypeVar('T')

class Command(BaseModel, Generic[T]):
    pass

@dataclass
class CreateConnectedRoomResult:
    room_id: str

class CreateConnectedRoom(Command[CreateConnectedRoomResult]):
    name: str = Field(min_length=1, max_length=30)
    description: str = Field(max_length=3000)
    exit_to_new_room_name: str
    exit_to_new_room_description: str
    exit_to_old_room_name: str
    exit_to_old_room_description: str


@dataclass
class TraverseExitResult:
    new_room_id: str

class TraverseExit(Command[TraverseExitResult]):
    exit_name: str

@dataclass
class LoginResult:
    user_id: str

class Login(Command[LoginResult]):
    email: EmailStr
    password: str = Field(min_length=3, max_length=50)


@dataclass
class PersonInRoom:
    id: str
    name: str

@dataclass
class ExitInRoom:
    name: str
    description: str

@dataclass
class CurrentRoom:
    id: str
    name: str
    description: str
    exits: List[ExitInRoom]
    people: List[PersonInRoom]

@dataclass
class GetCurrentRoomResult:
    current_room: Optional[CurrentRoom]

class GetCurrentRoom(Command[GetCurrentRoomResult]):
    pass

@dataclass
class CreateUserResult:
    user_id: str

class CreateUser(Command[CreateUserResult]):
    email: EmailStr
    name: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=3, max_length=50)


@dataclass
class CreateInitialDataResult:
    pass

class CreateInitialData(Command[CreateInitialDataResult]):
    pass

