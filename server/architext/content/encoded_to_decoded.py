from architext.content.new_tutorial import NEW_TUTORIAL_ENCODED
from architext.core.application.event_handlers.import_world import decode_text
import pprint
import json

text = NEW_TUTORIAL_ENCODED

print(json.dumps(json.loads(decode_text(text)), indent=2, ensure_ascii=False))