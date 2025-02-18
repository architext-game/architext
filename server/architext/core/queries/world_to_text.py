import base64
from dataclasses import dataclass
import json
import zlib
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.room import Room
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler
from typing import List, Literal, Dict, Union

@dataclass
class WorldToTextResult:
    world_id: str
    format: Literal['plain', 'encoded']
    text_representation: str

class WorldToText(Query[WorldToTextResult]):
    world_id: str
    format: Literal['plain', 'encoded']

class WorldToTextQueryHandler(QueryHandler[WorldToTextResult, WorldToTextResult]):
    pass


def room_to_dict(room: Room) -> Dict:
    return {
        "id": room.id,
        "name": room.name,
        "description": room.description,
        "exits": [exit_to_dict(exit) for exit in room.exits.values()],
        "items": [item_to_dict(item) for item in room.items.values()],
    }

def exit_to_dict(exit: Exit) -> Dict:
    return {
        "name": exit.name,
        "description": exit.description,
        "destination_room_id": exit.destination_room_id,
        "visibility": exit.visibility,
    }

def item_to_dict(item: Item) -> Dict:
    return {
        "name": item.name,
        "description": item.description,
        "visibility": item.visibility,
    }

def encode_dict(dict):
    json_string = json.dumps(dict)
    bytes = json_string.encode('utf-8')
    compressed_bytes = zlib.compress(bytes)
    b64bytes = base64.b64encode(compressed_bytes)
    b64string = b64bytes.decode()
    return b64string

def normalize(data: Union[Dict, List]):
    """Recursively sorts all lists inside a JSON structure to make it order-independent."""
    if isinstance(data, dict):
        return {k: normalize(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Sort lists using a stable sort by converting dicts into tuples for sorting
        return [normalize(item) for item in sorted(data, key=lambda x: json.dumps(x, sort_keys=True) if isinstance(x, dict) else str(x))]
    else:
        return data

class UOWWorldToTextQueryHandler(UOWQueryHandler, WorldToTextQueryHandler):
    def query(self, query: WorldToText, client_user_id: str) -> WorldToTextResult:

        world = self._uow.worlds.get_world_by_id(query.world_id)
        rooms = self._uow.rooms.list_rooms_by_world(query.world_id)

        assert world is not None

        world_dict = {
            "original_name": world.name,
            "original_description": world.description,
            "initial_room_id": world.initial_room_id,
            "rooms": [room_to_dict(room) for room in rooms]
        }

        world_dict = normalize(world_dict)

        if query.format == "plain":
            text_representation = json.dumps(
                world_dict, 
                indent=4,
                separators=(',', ': ')
            )
        elif query.format == "encoded":
            text_representation = encode_dict(world_dict)

        return WorldToTextResult(
            world_id=query.world_id,
            format=query.format,
            text_representation=text_representation
        )
