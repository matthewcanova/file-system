import math

from file_system.file_system_entities import Root, Drive, Folder, Zip, Text
from file_system.exceptions import IllegalFileSystemOperation, PathAlreadyExists, PathNotFound, NotATextFile
from file_system.file_system_helpers import path_parse, print_recursive


class FileSystem:

    """
    There is only 1 Root and it can contain zero to many Drives.
    A folder, driver, or zip file, may contain zero to many other folders, or files (text or zip).
    A text file does not contain any other entity (leaf nodes only).
    A drive is not contained in any entity (root only).
    Any non-drive entity, must be contained in another entity (non-root only).
    If A contains B then A is the parent of B.
    """

    def __init__(self):

        self._root = Root('root', 'root', '')

    def create(self, entity_type, name, path_of_parent):
        """
        Creates a new entity under the target parent
        """

        roots = [None, '', '\\', 'root']  # possible paths for root

        if path_of_parent in roots:
            path_of_parent = ''

        # validate target path exists and find the target parent entity
        try:
            target_parent = self.get_entity_at_path(path_of_parent)
        except Exception:
            raise

        # check that target parent doesn't already contain an entity with the same name
        if name in target_parent.get_names():
            raise PathAlreadyExists('An entity with that name already exists in ' + path_of_parent)

        # concatenate the path of the new entity
        if target_parent.path == '':
            new_path = name
        else:
            new_path = '{current_path}\\{name}'.format(current_path=target_parent.path, name=name)

        # create new entity
        try:
            if entity_type == 'drive':
                new_entity = Drive(entity_type, name, new_path)
            elif entity_type == 'folder':
                new_entity = Folder(entity_type, name, new_path)
            elif entity_type == 'zip':
                new_entity = Zip(entity_type, name, new_path)
            elif entity_type == 'text':
                new_entity = Text(entity_type, name, new_path)
            else:
                raise IllegalFileSystemOperation('Invalid entity_type: ' + entity_type)
        except Exception:
            raise

        # add new entity to it's target parent
        target_parent.add_child(new_entity)

        return new_entity

    def delete(self, path):
        """
        Deletes an existing entry
        """

        # validate target path and find the target parent entity
        target_path = path_parse(path)
        base_path = target_path[:-1]
        name = target_path[-1]

        try:
            parent = self.get_entity_at_path('\\'.join(base_path))
        except Exception:
            raise

        # decrement the sizes of ancestors
        self.update_sizes(parent.path, (parent.get_child(name).size * -1))

        parent.delete_child(name)

    def move(self, source_path, destination_path):
        """
        Change the parent of an entity
        """

        # find source parent and child
        target_path = path_parse(source_path)
        source_parent_path = '\\'.join(target_path[:-1])
        source_child = target_path[-1]

        try:
            source_parent = self.get_entity_at_path(source_parent_path)
        except Exception:
            raise

        # find destination entity
        try:
            destination_entity = self.get_entity_at_path(destination_path)
        except Exception:
            raise

        # if the destination does not already contain an entity of the source's name, move it.
        if source_child not in destination_entity.get_names():
            source_child = source_parent.get_child(source_child)

            self.update_sizes(source_parent.path, (source_child.size * -1))  # decrement sizes of sources ancestors
            self.update_sizes(destination_entity.path, source_child.size)  # increment sizes of destinations ancestors

            # add reference to child at destination, delete reference at source.
            destination_entity.add_child(source_parent.get_child(source_child))
            source_parent.delete_child(source_child)
        else:
            raise PathAlreadyExists('Destination already has an entity with the source\'s name')

    def write_to_file(self, path, content):
        """
        Change the content of a text file
        """

        # find target entity
        try:
            file = self.get_entity_at_path(path)
        except Exception:
            raise

        if file.entity_type != 'text':
            raise NotATextFile('Cannot write content to a non-text entity')
        else:
            size_delta = len(content) - len(file.content)
            file.content = content
            self.update_sizes(path, size_delta)

    def get_entity_at_path(self, path):

        current_entity = self._root

        path_list = path_parse(path)
        for entity in path_list:
            if entity in current_entity.get_names():
                current_entity = current_entity.get_child(entity)
            else:
                raise PathNotFound('Invalid target path')

        return current_entity

    def update_sizes(self, path, size):

        path_list = path_parse(path)
        self.recurse_sizes(path_list, self._root, size)

    def recurse_sizes(self, path, current, size):

        new_current = current.get_child(path[0])
        if len(path) == 1:
            new_current.size += size
            return size
        elif new_current.entity_type != 'zip':
            new_size = self.recurse_sizes(path[1:], new_current, size)
            new_current.size += new_size
            return new_size
        else:
            new_size = self.recurse_sizes(path[1:], new_current, size)
            compressed_size = math.ceil(new_size/2.0)
            new_current.size += compressed_size
            return compressed_size

    def print_file_system(self):

        print_recursive(self._root)
