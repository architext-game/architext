from .verb import Verb
from .look import Look 
from .. import util
from .. import strings
import architext.service_layer.goodservices as services
import architext.domain.exceptions as exceptions

class Go(Verb):
    """Allows the user to travel between rooms, using their exits."""

    command = _('go ')

    def process(self, message):
        command_length = len(self.command)
        partial_exit_name = message[command_length:]
        origin_room = self.session.repository.get_user_room(self.session.user_id)

        try:
            used_exit_id = services.use_exit(repository=self.session.repository, user_id=self.session.user_id, exit_name=partial_exit_name)
        except exceptions.AmbiguousName:
            self.session.sender.send_to_client(_('There is more than one exit with a similar name. Please be more specific.'))
            return
        except exceptions.TargetNotFound:
            self.session.sender.send_to_client(strings.not_found)
            return
        except exceptions.BadTargetType:
            return
        except exceptions.CantUseClosedExit:
            self.session.sender.send_to_client(_('It is closed.'))
            return

        user = self.session.repository.get_user(self.session.user_id)
        room = self.session.repository.get_user_room(self.session.user_id)
        there_exit = next((exit for exit in self.session.repository.get_exits_in_room(room.id) if exit.destination_id == origin_room.id and not exit.is_hidden()), None)
        used_exit = self.session.repository.get_exit(used_exit_id)

        if not self.session.repository.get_avatar(self.session.user_id, user.current_world_state_id).master_mode:
            if not used_exit.visible == 'hidden':
                self.session.sender.send_to_others_in_room(_("{user_name} leaves through {exit_name}.").format(user_name=user.name, exit_name=used_exit.name))
            else:
                self.session.sender.send_to_others_in_room(_("{user_name} goes to somewhere.").format(user_name=user.name))
            if there_exit:
                self.session.sender.send_to_others_in_room(_("{user_name} arrives through {exit_name}.").format(user_name=user.name, exit_name=there_exit))
            else:
                self.session.sender.send_to_others_in_room(_("{user_name} arrives from somewhere.").format(user_name=user.name))

        Look(self.session).show_current_room()

        self.finish_interaction()
