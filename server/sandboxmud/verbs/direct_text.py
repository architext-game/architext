from . import verb
from .. import entities

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
        target_user = next(entities.User.objects(name=target_user_name, client_id__ne=None), None)
        if target_user is not None:
            self.session.send_to_user(target_user, out_message)
        else:
            self.session.send_to_client("Ese usuario no existe o no está conectado.")
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
        exception_user = next(entities.User.objects(name=exception_user_name, room=self.session.user.room, client_id__ne=None), None)
        if exception_user is not None:
            self.session.send_to_room_except(exception_user, out_message)
        else:
            self.session.send_to_client("El usuario al que no quieres enviar el mensaje no está en esta sala. No se ha enviado mensaje a ningún jugador.")
        self.finish_interaction()
