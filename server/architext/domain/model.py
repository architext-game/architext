import typing
import uuid

def generate_uuid():
    return uuid.uuid4()

Visibility = typing.Literal['listed', 'hidden', 'obvious', 'takable']

class CustomVerb():
    def __init__(
            self,
            names: typing.List[str],
            commands: typing.List[str]
    ):
        self.names = names
        self.comands = commands

class Item():
    def __init__(
        self,
        name: str,
        visibility: Visibility,
        id: typing.Optional[str] = None,
        custom_verbs: typing.List[CustomVerb] = []
    ):
        self.id: str = id if id else generate_uuid()
        self.name = name
        self.visibility = visibility
        self.custom_verbs = custom_verbs

class World():
    def __init__(
        self,
        name: str,
        world_state_id: str,
        creator_id: str,
        public: bool = False,
        all_can_edit: bool = False,
        editor_ids: typing.List[str] = [],
        snapshot_ids: typing.List[str] = [],
        id: typing.Optional[str] = None,
    ):
        self.name = name
        self.id: str = id if id else generate_uuid()
        self.world_state_id = world_state_id
        self.snapshot_ids = snapshot_ids
        self.editor_ids = editor_ids
        self.creator_id = creator_id
        self.public = public
        self.all_can_edit = all_can_edit

    def is_privileged(self, user_id: str):
        return self.all_can_edit or user_id == self.creator_id or user_id in self.editor_ids

class WorldState():
    def __init__(
        self,
        next_room_alias: int,
        starting_room_id: str,
        custom_verbs: typing.List[CustomVerb] = [],
        id: typing.Optional[str] = None,
    ):
        self.id: str = id if id else generate_uuid()
        self.starting_room_id = starting_room_id
        self.custom_verbs = custom_verbs
        self.next_room_id = next_room_alias

class Exit():
    def __init__(
        self,
        name: str,
        destination_id: str,
        description: str,
        visible: Visibility = 'listed',
        is_open: bool = True,
        key_names: typing.List[str] = [],
        id: typing.Optional[str] = None,
    ):
        self.id: str = id if id else generate_uuid()
        self.name = name
        self.destination_id = destination_id
        self.description = description
        self.visible = visible
        self.is_open = is_open
        self.key_names = key_names

class Room():
    def __init__(
        self,
        name: str,
        alias: str,
        description: str,
        world_state_id: str = None,  # added to facilitate privilege checks
        id: typing.Optional[str] = None,
        custom_verbs: typing.List[CustomVerb] = [],
        item_ids: typing.List[str] = [],
        exit_ids: typing.List[str] = []
    ):
        self.id: str = id if id else generate_uuid()
        self.name = name
        self.alias = alias
        self.description = description
        self.custom_verbs = custom_verbs
        self.item_ids = item_ids
        self.exit_ids = exit_ids
        self.world_state_id = world_state_id


class User():
    def __init__(
        self,
        name: str,
        email: str,
        password_hash: str,
        current_world_state_id: str = None,
        id: typing.Optional[str] = None,
    ) -> None:
        self.name = name
        self.email = email
        self.id: str = id if id else generate_uuid()
        self.current_world_state_id = current_world_state_id
        self.password_hash = password_hash


class Avatar():
    def __init__(
        self,
        current_room_id: str,
        user_id: str,
        world_state_id: str,
    ) -> None:
        self.current_room_id = current_room_id
        self.user_id = user_id
        self.world_state_id = world_state_id