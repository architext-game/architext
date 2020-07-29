"""Defines the Session class, used to handle user interaction.
"""
import entities
import verbs as v

class Session:
    """This class handles interaction with a single user, though it can send messages to other users as well, to inform them of the session's user actions.
    The Session is responsible for:
      - Redirecting messages sent by its client to the right verb to process them.
      - Provide methods to verbs for sending messages from the client's perspective: only to the client, to other users in the client's room, etc.
      - Asking verbs if the interaction is finished so it can keep using the verb to process messages or poll again for a new verb.
      - Handle client disconnection.
    """

    # List of all verbs supported by the session, ordered by priority: if two verbs can handle the same message, the first will have preference.
    verbs = [v.Build, v.Emote, v.Go, v.Help, v.Login, v.Look, v.Remodel, v.Say, v.Shout, v.Craft, v.EditItem, v.Connect, v.Teleport, v.DeleteRoom, v.DeleteItem, v.DeleteExit, v.Info]

    def __init__(self, session_id, server):
        self.server = server  # server used to send messages
        self.session_id = session_id  # direction to send messages to our client
        self.current_verb = v.Login(self)  # verb that is currently handling interaction. It starts with the log-in process.
        self.user = None  # here we'll have an User entity once the log-in is completed.
        

    def process_message(self, message):
        """This method processes a message sent by the client.
        It polls all verbs, using their can_process method to find a verb that can process the message.
        Then makes that verb the current_verb and lets it handle the message.
        """
        if self.current_verb is None:
            for verb in self.verbs:
                if verb.can_process(message):
                    self.current_verb = verb(self)
                    break

        if self.current_verb is not None:
            self.current_verb.process(message)
            if self.current_verb.command_finished():
                self.current_verb = None
        else:
            self.send_to_client("No te entiendo.")

    def disconnect(self):
        if self.user is not None:
            self.send_to_others_in_room("¡Whoop! {} se ha esfumado.".format(self.user.name))
            self.user.disconnect()

    def send_to_client(self, message):
        self.server.send_message(self.session_id, "\n\r"+message)

    def send_to_others_in_room(self, message):
        users_in_this_room = entities.User.objects(room=self.user.room)
        for user in users_in_this_room:
            if user != self.user:
                self.server.send_message(user.client_id, message)

    def send_to_room(self, message):
        users_in_this_room = entities.User.objects(room=self.user.room)
        for user in users_in_this_room:
            self.server.send_message(user.client_id, message)

    def send_to_all(self, message):
        for user in entities.User.objects:
            self.server.send_message(user.client_id, message)