import abc
import architext.domain.model as model
import typing
import copy

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_room(self, room: model.Room) -> None:
        pass

    @abc.abstractmethod
    def get_room(self, id: str) -> model.Room:
        pass

    @abc.abstractmethod
    def add_world_state(self, world_state: model.WorldState) -> None:
        pass

    @abc.abstractmethod
    def add_world(self, world: model.World) -> None:
        pass

    @abc.abstractmethod
    def get_world_by_state_id(self, world_state_id: str) -> model.World:
        pass

    @abc.abstractmethod
    def add_user(self, user: model.User) -> None:
        pass

    @abc.abstractmethod
    def get_user(self, id: str) -> model.User:
        pass

    @abc.abstractmethod
    def get_world_state(self, id: str) -> model.WorldState:
        pass

    @abc.abstractmethod
    def get_target_names_in_room(self, id: str) -> typing.List[str]:
        pass

    @abc.abstractmethod
    def get_target_names_in_world_state(self, id: str) -> typing.List[str]:
        pass

    @abc.abstractmethod
    def get_takable_item_names_in_world_state(self, id: str) -> typing.List[str]:
        pass

    @abc.abstractmethod
    def get_items_in_room(self, id: str) -> typing.List[model.Item]:
        pass

    @abc.abstractmethod
    def get_exits_in_room(self, id: str) -> typing.List[model.Exit]:
        pass

    @abc.abstractmethod
    def get_rooms_in_world_state(self, id: str) -> typing.List[model.Room]:
        pass

    @abc.abstractmethod
    def add_exit(self, exit: model.Exit) -> None:
        pass

    @abc.abstractmethod
    def get_starting_room_of_world(self, id: str) -> model.Room:
        pass

    @abc.abstractmethod
    def get_world(self, id: str) -> model.World:
        pass

    @abc.abstractmethod
    def get_avatar(self, user_id: str, world_state_id: str) -> model.Avatar | None:
        pass

    @abc.abstractmethod
    def add_avatar(self, avatar: model.Avatar):
        pass

    @abc.abstractmethod
    def get_exit(self, id: str) -> model.Exit:
        pass

    @abc.abstractmethod
    def get_user_by_name(self, username: str) -> model.User | None:
        pass

    @abc.abstractmethod
    def get_user_by_email(self, email: str) -> model.User | None:
        pass


class FakeRepository(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self._item_store: typing.Dict[str, model.Item] = {}
        self._room_store: typing.Dict[str, model.Room] = {}
        self._world_store: typing.Dict[str, model.World] = {}
        self._world_state_store: typing.Dict[str, model.WorldState] = {}
        self._user_store: typing.Dict[str, model.User] = {}
        self._exit_store: typing.Dict[str, model.Exit] = {}
        self._avatar_store: typing.Dict[(str, str), model.Avatar] = {}

        from architext.service_layer.goodservices import create_user
        create_user(name='string', password='string', email='string', repository=self)

    def add_world(self, world: model.World):
        self._world_store[world.id] = world

    def get_world_by_state_id(self, world_state_id: str):
        for world in self._world_store.values():
            if world.world_state_id == world_state_id:
                return copy.deepcopy(world)
        raise KeyError()

    def add_world_state(self, world_state: model.WorldState):
        self._world_state_store[world_state.id] = world_state

    def add_room(self, room: model.Room) -> None:
        self._room_store[room.id] = room

    def get_room(self, id: str) -> model.Room:
        return copy.deepcopy(self._room_store[id])

    def add_user(self, user: model.User) -> None:
        self._user_store[user.id] = user

    def get_user(self, id: str) -> model.User:
        print("USERS", self._user_store)
        return copy.deepcopy(self._user_store[id])

    def get_world_state(self, id: str) -> model.WorldState:
        return copy.deepcopy(self._world_state_store[id])

    def get_target_names_in_room(self, id: str) -> typing.List[str]:
        items = self.get_items_in_room(id)
        exits = self.get_exits_in_room(id)

        names = [item.name for item in items]
        names += [exit.name for exit in exits]

        return copy.deepcopy(names)

    def get_target_names_in_world_state(self, id: str) -> typing.List[str]:
        rooms = self.get_rooms_in_world_state(id)

        names = []
        for room in rooms:
            names += self.get_target_names_in_room(room.id)

        return copy.deepcopy(names)

    def get_takable_item_names_in_world_state(self, id: str) -> typing.List[str]:
        rooms = self.get_rooms_in_world_state(id)

        names = []
        for room in rooms:
            items = self.get_items_in_room(room.id)
            names += [item.name for item in items if item.visibility == 'takable']

        return copy.deepcopy(names)

    def add_exit(self, exit: model.Exit) -> None:
        self._exit_store[exit.id] = exit

    def get_exits_in_room(self, id: str) -> typing.List[model.Exit]:
        room = self.get_room(id)
        return copy.deepcopy([self._exit_store[id] for id in room.exit_ids])

    def get_items_in_room(self, id: str) -> typing.List[model.Item]:
        room = self.get_room(id)
        return copy.deepcopy([self._exit_store[id] for id in room.item_ids])

    def get_rooms_in_world_state(self, id: str) -> typing.List[model.Room]:
        return copy.deepcopy([room for room in self._room_store.values() if room.world_state_id == id])

    def get_world(self, id) -> model.World:
        return copy.deepcopy(self._world_store[id])

    def get_starting_room_of_world(self, id) -> model.Room:
        world = self.get_world(id)
        world_state = self.get_world_state(world.world_state_id)
        return copy.deepcopy(self.get_room(world_state.starting_room_id))

    def get_avatar(self, user_id: str, world_state_id: str) -> model.Avatar | None:
        return copy.deepcopy(self._avatar_store.get((user_id, world_state_id)))

    def add_avatar(self, avatar: model.Avatar):
        self._avatar_store[(avatar.user_id, avatar.world_state_id)] = avatar

    def get_exit(self, id: str) -> model.Exit:
        return self._exit_store[id]

    def get_user_by_email(self, email: str) -> model.User | None:
        for user in self._user_store.values():
            if user.email == email:
                return user
        return None

    def get_user_by_name(self, username: str) -> model.User | None:
        for user in self._user_store.values():
            if user.name == username:
                return user
        return None