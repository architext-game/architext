from typing import Dict, List, Optional
from pydantic import BaseModel, Field, EmailStr
from dataclasses import dataclass

class Command(BaseModel):
    pass

class CreateConnectedRoom(Command):
    name: str = Field(min_length=1, max_length=30)
    description: str = Field(max_length=3000)
    exit_to_new_room_name: str
    exit_to_new_room_description: str
    exit_to_old_room_name: str
    exit_to_old_room_description: str

@dataclass
class CreateConnectedRoomResult:
    room_id: str

class TraverseExit(Command):
    exit_name: str

@dataclass
class TraverseExitResult:
    new_room_id: str

class Login(Command):
    email: EmailStr
    password: str = Field(min_length=3, max_length=50)

@dataclass
class LoginResult:
    user_id: str

class GetCurrentRoom(Command):
    pass

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

class CreateUser(Command):
    email: EmailStr
    name: str = Field(min_length=3, max_length=10)
    password: str = Field(min_length=3, max_length=50)

@dataclass
class CreateUserResult:
    user_id: str

class CreateInitialData(Command):
    pass

@dataclass
class CreateInitialDataResult:
    pass
