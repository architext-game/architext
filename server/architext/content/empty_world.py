from architext.core.queries.world_to_text import encode_text


EMPTY_WORLD = """{
    "original_name": "New World",
    "original_description": "A new world.",
    "initial_room_id": "0",
    "rooms": [
        {
            "id": "0",
            "name": "Empty room",
            "description": "An empty room in an empty world.",
            "exits": [],
            "items": []
        }
    ]
}"""

EMPTY_WORLD_ENCODED = encode_text(EMPTY_WORLD)