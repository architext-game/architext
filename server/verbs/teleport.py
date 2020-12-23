from .verb import Verb
from .look import Look 
import util
import entities


class TeleportClient(Verb):
    """Allows a creator to travel between any two rooms, using the destination unique alias.
    this command is intended to ease the creation process"""

    command = 'tp '

    def process(self, message):
        command_length = len(self.command)
        room_alias = message[command_length:]
        
        query = entities.Room.objects(alias=room_alias)
        if len(query) == 1:
            self.teleport_client(query.first())
        elif len(query) > 1:
            self.session.send_to_client('Hay más de una sala con ese alias. Esto no debería pasar.')
        elif len(query) == 0:
            self.session.send_to_client("NO hay ninguna sala con ese alias.")

        self.finish_interaction()

    def teleport_client(self, room):
        self.session.user.teleport(room)
        Look(self.session).show_current_room()


class TeleportUser(Verb):
    """Allows a creator to move one user to any room. Usage:
    command 'username' room_alias
    """

    command = "tpotro '"

    def process (self, message):
        message = message[len(self.command):]
        target_user_name, room_alias = message.split("' ", 1)
        target_user = next(entities.User.objects(name=target_user_name, client_id__ne=None), None)
        target_room = next(entities.Room.objects(alias=room_alias), None)
        if target_user is not None and target_room is not None:
            target_user.teleport(target_room)
            self.session.send_to_client("Hecho.")
        else:
            self.session.send_to_client("El usuario no existe o no está conectado, o no hay ninguna sala con ese alias.")
        self.finish_interaction()


class TeleportAllInRoom(Verb):
    """Allows a game master to move all users in his room to other room. Usage:
    command room_alias
    """

    command = "tpsala "

    def process(self, message):
        room_alias = message[len(self.command):]
        target_users = entities.User.objects(room=self.session.user.room, client_id__ne=None)
        target_room = next(entities.Room.objects(alias=room_alias), None)

        if target_room is not None:
            for user in target_users:
                user.teleport(target_room)
            self.session.send_to_client("Hecho")
        else:
            self.session.send_to_client("No existe una sala con ese alias.")
        
        self.finish_interaction()


class TeleportAllInWorld(Verb):
    """Allows a game master to move all connected users to the same room. Usage:
    command room_alias
    """

    command = "tptodos "

    def process(self, message):
        room_alias = message[len(self.command):]
        target_users = entities.User.objects(client_id__ne=None)
        target_room = next(entities.Room.objects(alias=room_alias), None)

        if target_room is not None:
            for user in target_users:
                user.teleport(target_room)
            self.session.send_to_client("Hecho")
        else:
            self.session.send_to_client("No existe una sala con ese alias.")
        
        self.finish_interaction()

