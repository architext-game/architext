class Verb():
    """This is the template for creating new verbs. Every verb should have Verb as parent.
    This is an abstract class, with some methods not implemented.

    A verb is every action that a user can take in the world. Each verb object processes
    a fixed set of user messages, and takes all the actions relative to them.

    Each verb has its own criteria that determines if it can process a given message. This
    criteria is defined in its can_process(message) method. The session calls the can_process method
    of each verb in its verb list until it finds a verb that can process the message. 

    Then, the session creates a new instance of the verb and lets it process all user messages
    (via the process(message) method) until the verb instance returns True for its method command_finished.
    """
    command = 'verb '

    @classmethod
    def can_process(cls, message):
        if message.startswith(cls.command):
            return True
        else:
            return False

    def __init__(self, session):
        self.session = session
        self.finished = False

    def process(self, message):
        raise Exception('Abstract method of interface Verb not implemented')

    def command_finished(self):
        return self.finished

    def finish_interaction(self):
        """This method must be called from within the Verb when the interaction is finished, so the session
        can pass command to other verbs"""
        self.finished = True