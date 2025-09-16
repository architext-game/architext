from dataclasses import dataclass
from architext.core.application.commands.base import Command
from pydantic import Field
from typing import Literal
from architext.core.application.settings import SOCIAL_INTERACTION_MAX_LENGTH


@dataclass
class SendSocialInteractionResult:
    pass

class SendSocialInteraction(Command[SendSocialInteractionResult]):
    content: str = Field(min_length=1, max_length=SOCIAL_INTERACTION_MAX_LENGTH)
    type: Literal['talk', 'emote'] 