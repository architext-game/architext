from . import verb
from .. import entities
from .. import util

class TextToOne(verb.Verb):
    """Lets game masters send any message to a single user using:
    command 'username' text
    """

    command = "textoa '"
    permissions = verb.PRIVILEGED

    def process(self, message):
        command_length = len(self.command)
        message = message[command_length:]
        target_user_name, out_message = message.split("' ", 1)
        target_user = util.name_to_entity(self.session, target_user_name, loose_match=['connected_users'])

        if target_user == "many":
            self.session.send_to_client("Hay varios usuarios con un nombre parecido a ese. Intenta poner mayúsculas y acentos.")
        elif target_user is None:
            self.session.send_to_client("Ese usuario no existe o no está conectado.")
        else:
            self.session.send_to_user(target_user, out_message)
            self.session.send_to_client(f"Texto enviado a {target_user.name}.")

        self.finish_interaction()


class TextToRoom(verb.Verb):
    """Lets game masters send any message to all users in their same room using:
    command text
    """

    command = "textosala "
    permissions = verb.PRIVILEGED

    def process(self, message):
        out_message = message[len(self.command):]
        self.session.send_to_room(out_message)
        self.finish_interaction()


class TextToWorld(verb.Verb):
    """Lets game masters send any message to all users in the world using:
    command text
    """

    command = "textomundo "
    permissions = verb.PRIVILEGED

    def process(self, message):
        out_message = message[len(self.command):]
        self.session.send_to_all(out_message)
        self.finish_interaction()


class TextToRoomUnless(verb.Verb):
    """Lets the game master send any message to all users in a room except one:
    command 'username' text
    """

    command = "textomenos '"
    permissions = verb.PRIVILEGED

    def process(self, message):
        message = message[len(self.command):]
        exception_user_name, out_message = message.split("' ", 1)
        exception_user = util.name_to_entity(self.session, exception_user_name, loose_match=['room_users'])

        if exception_user == "many":
            self.session.send_to_client("Hay varios usuarios con un nombre parecido a ese. Intenta poner mayúsculas y acentos.")
        elif exception_user is None:
            self.session.send_to_client("Ese usuario no existe o no está conectado en esta sala.")
        else:
            self.session.send_to_client(f"Texto enviado a todos menos a {exception_user.name}.")
            self.session.send_to_room_except(exception_user, out_message)
        self.finish_interaction()
