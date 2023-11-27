"""
New version of services.py using the AbstractRepository instead of mongoengine
"""

from typing import Optional, Literal
from architext.model.validate_target_name import validate_non_takable_name
import architext.service_layer.exceptions as exceptions
import architext.util as util
import architext.adapters.repository as repository
import architext.domain.model as model
import hashlib
import architext.entities.exceptions as exceptions

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

def create_user(repository, name: str, password: str, email:str):
    # operate
    user = model.User(name=name, email=email, password_hash=_hash_password(password))

    # write
    repository.add_user(user)

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

    validate_non_takable_name(
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
        exit_room_id: str,
        user_id: str
    ):
    # TODO: this service mixes write and operate sections
    # read
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
        exit_id: str
):
    user = repository.get_user(user_id)
    avatar = repository.get_avatar(user_id=user.id, world_state_id=user.current_world_state_id)
    exits = repository.get_exits_in_room(avatar.current_room_id)

    if not exit_id in [exit.id for exit in exits]:
        raise Exception()

    exit = repository.get_exit(exit_id)
    avatar.current_room_id = exit.destination_id

    repository.add_avatar(avatar)