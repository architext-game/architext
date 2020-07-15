def possible_meanings(partial_string, list_of_options):
    if partial_string in list_of_options:
        return [string for string in list_of_options if partial_string == string]
    else:
        return [string for string in list_of_options if partial_string in string]
