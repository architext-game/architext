from . import verb
import architext.domain.exceptions as domain_exceptions
import architext.strings as strings
from architext.service_layer import goodservices as services
from architext.model.validate_target_name import validate_non_takable_name

class Build(verb.Verb):
    """This verb allows the user to create a new room connected to his current location.
    All the user need to know is the command he should write to start creation. That
    command will start a text wizard that drives him across the creation process.
    """
    command = _('build')
    permissions = verb.PRIVILEGED


    def __init__(self, session):
        super().__init__(session=session)
        self.current_process_function = self.process_first_message

    def process(self, message):
        if message == '/':
            self.session.sender.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        title = _('You start building a new room.')
        body = _('Enter the following fields\n ⚑ Room\'s name')
        out_message = strings.format(title, body, cancel=True)
        self.session.sender.send_to_client(out_message)
        self.current_process_function = self.process_room_name

    def process_room_name(self, message):
        if not message:
            self.session.sender.send_to_client(strings.is_empty)
        else:
            self.new_room_name = message
            self.session.sender.send_to_client(_(' 👁 Description  [default "{default_description}"]').format(default_description=strings.default_description))
            self.current_process_function = self.process_room_description

    def process_room_description(self, message):
        self.this_room = self.session.repository.get_user_room(self.session.user_id)
        new_room = self.new_room_name
        self.new_room_description = message
        self.session.sender.send_to_client(
            _(' ⮕ Name of the exit in "{this_room}" towards "{new_room}"\n   [Default: "to {new_room}"]')
                .format(this_room=self.this_room.name, new_room=new_room)
        )
        self.current_process_function = self.process_here_exit_name

    def process_here_exit_name(self, message):
        if not message:
            message = _("to {room_name}").format(room_name=self.new_room_name)
            message = self.make_exit_name_valid(message, 'placeholder')

        self.entrance_name = message
        try:
            validate_non_takable_name(
                name=self.entrance_name,
                others_in_room=self.session.repository.get_target_names_in_room(self.this_room.id),
                takables_in_world=self.session.repository.get_takable_item_names_in_world_state(self.this_room.world_state_id)
            )
        except domain_exceptions.WrongNameFormat:
            self.session.sender.send_to_client(strings.wrong_format)
        except domain_exceptions.RoomNameClash:
            self.session.sender.send_to_client(strings.room_name_clash)
        except domain_exceptions.TakableItemNameClash:
            self.session.sender.send_to_client(strings.takable_name_clash)
        else:
            self.session.sender.send_to_client(
                _(' ⮕ Name of the exit in "{new_room}" towards "{this_room}"\n   [Default: "to {this_room}"]')
                    .format(new_room = self.new_room_name, this_room = self.this_room.name)
            )
            self.current_process_function = self.process_there_exit_name

    def process_there_exit_name(self, message):
        if not message:
            message = _("to {room_name}").format(room_name=self.this_room.name)
            message = self.make_exit_name_valid(message, 'placeholder')

        self.exit_name = message

        try:
            validate_non_takable_name(
                name=self.entrance_name,
                others_in_room=[],
                takables_in_world=self.session.repository.get_takable_item_names_in_world_state(self.this_room.world_state_id)
            )
        except domain_exceptions.WrongNameFormat:
            self.session.sender.send_to_client(strings.wrong_format)
        except domain_exceptions.TakableItemNameClash:
            self.session.sender.send_to_client(strings.takable_name_clash)
        else:
            services.create_connected_room(
                name=self.new_room_name,
                description=self.new_room_description,
                exit_name=self.exit_name,
                entrance_name=self.entrance_name,
                exit_room_id=self.this_room.id,
                user_id=self.session.user_id,
                repository=self.session.repository,
            )

            self.session.sender.send_to_client(_("Your new room is ready. Good work!"))
            avatar = self.session.repository.get_avatar(self.session.user_id, self.this_room.world_state_id)
            user = self.session.repository.get_user(self.session.user_id)
            if not avatar.master_mode:
                self.session.sender.send_to_others_in_room(
                    _("{user_name}'s eyes turn blank for a moment. A new exit appears in this room.")
                        .format(user_name=user.name)
                )
            self.finish_interaction()

    def make_exit_name_valid(self, exit_name, room_id: str):
        return exit_name
