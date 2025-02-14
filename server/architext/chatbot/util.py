import logging
import os
import re
import io
import regex
import json
import unicodedata
import json, zlib, base64, binascii
import typing

from architext.core.queries.get_room_details import ExitInRoomDetails, RoomDetails, ItemInRoomDetails


# username to be used by the ghost session (see ghost_session.py)
GHOST_USER_NAME = "-nadie-"

class ThingWithName(typing.Protocol):
    name: str

T = typing.TypeVar("T", bound=ThingWithName)
def get_by_name(name: str, list: typing.List[T]) -> T:
    return next((item for item in list if item.name == name))


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
