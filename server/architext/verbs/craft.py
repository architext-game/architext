from . import verb
from .. import entities
from .. import util
import architext.strings as strings
import architext.service_layer.services as services

class Craft(verb.Verb):
    """This verb allows users to create items that are placed in their current room"""

    command      = _('craft')
    save_command = _('craftsaved')
    permissions = verb.PRIVILEGED

    def __init__(self, session):
        super().__init__(session)
        self.current_process_function = self.process_first_message
        self.save_create = False  # if true, the item will be saved and not placed in the room.

    def process(self, message):
        if message == '/':
            self.session.send_to_client(strings.cancelled)
            self.finish_interaction()
        else:
            self.current_process_function(message)

    def process_first_message(self, message):
        if message == self.save_command:
            self.save_create = True
            title = _("You are save-crafting an item.")
            body = _(
                "It won't be created at this room but as a saved item that you'll be able to spawn later.\n"
                "\n"
                "Enter the following fields\n"
                " ⚑ Item's name"
            )
        else:
            title = _("You start crafting an item")
            body = _("Enter the following fields\n ⚑ Item's name")
        
        out_message = strings.format(title, body, cancel=True)
        self.session.send_to_client(out_message)
        self.current_process_function = self.process_item_name

    def process_item_name(self, message):
        self.new_item_name = message
        try:
            pass  # self.new_item.ensure_i_am_valid()
        except entities.EmptyName:
            self.session.send_to_client(strings.is_empty)
        except entities.WrongNameFormat:
            self.session.send_to_client(strings.wrong_format)
        except entities.RoomNameClash:
            self.session.send_to_client(strings.room_name_clash)
        except entities.TakableItemNameClash:
            self.session.send_to_client(strings.takable_name_clash)
        else:
            self.session.send_to_client(_(' 👁 Description  [default "{default_description}"]').format(default_description=strings.default_description))
            self.current_process_function = self.process_item_description
 
    def process_item_description(self, message):
        self.new_item_description = message
        self.session.send_to_client(_(
            ' 🔍 Visibility\n'
            ' Write:\n'
            ) +
            strings.visibility_list
            )
        self.current_process_function = self.process_visibility

    def process_visibility(self, message):
        if message.lower() in strings.visible_input_options:
            self.new_item_visible = 'obvious'
        elif message.lower() in strings.listed_input_options:
            self.new_item_visible = 'listed'
        elif message.lower() in strings.hidden_input_options:
            self.new_item_visible = 'hidden'
        elif message.lower() in strings.takable_input_options:
            self.new_item_visible = 'takable'
        else:
            self.session.send_to_client(_('Answer "listed", "visible", "hidden" or "takable.'))
            return

        if self.save_create:
            self.new_item_saved_in = self.session.user.room.world_state
            self.new_item_room = None

        services.create_item(
            session=self.session, 
            name=self.new_item_name,
            description=self.new_item_description,
            room_id=self.session.user.room.id if not self.save_create else None,
            visibility=self.new_item_visible,
            world_state_id=self.new_item_saved_in.id if self.save_create else None
        )

        try:
            pass  # self.new_item.save()
        except entities.NameNotGloballyUnique:
            self.session.send_to_client(_("There is an item or exit with that name in this world. Takable items need an unique name. Choose another visibility or start over to choose another name."))
        else:
            self.session.send_to_client(_("Item crafted!"))
            if not self.session.user.master_mode:
                self.session.send_to_others_in_room(_("{user_name} has crafted something here.").format(user_name=self.session.user.name))
            self.finish_interaction()
