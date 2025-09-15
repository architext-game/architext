import base64
import json
from typing import List
import uuid
import zlib
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.room import Room
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.world import World
from architext.core.domain.events import WorldCreated, WorldCreationRequested
from architext.core.domain.primitives import Visibility
from architext.core.ports.unit_of_work import UnitOfWork
from pydantic import TypeAdapter
from typing_extensions import TypedDict


def decode_text(encoded_str: str) -> str:
    compresed_b64bytes = base64.b64decode(encoded_str)
    b64bytes = zlib.decompress(compresed_b64bytes)
    json_str = b64bytes.decode()
    return json_str

class ExitDict(TypedDict):
    name: str
    description: str
    destination_room_id: str
    visibility: Visibility

class ItemDict(TypedDict):
    name: str
    description: str
    visibility: Visibility

class RoomDict(TypedDict):
    id: str
    name: str
    description: str
    exits: List[ExitDict]
    items: List[ItemDict]

class WorldDict(TypedDict):
    original_name: str
    original_description: str
    initial_room_id: str
    rooms: List[RoomDict]
    

world_dict_type_adapter = TypeAdapter(WorldDict)

def replace_ids(game_data: WorldDict):
    """
    Mutates `game_data` so that each unique 'id' becomes a new UUID,
    and references to that 'id' in 'destination_room_id' or 'initial_room_id' match accordingly.
    """
    # old_id -> new_uuid
    id_map = {}

    def get_new_id(old_id: str) -> str:
        """Return a UUID string for old_id, reusing existing ones if already mapped."""
        if old_id not in id_map:
            id_map[old_id] = str(uuid.uuid4())
        return id_map[old_id]

    # 1) Replace the initial_room_id
    if "initial_room_id" in game_data:
        old_init_id = game_data["initial_room_id"]
        game_data["initial_room_id"] = get_new_id(old_init_id)

    # 2) Replace each room's id and store it in the id_map
    for room in game_data["rooms"]:
        old_id = room["id"]
        new_id = get_new_id(old_id)
        room["id"] = new_id

    # 3) Replace each exit's destination_room_id using the same mapping
    for room in game_data["rooms"]:
        for exit_ in room.get("exits", []):
            dest_id = exit_["destination_room_id"]
            exit_["destination_room_id"] = get_new_id(dest_id)

def import_world(uow: UnitOfWork, event: WorldCreationRequested):
    with uow as transaction:
        world_id = event.future_world_id

        if event.format == "encoded":
            world_text = decode_text(event.text_representation)
        elif event.format == "plain":
            world_text = event.text_representation
        else:
            raise Exception(f"Unknown format {event.format}")

        # This will fail for invalid input
        world_dict = world_dict_type_adapter.validate_python(json.loads(world_text))

        replace_ids(world_dict)

        world = World(
            name=event.world_name,
            description=event.world_description,
            id=world_id,
            initial_room_id=world_dict["initial_room_id"],
            owner_user_id=event.user_id,
            base_template_id=event.base_template_id,
            visibility=event.visibility,
        )

        rooms = [Room(
            id=room["id"],
            name=room["name"],
            description=room["description"],
            world_id=world_id,
            exits={exit["name"]: Exit(
                name=exit["name"],
                description=exit["description"],
                destination_room_id=exit["destination_room_id"]
            ) for exit in room["exits"]},
            items={item["name"]: Item(
                name=item["name"],
                description=item["description"],
            ) for item in room["items"]}
        ) for room in world_dict["rooms"]]

        transaction.worlds.save_world(world)
        for room in rooms:
            transaction.rooms.save_room(room)

        transaction.external_events.publish(WorldCreated(
            owner_id=event.user_id,
            world_id=world.id
        ))
