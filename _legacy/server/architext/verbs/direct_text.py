from . import verb
from .. import entities
from .. import util

class TextToOne(verb.Verb):
    """Lets game masters send any message to a single user using:
    command 'username' text
    """

    regex_command = True
    command = _("textto (?P<user_name>.+) - (?P<text>.+)")
    permissions = verb.PRIVILEGED

    def process(self, message):
        match = util.match(self.command, message)
        user_name = match['user_name'].strip()
        text = match['text'].strip()

        target_user = util.name_to_entity(self.session, user_name, loose_match=['world_users'])

        if target_user == "many":
            self.session.send_to_client(_("There are more than one user with a similiar name. Try to match case and accents."))
        elif target_user is None:
            self.session.send_to_client(_("That user is not in this world."))
        else:
            self.session.send_to_user(target_user, text)
            self.session.send_to_client(_("Text sent to {user_name}.").format(user_name=target_user.name))

        self.finish_interaction()


class TextToRoom(verb.Verb):
    """Lets game masters send any message to all users in their same room using:
    command text
    """

    command = _("textroom ")
    permissions = verb.PRIVILEGED

    def process(self, message):
        out_message = message[len(self.command):]
        self.session.send_to_room(out_message)
        self.finish_interaction()


class TextToWorld(verb.Verb):
    """Lets game masters send any message to all users in the world using:
    command text
    """

    command = _("textworld ")
    permissions = verb.PRIVILEGED

    def process(self, message):
        out_message = message[len(self.command):]
        self.session.send_to_all(out_message)
        self.finish_interaction()


class TextToRoomUnless(verb.Verb):
    """Lets the game master send any message to all users in a room except one:
    command 'username' text
    """

    command = _("textroombut '")
    permissions = verb.PRIVILEGED

    def process(self, message):
        message = message[len(self.command):]
        exception_user_name, out_message = message.split("' ", 1)
        exception_user = util.name_to_entity(self.session, exception_user_name, loose_match=['room_users'])

        if exception_user == "many":
            self.session.send_to_client(_("There are more than one user with a similiar name. Try to match case and accents."))
        elif exception_user is None:
            self.session.send_to_client(_("That user is not connected or does not exist"))
        else:
            self.session.send_to_client(_("Text send to all users in this room except {user_name}.").format(user_name=exception_user.name))
            self.session.send_to_room_except(exception_user, out_message)
        self.finish_interaction()
