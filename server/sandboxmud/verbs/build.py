from . import verb
from .. import entities
from .. import util
import sandboxmud.strings as strings

class Build(verb.Verb):
    """This verb allows the user to create a new room connected to his current location.
    All the user need to know is the command he should write to start creation. That
    command will start a text wizard that drives him across the creation process.
    """
    command = _('build')
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.new_room = entities.Room(save_on_creation=False, world_state=self.session.user.room.world_state)
        self.exit_from_here = entities.Exit(destination=self.new_room, room=self.session.user.room, save_on_creation=False)
        self.exit_from_there = entities.Exit(destination=self.session.user.room, room=self.new_room, save_on_creation=False)
        self.current_process_function = self.process_first_message

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancel_prompt)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        title = _('You start building a new room.')
        body = _('Enter the following fields\n ⚑ Room\'s name')
        out_message = strings.format(title, body, cancel=True)
        self.session.send_to_client(out_message)
        self.current_process_function = self.process_room_name

    def process_room_name(self, message):
        if not message:
            self.session.send_to_client(strings.is_empty)
        else:
            self.new_room.name = message
            self.session.send_to_client(_(' 👁 Description  [default "{default_description}"]').format(default_description=strings.default_description))
            self.current_process_function = self.process_room_description

    def process_room_description(self, message):
        this_room = self.session.user.room.name
        new_room = self.new_room.name
        self.new_room.description = message
        self.session.send_to_client(
            _(' ⮕ Name of the exit in "{this_room}" towards "{new_room}"\n   [Default: "to {new_room}"]')
                .format(this_room=this_room, new_room=new_room)
        )
        self.current_process_function = self.process_here_exit_name

    def process_here_exit_name(self, message):
        if not message:
            message = "a {}".format(self.new_room.name)
            message = self.make_exit_name_valid(message, self.session.user.room)

        self.exit_from_here.name = message
        try:
            self.exit_from_here.ensure_i_am_valid()
        except entities.WrongNameFormat:
            self.session.send_to_client(strings.wrong_format)
        except entities.RoomNameClash:
            self.session.send_to_client(srings.room_name_clash)
        except entities.TakableItemNameClash:
            self.session.send_to_client(strings.takable_name_clash)
        else:
            self.session.send_to_client(
                _(' ⮕ Name of the exit in "{new_room}" towards "{this_room}"\n   [Default: "to {this_room}"]')
                    .format(new_room = self.new_room.name, this_room = self.session.user.room.name)
            )
            self.current_process_function = self.process_there_exit_name

    def process_there_exit_name(self, message):
        if not message:
            message = _("to {room_name}").format(room_name=self.session.user.room.name)
            message = self.make_exit_name_valid(message, self.new_room)  

        self.exit_from_there.name = message
        
        try:
            self.exit_from_there.ensure_i_am_valid()
        except entities.WrongNameFormat:
            self.session.send_to_client(strings.wrong_format)
        except entities.TakableItemNameClash:
            self.session.send_to_client(strings.takable_name_clash)
        else:
            self.new_room.save()
            self.exit_from_here.save()
            self.exit_from_there.save()

            self.session.send_to_client(_("Your new room is ready. Good work!"))
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

    def cancel():
        self.session.user.room.exits.remove(self.exit_from_here)