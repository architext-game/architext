import logging
from . import entities
import os
import re

# username to be used by the ghost session (see ghost_session.py)
GHOST_USER_NAME = "-nadie-"

def possible_meanings(partial_string, list_of_options, loose_match=True, substr_match=True):
    # first check for exact matches
    if partial_string in list_of_options:
        return [string for string in list_of_options if partial_string == string]

    # then check for complete easy text matches
    elif loose_match and next(filter(lambda s: similar(s, partial_string), list_of_options), None) is not None:
        return list(filter(lambda s: similar(s, partial_string), list_of_options))

    # then check for easy text containment
    elif substr_match:
        return [string for string in list_of_options if contains_similar(partial_string, string)]

    # if nothing found with the given options, return an empty list
    else:
        return []


def find_name_matches(input_string, items, item_to_string, loose_match=True, substr_match=True):
    """
    Parameters
    ----------
    input_string : str
        a string that refers to someitem, but we don't know which someitem.
    items : list
        a list of the items that input_string may be referring to.
    item_to_string : function (any) => string
        a function that gets a item a return that item's corresponding string (like a name).
    
    Returns
    -------
    the items whose strings are the most similar to the input string, according to the
    possible_meanings function.
    """
    item_strings = [item_to_string(item) for item in items]
    strings_she_refers_to = possible_meanings(input_string, item_strings, loose_match=loose_match, substr_match=substr_match)
    items_she_refers_to = [item for item in items if item_to_string(item) in strings_she_refers_to]
    return items_she_refers_to


def name_to_entity(session, name, loose_match=[], substr_match=[], strict_match=[]):
    """
    Parameters
    ----------
    session: Session
        session that is calling this function, for context.
    name: str
        the function will try to find a entity that matches with this name.
    loose_match: list of str
        list of values specifying where to do a loose match. Loose match ignores
        case and accents. Valid values: "saved_items", "room_items", "room_exits", "inventory".
    substr_match: list of str
        Ignores case, accents and matches with just a substring of the entities name.
        Valid values: "room_items", "room_exits", "inventory".
    strict_macth: list of str
        The name has to be equal (==) to the entity name.
        Valid values: "saved_items", "room_items", "room_exits", "inventory".
    
    Returns
    -------
    The entity that best matches with the name given the other parameters.
    Priority: strict_match before loose_match before substr_match
    If a match is found in one level, the others won't be checked.
    Returns None if no entity matches the name.
    Returns "many" if there are many matches at a given level.
    """

    if strict_match:
        candidates = []
        matches = []

        if "saved_items" in strict_match:
            saved_items = list(entities.Item.objects(room=None, saved_in=session.user.room.world_state))
            matches += find_name_matches(name, saved_items, lambda i: i.item_id, loose_match=False, substr_match=False)

        if "connected_users" in strict_match:
            match = next(entities.User.objects(name=name, client_id__ne=None), None)
            if match is not None:
                matches += [match]

        if "room_items" in strict_match:
            candidates += session.user.room.items

        if "room_exits" in strict_match:
            candidates += session.user.room.exits

        if "inventory" in strict_match:
            candidates += session.user.get_current_world_inventory().items

        matches += find_name_matches(name, candidates, lambda e: e.name, loose_match=False, substr_match=False)

        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            session.send_to_client(str(matches))
            return "many"

    if loose_match:
        # saved items take preference and are evaluated separately
        if "saved_items" in loose_match:
            saved_items = list(entities.Item.objects(room=None, saved_in=session.user.room.world_state))
            matches = find_name_matches(name, saved_items, lambda i: i.item_id, loose_match=True, substr_match=False)
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                return "many"

        if "connected_users" in loose_match:
            connected_users = list(entities.User.objects(client_id__ne=None))
            matches = find_name_matches(name, connected_users, lambda u: u.name, loose_match=True, substr_match=False)
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                return "many"

        if "room_users" in loose_match:
            room_users = list(entities.User.objects(room=session.user.room, client_id__ne=None))
            matches = find_name_matches(name, room_users, lambda u: u.name, loose_match=True, substr_match=False)
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                return "many"

        candidates = []

        if "room_items" in loose_match:
            candidates += session.user.room.items

        if "room_exits" in loose_match:
            candidates += session.user.room.exits
        
        if "inventory" in loose_match:
            candidates += session.user.get_current_world_inventory().items

        matches = find_name_matches(name, candidates, lambda e: e.name, loose_match=True, substr_match=False)

        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            return "many"

    if substr_match:
        candidates = []

        if "room_items" in substr_match:
            candidates += session.user.room.items

        if "room_exits" in substr_match:
            candidates += session.user.room.exits

        if "inventory" in substr_match:
            candidates += session.user.get_current_world_inventory().items

        matches = find_name_matches(name, candidates, lambda e: e.name, loose_match=True, substr_match=True)

        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            return "many"
    
    # no matches found in any level
    return None

def setup_logger(logger_name, log_file, console=False, level=logging.INFO):
    """Sets up a logger that can be used across all modules.
    Example:
        setup_logger('log1', "logs.txt")  # Sets up the logger
        logger_1 = logging.getLogger('log1')  # Gets the logger (works from anywhere)
        logger_1.info('Some info to log')  # logs something
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')

# handler = logging.handlers.RotatingFileHandler(
#              LOG_FILENAME, maxBytes=20, backupCount=5)

    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s: %(message)s')
    fileHandler = logging.FileHandler(os.getcwd() + '/logs/' + log_file, 'a', 'utf-8')
    fileHandler.setFormatter(formatter)
    if console:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)  

    logger.setLevel(level)
    logger.addHandler(fileHandler)
      

    return logger

def fix_string(string, remove_breaks=False, max_length=None):
    if remove_breaks:
        string = string.replace('\n', '')
    if max_length is not None:
        string = string[:max_length]
    return string

def similar(text_one, text_two):
    text_one = easy_text(text_one)
    text_two = easy_text(text_two)

    return text_one == text_two

def contains_similar(substring, bigstring):
    substring = easy_text(substring)
    bigstring = easy_text(bigstring)

    return substring in bigstring

def easy_text(text):
    text = text.lower()
    text = remove_accents(text)
    return text

def remove_accents(text):
    """Removes common accent characters."""

    text = re.sub(u"[àáâãäå]", 'a', text)
    text = re.sub(u"[èéêë]", 'e', text)
    text = re.sub(u"[ìíîï]", 'i', text)
    text = re.sub(u"[òóôõö]", 'o', text)
    text = re.sub(u"[ùúûü]", 'u', text)
    text = re.sub(u"[ýÿ]", 'y', text)
    text = re.sub(u"[ñ]", 'n', text)

    return text 

