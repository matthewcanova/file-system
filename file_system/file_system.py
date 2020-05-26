import math

from file_system.file_system_entities import Root, Drive, Folder, Zip, Text
from file_system.file_system_exceptions import IllegalFileSystemOperation, PathAlreadyExists, PathNotFound, NotATextFile
from file_system.file_system_helpers import path_parse, print_recursive


class FileSystem:

    """
    There is only 1 Root and it can contain zero to many Drives.
    A folder, drive, or zip file, may contain zero to many other folders, or files (text or zip).
    A text file does not contain any other entity (leaf nodes only).
    A drive is not contained in any entity (root only).
    Any non-drive entity, must be contained in another entity (non-root only).
    If A contains B then A is the parent of B.
    """

    def __init__(self):

        self._root = Root('root', 'root', '')

    def __str__(self):
        string = print_recursive(self._root).splitlines()[1:]
        return '\n'.join(string)

    def create(self, entity_type, name, path_of_parent):
        """
        Creates a new entity under the target parent
        :param entity_type root, drive, folder, zip, or text
        :param name string
        :param path_of_parent '\' separated path to target parent, or root identifier if a drive
        :return entity newly created entity
        """

        roots = [None, '', '\\', 'root']  # possible paths for root

        if path_of_parent in roots:
            path_of_parent = ''

        # validate target path exists and find the target parent entity
        try:
            target_parent = self._get_entity_at_path(path_of_parent)
        except Exception:
            raise

        # check that target parent doesn't already contain an entity with the same name
        if name in target_parent.get_names():
            raise PathAlreadyExists('An entity with that name already exists in {}'.format(path_of_parent))

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
                raise IllegalFileSystemOperation('Invalid entity_type: {}'.format(entity_type))
        except Exception:
            raise

        # add new entity to it's target parent
        target_parent.add_child(new_entity)

        return new_entity

    def delete(self, path):
        """
        Deletes an existing entry
        :param path path to the entity to be deleted
        """

        # validate target path and find the target parent entity
        target_path = path_parse(path)
        base_path = '\\'.join(target_path[:-1])
        name = target_path[-1]

        try:
            parent = self._get_entity_at_path(base_path)
        except Exception:
            raise

        # decrement the sizes of ancestors
        self._update_sizes(parent.path, (parent.get_child(name).size * -1))

        # delete child
        parent.delete_child(name)

    def move(self, source_path, destination_path):
        """
        Change the parent of an entity
        :param source_path the path to the entity to be moved
        :param destination_path the parent to move the entity under
        """

        # find source parent and child
        target_path = path_parse(source_path)
        source_parent_path = '\\'.join(target_path[:-1])
        source_child = target_path[-1]

        try:
            source_parent = self._get_entity_at_path(source_parent_path)
        except Exception:
            raise

        # find destination entity
        try:
            destination_entity = self._get_entity_at_path(destination_path)
        except Exception:
            raise

        # if the destination does not already contain an entity of the source's name, move it.
        if source_child not in destination_entity.get_names():
            source_child_entity = source_parent.get_child(source_child)

            self._update_sizes(source_parent.path, (source_child_entity.size * -1))  # dec sizes of sources ancestors
            self._update_sizes(destination_entity.path, source_child_entity.size)  # inc sizes of destinations ancestors

            # add reference to child at destination and update paths
            destination_entity.add_child(source_child_entity)
            source_child_entity.path = destination_entity.path + '\\' + source_child_entity.name
            # delete reference at source and update paths
            source_parent.delete_child(source_child_entity.name)
        else:
            raise PathAlreadyExists('Destination already has an entity with the source\'s name')

    def write_to_file(self, path, content):
        """
        Change the content of a text file
        :param path path to the text file whose content will be written to
        :param content the content that will be written to the text file
        """

        # find target entity
        try:
            file = self._get_entity_at_path(path)
        except Exception:
            raise

        # ensure we are writing to a text entity
        if file.entity_type != 'text':
            raise NotATextFile('Cannot write content to a non-text entity')
        else:
            size_delta = len(content) - len(file.content)  # calculate the delta in size based on the new content
            file.content = content  # update the content
            self._update_sizes(path, size_delta)  # update sizes of all ancestors based on size delta

    def _get_entity_at_path(self, path):
        """
        Given a path string, returns the entity at the path
        """

        current_entity = self._root

        path_list = path_parse(path)
        for entity in path_list:
            if entity in current_entity.get_names():
                current_entity = current_entity.get_child(entity)
            else:
                raise PathNotFound('Invalid target path')

        return current_entity

    def _update_sizes(self, path, size):
        """
        Updates sizes of all entities in the path by size
        """

        path_list = path_parse(path)
        self._recurse_sizes(path_list, self._root, size)

    def _recurse_sizes(self, path, current, size):
        """
        Recursively update the sizes of ancestors
        Base Case: Final entity in a path, update by size, and return size
        Recursive Case Non-Zip: Recurse with rest of path, new current entity, and size value
            Update size by returned value
        Recursive Case Zip: Recurse with rest of path, new current entity, and size value
            Update size by math.ceil(returned value/2.0)
        """
        if len(path) == 0:
            return

        new_current = current.get_child(path[0])

        # Base Case
        if len(path) == 1:
            if new_current.entity_type == 'zip':
                compressed_size = math.ceil(size / 2.0)
                new_current.size += compressed_size
                return compressed_size
            else:
                new_current.size += size
                return size
        # Recursive Case Non-Zip
        elif new_current.entity_type != 'zip':
            new_size = self._recurse_sizes(path[1:], new_current, size)
            new_current.size += new_size
            return new_size
        # Recursive Case Zip
        else:
            new_size = self._recurse_sizes(path[1:], new_current, size)
            compressed_size = math.ceil(new_size/2.0)
            new_current.size += compressed_size
            return compressed_size
