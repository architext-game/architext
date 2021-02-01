from .. import entities
from .. import util
from .verb import Verb

class CustomVerb(Verb):
    command = None

    @classmethod
    def can_process(cls, message, session):
        '''true if any custom verb corresponds to the message'''
        return cls.search_for_custom_verb(message, session) is not None

    @classmethod
    def search_for_custom_verb(cls, message, session):
        if len(message.split(" ", 1)) == 2:  # if the message has the form "verb item"
            target_verb_name, target_item_name = message.split(" ", 1)
            candidate_items = session.user.room.items + session.user.inventory
            items_they_may_be_referring_to = util.possible_meanings(target_item_name, [i.name for i in candidate_items])
            if len(items_they_may_be_referring_to) == 1:
                target_item_name = items_they_may_be_referring_to[0]
                suitable_item_found = next(filter(lambda i: i.name==target_item_name, candidate_items))
                suitable_verb_found_in_item = next(filter(lambda v: v.is_name(target_verb_name), suitable_item_found.custom_verbs), None)
                if suitable_verb_found_in_item is not None:
                    return suitable_verb_found_in_item
        else:
            suitable_verb_found_in_room = next(filter(lambda v: v.is_name(target_verb_name), session.user.room.custom_verbs), None)
            if suitable_verb_found_in_room is not None:
                return suitable_verb_found_in_room
            world = entities.World.objects[0]
            suitable_verb_found_in_world = next(filter(lambda v: v.is_name(target_verb_name), world.custom_verbs), None)
            if suitable_verb_found_in_world is not None:
                return suitable_verb_found_in_world
        return None

    def __init__(self, session):
        super().__init__(session)
        self.custom_verb_definition = None

    def process(self, message):
        if self.custom_verb_definition is None:
            self.custom_verb_definition = self.search_for_custom_verb(message, self.session)
        if self.custom_verb_definition is None:
            raise Exception('Invalid message passed to verbs.CustomVerb')
        self.execute_custom_verb(self.custom_verb_definition)
        self.finish_interaction()

    def execute_custom_verb(self, custom_verb):
        from .. import session
        ghost = session.GhostSession(self.session.server, self.session.user.room)
        for message in custom_verb.commands:
            formatted_message = self.format_custom_verb_message(message)
            ghost.process_message(formatted_message)
        ghost.disconnect()

    def format_custom_verb_message(self, message):
        message = message.replace('.usuario', self.session.user.name)
        return message