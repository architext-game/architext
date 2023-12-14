from . import verb
from .. import util
from .. import entities
import architext.strings as strings

class Connect(verb.Verb):
    """This verb allow users to connect two existing rooms. One is the room where the user is located,
    The other room is specified through its alias"""

    command = _('link')
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.other_room = None
        self.exit_from_here = entities.Exit(room=self.session.user.room, save_on_creation=False)
        self.exit_from_there = entities.Exit(destination=self.session.user.room, save_on_creation=False)
        self.current_process_function = self.process_first_message
    
    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        title = _('Linking from {user_room_name} (number {user_room_alias}).').format(
            user_room_name=self.session.user.room.name, 
            user_room_alias=self.session.user.room.alias
        )
        body = _(
            'You are about to create an exit in your current room.\n'
            'Enter the number of the room you want to connect it to (you can check it using the "info" verb).\n\n'
            'Destination room number:'
        )
        self.session.send_formatted(title, body, cancel=True)
        self.current_process_function = self.process_room_alias

    def process_room_alias(self, message):
        if not message:
            self.session.send_to_client(strings.is_empty)
        elif entities.Room.objects(alias=message, world_state=self.session.user.room.world_state):
            self.other_room = entities.Room.objects(alias=message, world_state=self.session.user.room.world_state).first()
            self.exit_from_here.destination = self.other_room
            self.exit_from_there.room = self.other_room
            out_message = _(
                'Linking with "{destination_name}" (number {destination_alias}).\n'
                '  ⮕ Enter the name of the exit in {this_room_name} (number {this_room_alias}) towards {destination_name} (number {destination_alias})\n'
                '[Default: to {destination_name}]'
            ).format(destination_name=self.other_room.name, destination_alias=self.other_room.alias, this_room_name=self.session.user.room.name, this_room_alias=self.session.user.room.alias)
            self.session.send_to_client(out_message)
            self.current_process_function = self.process_here_exit_name
        else:
            self.session.send_to_client(strings.room_not_found)

    def process_here_exit_name(self, message):
        if not message:
            message = _("to {destination_name}").format(destination_name=self.other_room.name)
            message = self.make_exit_name_valid(message, self.session.user.room)

        self.exit_from_here.name = message
        
        try:
            self.exit_from_here.ensure_i_am_valid()
        except entities.WrongNameFormat:
            self.session.send_to_client(strings.wrong_format)
        except entities.RoomNameClash:
            self.session.send_to_client(strings.room_name_clash)
        except entities.TakableItemNameClash:
            self.session.send_to_client(strings.takable_name_clash)
        else:
            out_message = _(
                '  ⮕ Enter the name of the exit in {destination_name} (number {destination_alias}) towards {this_room_name} (number {this_room_alias})\n'
                '[Default: to {this_room_name}]'
            ).format(destination_name=self.other_room.name, destination_alias=self.other_room.alias, this_room_name=self.session.user.room.name, this_room_alias=self.session.user.room.alias)
            
            self.session.send_to_client(out_message)
            self.current_process_function = self.process_there_exit_name

    def process_there_exit_name(self, message):
        if not message:
            message = _("to {destination_name}").format(destination_name=self.session.user.room.name)
            message = self.make_exit_name_valid(message, self.other_room)

        self.exit_from_there.name = message

        try:
            self.exit_from_there.ensure_i_am_valid()
        except entities.WrongNameFormat:
            self.session.send_to_client(strings.wrong_format)
        except entities.RoomNameClash:
            self.session.send_to_client(strings.room_name_clash)
        except entities.TakableItemNameClash:
            self.session.send_to_client(strings.takable_name_clash)
        else:
            self.exit_from_here.destination = self.other_room
            self.exit_from_there.room = self.other_room
            self.exit_from_here.save()
            self.exit_from_there.save()
            self.session.send_to_client(_("Your new exits are ready!"))
            if not self.session.user.master_mode:
                self.session.send_to_others_in_room(
                    _("{user_name}'s eyes turn blank for a moment. A new exit appears in this room.")
                        .format(user_name=self.session.user.name)
                )
            self.finish_interaction()

    def make_exit_name_valid(self, exit_name, room):
        while not entities.Exit.name_is_valid(exit_name, room):
            exit_name = _('straight {exit_name}').format(exit_name=exit_name)
        return exit_name
