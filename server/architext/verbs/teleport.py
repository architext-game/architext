from . import verb
from .look import Look 
from .. import util
from .. import entities
import architext.strings as strings

class Recall(verb.Verb):
    """Puts the player in the starting room of current world"""

    command = _("recall")

    def process(self, message):
        starting_room = self.session.user.room.world_state.starting_room
        self.session.user.teleport(starting_room)
        Look(self.session).show_current_room()
        self.finish_interaction()

class TeleportClient(verb.Verb):
    """Allows a creator to travel between any two rooms, using the destination unique alias.
    this command is intended to ease the creation process"""

    command = _('tp ')
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        room_alias = message[command_length:]
        
        query = entities.Room.objects(alias=room_alias, world_state=self.session.user.room.world_state)
        if len(query) == 1:
            self.teleport_client(query.first())
        elif len(query) > 1:
            raise Exception('There is more than one room with the same alias.')
        elif len(query) == 0:
            self.session.send_to_client(strings.room_not_found)

        self.finish_interaction()

    def teleport_client(self, room):
        self.session.user.teleport(room)
        Look(self.session).show_current_room()


class TeleportUser(verb.Verb):
    """Allows a creator to move one user to any room. Usage:
    command 'username' room_alias
    """

    command = _("tpuser '")
    permissions = verb.PRIVILEGED

    def process (self, message):
        message = message[len(self.command):]
        target_user_name, room_alias = message.split("' ", 1)
        target_user = next(entities.User.objects(name=target_user_name, room__ne=None, client_id__ne=None), None)
        if target_user:
            target_user = target_user if target_user.room.world_state == self.session.user.room.world_state else None
        target_room = next(entities.Room.objects(alias=room_alias, world_state=self.session.user.room.world_state), None)
        if target_user is not None and target_room is not None:
            target_user.teleport(target_room)
            self.session.send_to_client(_("Done. Note that this verb moves players but doesn't tell them that they have been moved. You can tell them using text verbs if you want to."))
        else:
            self.session.send_to_client(_("The user isn't on this world or there is not a room with that room number."))
        self.finish_interaction()


class TeleportAllInRoom(verb.Verb):
    """Allows a game master to move all users in his room to other room. Usage:
    command room_alias
    """

    command = _("tproom ")
    permissions = verb.PRIVILEGED

    def process(self, message):
        room_alias = message[len(self.command):]
        target_users = entities.User.objects(room=self.session.user.room, client_id__ne=None)
        target_room = next(entities.Room.objects(alias=room_alias, world_state=self.session.user.room.world_state), None)

        if target_room is not None:
            for user in target_users:
                user.teleport(target_room)
            self.session.send_to_client(_("Done. Note that this verb  moves players but doesn't tell them that they have been moved. You can tell them using text verbs if you want to."))
        else:
            self.session.send_to_client(strings.room_not_found)
        
        self.finish_interaction()


class TeleportAllInWorld(verb.Verb):
    """Allows a game master to move all connected users to the same room. Usage:
    command room_alias
    """

    command = _("tpall ")
    permissions = verb.PRIVILEGED

    def process(self, message):
        room_alias = message[len(self.command):]
        target_users = entities.User.objects(client_id__ne=None)
        target_room = next(entities.Room.objects(alias=room_alias, world_state=self.session.user.room.world_state), None)

        if target_room is not None:
            for user in target_users:
                user.teleport(target_room)
            self.session.send_to_client(_("Done. Note that this verb only  players but doesn't tell them that they have been moved. You can tell them using text verbs if you want to."))
        else:
            self.session.send_to_client(strings.room_not_found)
        
        self.finish_interaction()

