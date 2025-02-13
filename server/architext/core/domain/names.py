from typing import List, Union
import unicodedata
import re

from architext.core.domain.entities.item import Item
from architext.core.domain.entities.exit import Exit


def normalize(name: str) -> str:
    name = name.lower()
    name = ''.join(c for c in unicodedata.normalize('NFKD', name) if unicodedata.category(c) != 'Mn')
    return name

def equal(name_a: str, name_b: str) -> bool:
    return normalize(name_a) == normalize(name_b)

def substring(substring: str, name: str) -> bool:
    return normalize(substring) in normalize(name)

def complete_words_substring_greater_than_35_percent(substring: str, name: str) -> bool:
    words_substring = re.findall(r'\b\w+\b', substring.lower())
    words_name = re.findall(r'\b\w+\b', name.lower())
    
    pattern = r'\b' + r'\s+'.join(words_substring) + r'\b'
    
    total_chars_substring = sum(len(word) for word in words_substring)
    total_chars_name = sum(len(word) for word in words_name)
    
    if total_chars_substring / total_chars_name < 0.35:
        return False
    
    return re.search(pattern, name.lower()) is not None

def complete_name_match(name: str, things: List[Union[Item, Exit]]):
    match = next((thing for thing in things if equal(thing.name, name)), None)
    return match

def visible_name_match(name: str, things: List[Union[Item, Exit]]):
    matches = [thing for thing in things if substring(name, thing.name) and thing.visibility != "hidden"]
    return matches

def hidden_name_match(name: str, things: List[Union[Item, Exit]]):
    matches = [thing for thing in things if complete_words_substring_greater_than_35_percent(name, thing.name)]
    return matches

def duplicates(strings: List[str]) -> bool:
    normalized_strings = [normalize(string) for string in strings]
    there_are_duplicates = len(normalized_strings) != len(set(normalized_strings))
    return there_are_duplicates