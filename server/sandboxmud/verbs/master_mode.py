from . import verb
import textwrap

class MasterMode(verb.Verb):
    """Lets players enter and leave master mode"""

    command = _('mastermode')
    permissions = verb.PRIVILEGED

    def process(self, message):
        if self.session.user.master_mode:
            self.session.user.leave_master_mode()
            self.session.send_to_client(_("You left master mode"))
        else:
            self.session.user.enter_master_mode()
            self.session.send_to_client(_(
                'Master mode\n'
                '───────────\n'
                'While in master mode:\n'
                ' ● You are invisible to the rest of players.\n'
                ' ● You can go through closed exits.\n'
                '\n'
                'You are now in master mode. Enter "mastermode" again to go back to normal mode.'
            ))

        self.finish_interaction()