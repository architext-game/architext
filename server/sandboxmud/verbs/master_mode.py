from . import verb

class MasterMode(verb.Verb):
    """Lets players enter and leave master mode"""

    command = 'director'
    permissions = verb.PRIVILEGED

    def process(self, message):
        if self.session.user.master_mode:
            self.session.user.leave_master_mode()
            self.session.send_to_client("Has salido del modo director.")
        else:
            self.session.user.enter_master_mode()
            self.session.send_to_client("Has entrado en el modo director.")

        self.finish_interaction()