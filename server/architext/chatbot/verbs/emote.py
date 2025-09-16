from gettext import gettext as _

from .verb import Verb

from architext.core.application.commands import SendSocialInteraction

class Emote(Verb):
    command = _('me ')

    def process(self, message: str):
        command_length = len(self.command)
        content = message[command_length:]
        
        self.architext.handle(SendSocialInteraction(
            type='emote',
            content=content,
        ), self.session.user_id)

        self.finish_interaction()
