from .verb import Verb
from .look import Look 
from .. import util

class Go(Verb):
    """Allows the user to travel between rooms, using their exits."""

    command = _('go ')

    def process(self, message):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        available_exits = [exit.name for exit in self.session.user.room.exits]
        possible_meanings = util.possible_meanings(partial_exit_name, available_exits)
        if len(possible_meanings) == 1:
            selected_exit_name = possible_meanings[0]
            selected_exit = next(filter(lambda e: e.name==selected_exit_name, self.session.user.room.exits))
            self.go(selected_exit)
        elif len(possible_meanings) > 1:
            self.session.send_to_client(_('There is more than one exit with a similar name. Please be more specific.'))
        elif len(possible_meanings) == 0:
            self.session.send_to_client(strings.not_found)

        self.finish_interaction()

    def go(self, selected_exit):
        if not self.session.user.master_mode:
            if not selected_exit.is_open:
                self.session.send_to_client(_('It is closed.'))
                return

        origin_room = self.session.user.room
        self.session.user.move(selected_exit.name)
        there_exit = [exit.name for exit in self.session.user.room.exits if exit.destination == origin_room and not exit.is_hidden()]

        if not self.session.user.master_mode:
            if not selected_exit.is_hidden():
                self.session.send_to_others_in_room(_("{user_name} leaves through {exit_name}.").format(user_name=self.session.user.name, exit_name=selected_exit.name))
            else:
                self.session.send_to_others_in_room(_("{user_name} goes to somewhere.").format(user_name=self.session.user.name))
            if there_exit:
                self.session.send_to_others_in_room(_("{user_name} arrives through {exit_name}.").format(user_name=self.session.user.name, exit_name=there_exit[0]))
            else:
                self.session.send_to_others_in_room(_("{user_name} arrives from somewhere.").format(user_name=self.session.user.name))

        Look(self.session).show_current_room()
