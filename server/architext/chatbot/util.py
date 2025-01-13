import logging
import os
import re
import io
import regex
import json
import unicodedata
import json, zlib, base64, binascii
import typing


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

        if "world_users" in loose_match:
            target_user = next(entities.User.objects(name=name, room__ne=None, client_id__ne=None), None)
            if target_user and target_user.room.world_state == session.user.room.world_state:
                return target_user

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

def get_config():
    with io.open('config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config


def create_world(user, world=typing.Literal['riddle', 'tutorial'], public=False):
    locale = get_config()['locale']
    if world == 'riddle':
        if locale == 'es_ES':
            filename = './architext/resources/monks_riddle_es.json'
            world_name = "El Enigma del Monasterio"
        else:
            filename = './architext/resources/monks_riddle_en.json'
            world_name = "The Monk's Riddle"
    elif world == 'tutorial':
        if locale == 'es_ES':
            filename = './architext/resources/museum_es.json'
            world_name = "El Museo de Arquitextura"
        else:
            filename = './architext/resources/museum_en.json'
            world_name = "The Museum of Architexture"

    with open(filename, 'r') as file:
        # remove_control_characters
        world_dict = json.load(file)
    return world_from_dict(world_dict, world_name, user, public)

def match(pattern, string):
    """
    Checkes one or more regex patterns against a given string.
    For a match to ocurr, the string must fully match the pattern (see Python's
    re.Pattern.fullmatch function docs for more info.)

    Parameters
    ----------
    patterns : str or [str]
        A single regex pattern or a list of patterns to check.
    string : str
        The string to be checked.
    
    Returns
    -------
    A dict that contains the result of the re.Match.groupdict function
    for the first matching pattern in the list, containing the name and
    values of named subgroups. Also contains a 'pattern' key containing the 
    matched regular expression. If the expression contained a 'pattern' named 
    subgroup, it value in the dict will be overwritten.
    If there is no match, returns None.

    If the regex contained a repeating named pattern and there is more than
    one match for that group, its key will contain a list with all the 
    matches.
    """
    if type(pattern) != list:
        pattern = [pattern]
    
    for p in pattern:
        compiled_pattern = regex.compile(p)
        the_match = compiled_pattern.fullmatch(string)
        
        if the_match is not None:
            capturesdict = the_match.capturesdict()

            for group in capturesdict:
                if len(capturesdict[group]) == 1:
                    capturesdict[group] = capturesdict[group][0]
                elif len(capturesdict[group]) == 0:
                    capturesdict[group] = None

            capturesdict['pattern'] = p

            return capturesdict

    return None
 

def world_from_dict(world_dict, world_name, creator, public=False):
    
    new_world_state = entities.WorldState(save_on_creation=False)
    new_world = entities.World(save_on_creation=False, name=world_name, creator=creator, world_state=new_world_state, public=public)
    
    items = []
    custom_verbs = []
    exits = []
    other_rooms = []
    inventories = []
    saved_items = []

    new_world_state.starting_room, added_items = room_from_dict(world_dict['starting_room'])
    items += added_items

    for room_dict in world_dict['other_rooms']:
        room, added_items = room_from_dict(room_dict, world_state=new_world_state)
        other_rooms.append(room)
        items += added_items
    
    for verb_dict in world_dict['custom_verbs']:
        custom_verbs.append(custom_verb_from_dict(verb_dict))

    all_rooms = other_rooms + [new_world_state.starting_room]
    rooms_dict_by_alias = { room.alias: room for room in all_rooms }
    for exit_dict in world_dict['exits']:
        new_exit = exit_from_dict(exit_dict, rooms_dict_by_alias)
        exits.append(new_exit)

    creator_inventory = inventory_from_dict(item_list=world_dict['inventory'], user=creator, world_state=new_world_state)
    inventories.append(creator_inventory)

    for item_dict in world_dict['saved_items']:
        new_item = item_from_dict(item_dict, saved_in=new_world_state)
        saved_items.append(new_item)

    new_world_state._next_room_id = world_dict['next_room_id']

    # todo: save all in the correct order
    # save all entities that world_state references
    for verb in new_world_state.starting_room.custom_verbs:
        verb.save()
    new_world_state.starting_room.save()
    for verb in custom_verbs:
        verb.save()
    new_world_state.custom_verbs = custom_verbs
    # now the world state can be saved
    new_world_state.save()
    # now we can add the world_state reference to the starting room
    new_world_state.starting_room.world_state = new_world_state
    new_world_state.starting_room.save()
    # and save the saved items
    for item in saved_items:
        for verb in item.custom_verbs:
            verb.save()
        item.save()
    # now we can save the rest of the rooms
    for room in other_rooms:
        for verb in room.custom_verbs:
            verb.save()
        room.save()
    # now we can save the exits and items
    for exit in exits:
        exit.save()
    for item in items:
        for verb in item.custom_verbs:
            verb.save()
        item.save()
    # we finally save the inventories
    for inventory in inventories:
        for item in inventory.items:
            for verb in item.custom_verbs:
                verb.save()
            item.save()
        inventory.save()
    # and the world itself
    new_world.save()
    return new_world
    


def room_from_dict(room_dict, world_state=None):
    custom_verbs = [custom_verb_from_dict(verb_dict) for verb_dict in room_dict['custom_verbs']]

    new_room = entities.Room(
        save_on_creation=False, 
        world_state=world_state,
        name=room_dict['name'],
        alias=room_dict['alias'],
        description=room_dict['description'],
        custom_verbs=custom_verbs
    )

    items = []
    for item_dict in room_dict['items']:
        new_item = item_from_dict(item_dict, room=new_room)
        items.append(new_item)
    return new_room, items

def item_from_dict(item_dict, room=None, saved_in=None):
    custom_verbs = [custom_verb_from_dict(verb_dict) for verb_dict in item_dict['custom_verbs']]
    
    new_item = entities.Item(
        save_on_creation=False,
        item_id=item_dict['item_id'],
        name=item_dict['name'],
        description=item_dict['description'],
        visible=item_dict['visible'],
        custom_verbs=custom_verbs,
        room=room,
        saved_in=saved_in
    )

    return new_item

def custom_verb_from_dict(verb_dict):
    custom_verb = entities.CustomVerb(
        save_on_creation=False, 
        names=verb_dict["names"],
        commands=verb_dict["commands"]
    )
    return custom_verb

def exit_from_dict(exit_dict, rooms_dict_by_alias):
    room_alias = exit_dict["room"]
    destination_alias = exit_dict["destination"]
    room = rooms_dict_by_alias[room_alias]
    destination = rooms_dict_by_alias[destination_alias]
    
    new_exit=entities.Exit(
        save_on_creation=False,
        name=exit_dict["name"],
        description=exit_dict["description"],
        destination=destination,
        room=room,
        visible=exit_dict['visible'],
        is_open=exit_dict['is_open'],
        key_names=exit_dict['key_names'],
    )

    return new_exit

def inventory_from_dict(item_list, user, world_state):
    items = []
    for item_dict in item_list:
        new_item = item_from_dict(item_dict)
        items.append(new_item)
    
    new_inventory = entities.Inventory(
        save_on_creation=False,
        user=user,
        world_state=world_state,
        items=items
    )

    return new_inventory


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def encode_dict(dict):
    json_string = json.dumps(dict)
    bytes = json_string.encode('utf-8')
    compressed_bytes = zlib.compress(bytes)
    b64bytes = base64.b64encode(compressed_bytes)
    b64string = b64bytes.decode()
    return b64string

def decode_dict(encoded_str):
    compresed_b64bytes = base64.b64decode(encoded_str)
    b64bytes = zlib.decompress(compresed_b64bytes)
    json_str = b64bytes.decode()
    dict = json.loads(json_str)
    return dict

def text_to_world_dict(text):
    world_dict = None

    # the message may be encoded or not, so we try both ways
    try:
        world_dict = json.loads(text)
    except json.decoder.JSONDecodeError:
        try:
            world_dict = decode_dict(text)
        except (binascii.Error, zlib.error, ValueError, json.decoder.JSONDecodeError):
            'the message is not valid'

    return world_dict
