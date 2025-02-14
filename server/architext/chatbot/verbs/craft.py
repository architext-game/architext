from gettext import gettext as _

from typing import Literal, Optional, TYPE_CHECKING

from architext.core.commands import CreateItem
from architext.core.domain.primitives import Visibility
from architext.core.queries.is_name_valid import IsNameValid
from architext.core.settings import ITEM_DESCRIPTION_MAX_LENGTH, ITEM_NAME_MAX_LENGTH

from . import verb
import architext.chatbot.strings as strings
from dataclasses import dataclass

if TYPE_CHECKING:
    from architext.chatbot.session import Session
else:
    Session = object()

@dataclass
class UserInput():
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[Visibility] = None
    

class Craft(verb.Verb):
    """This verb allows the user to create a new room connected to his current location.
    All the user need to know is the command he should write to start creation. That
    command will start a text wizard that drives him across the creation process.
    """
    command = _('craft')
    privileges_requirement = 'owner'

    def setup(self) -> None:
        self.user_input = UserInput()
        self.state: Literal[
            'start', 
            'expect_name', 
            'expect_description', 
            'expect_visibility',
        ] = 'start'

    def process(self, message: str):
        if message == '/':
            self.session.sender.send(self.session.user_id, strings.cancelled)
            self.finish_interaction()

        elif self.state == 'start':
            title = _("You start crafting an item")
            body = _("Enter the following fields\n ⚑ Item's name")
            self.session.sender.send_formatted(self.session.user_id, title, body, cancel=True)
            self.state = 'expect_name'

        elif self.state == 'expect_name':
            if not message:
                self.session.sender.send(self.session.user_id, strings.is_empty)
            elif len(message) > ITEM_NAME_MAX_LENGTH:
                self.session.sender.send(self.session.user_id, strings.too_long.format(limit=ITEM_NAME_MAX_LENGTH))
            elif self.architext.query(IsNameValid(name=message), self.session.user_id).error == 'duplicated':
                self.session.sender.send(self.session.user_id, strings.room_name_clash)
            else:
                self.user_input.name = message
                self.session.sender.send(self.session.user_id, _(' 👁 Description  [default "{default_description}"]').format(default_description=strings.default_description))
                self.state = 'expect_description'

        elif self.state == 'expect_description':
            if not message:
                message = strings.default_description
            if len(message) > ITEM_DESCRIPTION_MAX_LENGTH:
                self.session.sender.send(self.session.user_id, strings.too_long.format(limit=ITEM_DESCRIPTION_MAX_LENGTH))
            else:
                self.user_input.description = message
                self.session.sender.send(self.session.user_id, 
                    _(
                        ' 🔍 Visibility\n'
                        ' Write:\n'
                    ) + strings.visibility_list
                )
                self.state = 'expect_visibility'

        elif self.state == 'expect_visibility':
            if message.lower() in strings.unlisted_input_options:
                self.user_input.visibility = "unlisted"
            if message.lower() in strings.auto_input_options:
                self.user_input.visibility = "auto"
            elif message.lower() in strings.listed_input_options:
                self.user_input.visibility = "listed"
            elif message.lower() in strings.hidden_input_options:
                self.user_input.visibility = "hidden"
            else:
                self.session.sender.send(self.session.user_id, strings.wrong_value)
                return
            
            self.architext.handle(CreateItem(
                name=self.user_input.name,
                description=self.user_input.description,
                visibility=self.user_input.visibility,
            ), self.session.user_id)

            self.session.sender.send(self.session.user_id, _("Your new item is ready. Good work!"))
            # if not self.session.user.master_mode:
            #     self.session.send_to_others_in_room(
            #         _("{user_name}'s eyes turn blank for a moment. A new item appears in this room.")
            #             .format(user_name=self.session.user.name)
            #     )
            self.finish_interaction()
