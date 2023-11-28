"""
New version of services.py using the AbstractRepository instead of mongoengine
"""

from typing import Optional, Literal
from architext.model.validate_target_name import validate_non_takable_name as _validate_non_takable_name
import architext.util as util
import architext.adapters.repository as repository
import architext.domain.model as model
import hashlib
import architext.entities.exceptions as exceptions
from architext.domain.name_to_target import name_to_target as _name_to_target

def create_world(
        user_id: str,
        repository: repository.AbstractRepository,
        name: str,
        room_name: str,
        room_description: str,
    ):
    # operate
    room = model.Room(name=room_name, alias=0, description=room_description)
    world_state = model.WorldState(starting_room_id=room.id, next_room_alias=2)
    room.world_state_id = world_state.id
    world = model.World(name=name, world_state_id=world_state.id, creator_id=user_id)

    # write
    repository.add_room(room)
    repository.add_world_state(world_state)
    repository.add_world(world)

    return world.id

def _hash_password(password):
    return hashlib.sha256(bytes(password, 'utf-8')).digest()

def create_user(repository: repository.AbstractRepository, name: str, password: str, email:str):
    # read
    same_email = repository.get_user_by_email(email)
    same_name = repository.get_user_by_name(name)

    # validate
    if same_email:
        raise exceptions.EmailAlreadyInUse()
    if same_name:
        raise exceptions.NameAlreadyInUse()

    # operate / write
    user = model.User(name=name, email=email, password_hash=_hash_password(password))
    repository.add_user(user)
    world_id = create_world(name='First World', repository=repository, room_description='Your first room is this', room_name='First room', user_id=user.id)
    world = repository.get_world(world_id)
    enter_world(repository=repository, user_id=user.id, world_state_id=world.world_state_id)

    return user.id

def create_exit(
        user_id: str,
        repository: repository.AbstractRepository,
        location_room_id: str,
        destination_room_id: str,
        description: str = None,
        name: str = None
    ):
    # read
    location = repository.get_room(location_room_id)
    world = repository.get_world_by_state_id(location.world_state_id)
    others_in_room = repository.get_target_names_in_room(location_room_id)
    takables_in_world = repository.get_takable_item_names_in_world_state(location.world_state_id)

    # validate
    if not world.is_privileged(user_id):
        raise exceptions.InsufficientPrivileges()

    _validate_non_takable_name(
        name=name,
        others_in_room=others_in_room,
        takables_in_world=takables_in_world
    )

    # operate
    new_exit = model.Exit(
        name=name,
        description=description,
        destination_id=destination_room_id,
    )
    location.exit_ids.append(new_exit.id)

    # write
    repository.add_exit(new_exit)
    repository.add_room(location)

    pass

def create_connected_room(
        repository: repository.AbstractRepository,
        name: str,
        description: str,
        exit_name: str,
        entrance_name: str,
        user_id: str,
        exit_room_id: str = None,
    ):
    # TODO: this service mixes write and operate sections
    # read
    if exit_room_id is None:
        user = repository.get_user(user_id)
        avatar = repository.get_avatar(user_id=user_id, world_state_id=user.current_world_state_id)
        exit_room_id = avatar.current_room_id

    old_room = repository.get_room(exit_room_id)
    world_state = repository.get_world_state(old_room.world_state_id)
    world = repository.get_world_by_state_id(world_state.id)

    # validate
    if not world.is_privileged(user_id):
        raise exceptions.InsufficientPrivileges

    # operate / write
    new_room = model.Room(
        alias=world_state.next_room_id,
        description=description,
        name=name,
        world_state_id=world_state.id,
    )
    world_state.next_room_id += 1
    repository.add_room(new_room)
    repository.add_world_state(world_state)
    create_exit(
        repository=repository,
        destination_room_id=new_room.id,
        location_room_id=old_room.id,
        name=entrance_name,
        user_id=user_id,
    )
    create_exit(
        repository=repository,
        destination_room_id=old_room.id,
        location_room_id=new_room.id,
        name=exit_name,
        user_id=user_id,
    )

    return new_room.id


def enter_world(
    repository: repository.AbstractRepository,
    user_id: str,
    world_state_id: str
):
    # read
    avatar = repository.get_avatar(user_id=user_id, world_state_id=world_state_id)
    user = repository.get_user(user_id)
    world_state = repository.get_world_state(world_state_id)

    # validate
    # does the world state, the room, etc, exist?

    # operate
    if not avatar:
        avatar = model.Avatar(
            current_room_id=world_state.starting_room_id,
            user_id=user_id,
            world_state_id=world_state.id
        )
    user.current_world_state_id = world_state_id

    # write
    repository.add_avatar(avatar)  # may be unchanged
    repository.add_user(user)

def use_exit(
        repository: repository.AbstractRepository,
        user_id: str,
        exit_name: str
):
    user = repository.get_user(user_id)
    avatar = repository.get_avatar(user_id=user.id, world_state_id=user.current_world_state_id)

    target = _find_target(name=exit_name, repository=repository, user_id=user_id)

    if not target:
        raise exceptions.TargetNotFound()
    if target['type'] != 'exit':
        raise exceptions.BadTargetType()

    exit = repository.get_exit(target['id'])
    avatar.current_room_id = exit.destination_id

    repository.add_avatar(avatar)


def login(
        repository: repository.AbstractRepository,
        username: str,
        password: str
):
    user = repository.get_user_by_name(username)

    if not user:
        raise exceptions.UserDoesNotExist()
    if user.password_hash != _hash_password(password):
        raise exceptions.IncorrectPassword()

    return user.id

def _find_target(
        repository: repository.AbstractRepository,
        name: str,
        user_id: str
):
    user = repository.get_user(user_id)
    avatar = repository.get_avatar(user_id=user.id, world_state_id=user.current_world_state_id)
    target = _name_to_target(
        name=name,
        room_exits=repository.get_exits_in_room(avatar.current_room_id),
        substr_match=['room_exits'],
    )
    if target is None:
        raise exceptions.TargetNotFound()
    return {
        'id': target.id,
        'type': 'item' if isinstance(target, model.Item) else 'exit'
    }

from typing import TypedDict, List

class RoomData(TypedDict):
    name: str
    description: str

class ExitData(TypedDict):
    name: str
    description: str

class LookData(TypedDict):
    room: RoomData
    exits: List[ExitData]

def look(
        repository: repository.AbstractRepository,
        user_id: str
) -> LookData:
    try:
        user = repository.get_user(user_id)
    except KeyError:
        raise exceptions.UserDoesNotExist()
    avatar = repository.get_avatar(user_id=user.id, world_state_id=user.current_world_state_id)
    room = repository.get_room(avatar.current_room_id)
    exits = repository.get_exits_in_room(room.id)

    room_data = RoomData(description=room.description, name=room.name)
    look_data = LookData(room=room_data, exits=[ExitData(description=exit.description, name=exit.name) for exit in exits])
    return look_data