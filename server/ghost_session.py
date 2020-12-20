from session import Session
import special_words
import entities

class GhostSession(Session):
    """This is a ghost session that the system uses to perform automated tasks
    like player defined verbs. The tasks are executed as normal messages that
    a ghost session processes as if it were a normal session. 

    The differences whith a normal session are:
     - A ghost session doesn't respond to the client that is issuing it
       messages, because there is none.
     - A ghost session belongs to the user specified in the field GHOST_USER_NAME.
       This user cannot be used by normal sessions.
     - A ghost session ends as soon as the automated task does.
    """

    def __init__(self, server, start_room):
        GHOST_USER_NAME = special_words.GHOST_USER_NAME  # name of the ghost user
        PLACEHOLDER_SESSION_ID = -1  # with this invalid id, the server won't send messages meant to the session's client 
        super().__init__(PLACEHOLDER_SESSION_ID, server)  # normal session __init__. Assigns session id and server.
        self.current_verb = None  # we want to not have an assigned verb at sesion creation.

        # retrieve or create ghost user and put in in the right room.
        if entities.User.objects(name=GHOST_USER_NAME):
            self.session.user = entities.User.objects(name=GHOST_USER_NAME).first()
            self.session.user.connect(self.session.session_id)
            self.session.user.teleport(start_room)
        else:
            self.session.user = entities.User(name=GHOST_USER_NAME, room=start_room)
            self.session.user.connect(self.session.session_id)
