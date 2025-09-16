from dataclasses import dataclass
from architext.core.application.commands.base import Command


@dataclass
class DeleteTemplateResult:
    pass

class DeleteTemplate(Command[DeleteTemplateResult]):
    template_id: str 