
###################
# HELPER FUNCTIONS
###################


def path_parse(path):
    """
    Guarantees no leading or trailing \s and no blank entries in the path list
    Returns a parsed list of the path entities
    """

    split_path = path.split('\\')
    split_path = [entity for entity in split_path if entity != '']

    return split_path


def print_recursive(entity):
    """
    Recursively prints an entity and its children
    """

    string = entity.name + ' ' + str(entity.size) + '\n'

    if entity.entity_type != 'text':
        for entity_name in entity.get_names():
            string += print_recursive(entity.get_child(entity_name))

    return string
