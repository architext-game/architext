import json
from typing import List, Literal, TypedDict


class ExitDict(TypedDict):
    name: str
    description: str
    destination_room_id: str
    visibility: Literal["hidden", "unlisted", "listed", "auto"]

class ItemDict(TypedDict):
    name: str
    description: str
    visibility: Literal["hidden", "unlisted", "listed", "auto"]

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

def visibility(old: str) -> Literal["hidden", "unlisted", "listed", "auto"]:
    if old == "hidden":
        return "hidden"
    if old == "listed":
        return "listed"
    if old == "obvious":
        return "unlisted"
    else:
        raise Exception(f"Bad visibility value {old}")

def convert_json(old_json: dict) -> WorldDict:
    rooms: List[RoomDict] = []
    all_rooms = [old_json["starting_room"]] + old_json["other_rooms"]
    
    for room in all_rooms:
        room_id = room["alias"]
        exits: List[ExitDict] = []
        items: List[ItemDict] = []
        
        for exit_data in old_json["exits"]:
            if exit_data["room"] == room_id:
                exits.append({
                    "name": exit_data["name"],
                    "description": exit_data["description"] or "",
                    "destination_room_id": exit_data["destination"],
                    "visibility": visibility(exit_data["visible"]),
                })
                
        for item in room["items"]:
            items.append({
                "name": item["name"],
                "description": item["description"],
                "visibility": visibility(exit_data["visible"]),
            })
            
        rooms.append({
            "id": room_id,
            "name": room["name"],
            "description": room["description"],
            "exits": exits,
            "items": items
        })
    
    return {
        "original_name": old_json["starting_room"]["name"],
        "original_description": old_json["starting_room"]["description"],
        "initial_room_id": old_json["starting_room"]["alias"],
        "rooms": rooms
    }

# Cargar JSON de entrada
def main():
    with open("input.json", "r", encoding="utf-8") as file:
        old_json = json.load(file)
    
    new_json = convert_json(old_json)
    
    with open("output.json", "w", encoding="utf-8") as file:
        json.dump(new_json, file, indent=4, ensure_ascii=False)
    
    print("Conversión completada. El resultado se ha guardado en output.json")

if __name__ == "__main__":
    main()
