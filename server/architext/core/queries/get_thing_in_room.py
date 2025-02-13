from dataclasses import dataclass, field
import re
from typing import Literal, List, Optional, Union
import unicodedata
from architext.core.authorization import assertUserIsLoggedIn
from architext.core.domain.entities.exit import Exit
from architext.core.domain.entities.item import Item
from architext.core.domain.entities.room import Room
from architext.core.queries.base import Query, QueryHandler, UOWQueryHandler

@dataclass
class ExitInRoom:
    name: str
    description: str

@dataclass
class ItemInRoom:
    name: str
    description: str

@dataclass
class GetThingInRoomResult:
    status: Literal['item_matched', 'exit_matched', 'none_found', 'multiple_matches']
    item_match: Optional[ItemInRoom] = None
    exit_match: Optional[ExitInRoom] = None
    multiple_matches: List[str] = field(default_factory=list)

class GetThingInRoom(Query[GetThingInRoomResult]):
    partial_name: str

class GetThingInRoomQueryHandler(QueryHandler[GetThingInRoom, GetThingInRoomResult]):
    pass

class UOWGetThingInRoomQueryHandler(UOWQueryHandler, GetThingInRoomQueryHandler):
    def query(self, query: GetThingInRoom, client_user_id: str) -> GetThingInRoomResult:
        uow = self._uow
        assertUserIsLoggedIn(uow, client_user_id)
        user = uow.users.get_user_by_id(client_user_id)

        if user is None:
            raise ValueError("User not found")
        if user.room_id is None:
            raise ValueError("User is not in a room")
        current_room = uow.rooms.get_room_by_id(user.room_id)
        if current_room is None:
            raise ValueError(f"Room with id {user.room_id} not found")

        things = list(current_room.items.values()) + list(current_room.exits.values())
        match = complete_name_match(query.partial_name, things)

        if match:
            item_match = isinstance(match, Item)
            return GetThingInRoomResult(
                status="item_matched" if item_match else "exit_matched",
                item_match=match if item_match else None,
                exit_match=match if not item_match else None,
            )

        matches = visible_name_match(query.partial_name, things)

        print("PATATA", matches, [t.name for t in things])

        if len(matches) > 1:
            return GetThingInRoomResult(
                status="multiple_matches",
                multiple_matches=[m.name for m in matches]
            )
        
        if len(matches) == 1:
            match = matches[0]
            item_match = isinstance(match, Item)
            return GetThingInRoomResult(
                status="item_matched" if item_match else "exit_matched",
                item_match=match if item_match else None,
                exit_match=match if not item_match else None,
            )

        matches = hidden_name_match(query.partial_name, things)

        if len(matches) == 1:
            match = matches[0]
            item_match = isinstance(match, Item)
            return GetThingInRoomResult(
                status="item_matched" if item_match else "exit_matched",
                item_match=match if item_match else None,
                exit_match=match if not item_match else None,
            )

        # Nothing matched or many hidden matched
        return GetThingInRoomResult(
            status='none_found'
        )


def normalize(name: str) -> str:
    name = name.lower()
    name = ''.join(c for c in unicodedata.normalize('NFKD', name) if unicodedata.category(c) != 'Mn')
    return name

def equal(name_a: str, name_b: str) -> bool:
    return normalize(name_a) == normalize(name_b)

def substring(substring: str, name: str) -> bool:
    return normalize(substring) in normalize(name)

def complete_words_substring_greater_than_35_percent(substring: str, name: str) -> bool:
    words_substring = re.findall(r'\b\w+\b', substring.lower())
    words_name = re.findall(r'\b\w+\b', name.lower())
    
    pattern = r'\b' + r'\s+'.join(words_substring) + r'\b'
    
    total_chars_substring = sum(len(word) for word in words_substring)
    total_chars_name = sum(len(word) for word in words_name)
    
    if total_chars_substring / total_chars_name < 0.35:
        return False
    
    return re.search(pattern, name.lower()) is not None

def complete_name_match(name: str, things: List[Union[Item, Exit]]):
    match = next((thing for thing in things if equal(thing.name, name)), None)
    return match

def visible_name_match(name: str, things: List[Union[Item, Exit]]):
    matches = [thing for thing in things if substring(name, thing.name) and thing.visibility != "hidden"]
    return matches

def hidden_name_match(name: str, things: List[Union[Item, Exit]]):
    matches = [thing for thing in things if complete_words_substring_greater_than_35_percent(name, thing.name)]
    return matches