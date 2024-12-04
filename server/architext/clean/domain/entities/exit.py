from typing import List, Optional, Literal
from dataclasses import dataclass, field

@dataclass
class Exit:
    name: str
    destination_room_id: str
    description: str
    visibility: Literal['listed', 'hidden', 'obvious']
    is_open: bool
    key_names: List[str] = field(default_factory=list)

    def add_key(self, item_name):
        self.key_names.append(item_name)
        self.save()

    def remove_key(self, item_name):
        self.key_names.remove(item_name)
        self.save()

    def open(self):
        self.is_open = True
        self.save()

    def close(self):
        self.is_open = False
        self.save()

    def is_obvious(self):
        return self.visible == 'obvious'

    def is_listed(self):
        return self.visible == 'listed'

    def is_hidden(self):
        return self.visible == 'hidden'
