from . import verb
import textwrap

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
            self.session.send_to_client(textwrap.dedent(f"""
                Modo director
                {chr(9472)*13}
                En este modo:
                 {chr(9679)} Eres invisible para el resto de jugadores.
                 {chr(9679)} Puedes usar salidas cerradas.
                 
                Has entrado en el modo director."""))

        self.finish_interaction()