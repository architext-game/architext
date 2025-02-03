from enum import Enum
from typing import Literal

"""
Visibility values:
 - hidden: The entity can be referenced by verbs but cannot be
 discovered by the "look", "objects" or "items" verbs.
 - unlisted: The entity will be listed by "objects" or "items" verbs,
 but won't be listed in the room description.
 - listed: The entity will be listed by "objects" or "items" verbs,
 and will be listed in the room description.
 - auto: The entity will be listed by "objects" or "items" verbs,
 and will be listed in the room description, unless the entity name
 is present in the room description. This should be the default value.
"""
Visibility = Literal["hidden", "unlisted", "listed", "auto"]