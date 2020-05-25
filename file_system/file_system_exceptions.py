
class IllegalFileSystemOperation(Exception):
    """
    Violates specifications of the file system
    """
    pass


class PathNotFound(Exception):
    """
    An invalid path was provided
    """
    pass


class PathAlreadyExists(Exception):
    """
    An existing path was provided where one was not expected
    """
    pass


class NotATextFile(Exception):
    """
    Expected an entity of type 'text'
    """
    pass
