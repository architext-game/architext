# Exceptions related to entities
class BadItem(Exception):
    """Raised when saving an item that does not abide by the item prerequisites"""

class EmptyName(BadItem):
    """Raised when creating an item with an empty name"""

class WrongNameFormat(BadItem):
    """Raised when creating an item with a bad formatted name"""

class RoomNameClash(BadItem):
    """Raised when creating an item with the same name of an exit at the
    same room"""

class TakableItemNameClash(BadItem):
    """Raised when creating an Item or Room that may be unique in their room,
    but may cause problems in other ways. e.g. if there is a takable item with
    that name somewhere else"""

class NameNotGloballyUnique(BadItem):
    """Raised when creating a takable item whose name is already present
    it any item or exit of the world."""

class CantDelete(Exception):
    """Raised when trying to delete something that can't be deleted"""

class ValueWithLineBreaks(Exception):
    """Raised when a value that should not have line breaks has line breaks"""

class ValueTooLong(Exception):
    """Raised when a value exceeds its max length"""