import pytest
from file_system.file_system import FileSystem
from file_system.file_system_exceptions import IllegalFileSystemOperation


def test_file_system_root():
    """
    Test the root to ensure only drives can be added
    """

    file_system = FileSystem()

    with pytest.raises(IllegalFileSystemOperation):
        file_system.create('folder', 'test', 'root')

    with pytest.raises(IllegalFileSystemOperation):
        file_system.create('zip', 'test', 'root')

    with pytest.raises(IllegalFileSystemOperation):
        file_system.create('text', 'test', 'root')

    new_drive = file_system.create('drive', 'test', 'root')

    assert new_drive.entity_type == 'drive'
    assert new_drive.path == 'test'
    assert new_drive.size == 0


def test_file_system_root_ids():
    """
    Test the various versions of root and ensure the path is set correctly
    """

    file_system = FileSystem()

    root_drive_a = file_system.create('drive', 'a', '')
    root_drive_b = file_system.create('drive', 'b', '\\')
    root_drive_c = file_system.create('drive', 'c', None)
    root_drive_d = file_system.create('drive', 'd', 'root')

    assert root_drive_a.path == 'a'
    assert root_drive_b.path == 'b'
    assert root_drive_c.path == 'c'
    assert root_drive_d.path == 'd'


def test_file_system_create_drives():
    """
    Test a folder being added to a drive
    """

    file_system = FileSystem()

    drive_a = file_system.create('drive', 'a', '')

    folder_a = file_system.create('folder', 'a', 'a')

    assert folder_a.name in drive_a.get_names()

    assert folder_a.entity_type == 'folder'
    assert len(folder_a.get_names()) == 0
    assert folder_a.path == 'a\\a'


def test_file_system_create_text():
    """
    Test content being added to a text file and the size being distributed up
    """

    file_system = FileSystem()

    drive_a = file_system.create('drive', 'a', '')

    folder_a = file_system.create('folder', 'a', 'a')

    text_a = file_system.create('text', 'a', 'a\\a')

    assert text_a.name in folder_a.get_names()

    file_system.write_to_file(text_a.path, 'test_string')

    assert text_a.size == len('test_string')
    assert folder_a.size == len('test_string')
    assert drive_a.size == len('test_string')


def test_file_system_create_zip():
    """
    Test content being added to a text file and the size being distributed up through a zip
    """

    file_system = FileSystem()

    drive_a = file_system.create('drive', 'a', '')

    zip_a = file_system.create('zip', 'a', 'a')

    text_a = file_system.create('text', 'a', 'a\\a')

    assert text_a.name in zip_a.get_names()

    file_system.write_to_file(text_a.path, 'teststring')

    assert text_a.size == len('teststring')
    assert zip_a.size == len('teststring') / 2
    assert drive_a.size == len('teststring') / 2


def test_file_system_delete():

    file_system = FileSystem()

    drive_a = file_system.create('drive', 'a', '')

    folder_a = file_system.create('folder', 'a', 'a')

    text_a = file_system.create('text', 'a', 'a\\a')

    test_string = 'teststring'
    file_system.write_to_file(text_a.path, test_string)

    assert folder_a.size == len(test_string)
    assert drive_a.size == len(test_string)

    file_system.delete(text_a.path)

    assert 'a' not in folder_a.get_names()
    assert folder_a.size == 0
    assert drive_a.size == 0


def test_file_system_move():

    file_system = FileSystem()

    file_system.create('drive', 'a', '')

    folder_b = file_system.create('folder', 'b', 'a')

    folder_bb = file_system.create('folder', 'bb', 'a')

    text_c = file_system.create('text', 'c', 'a\\b')

    test_string = 'teststring'
    file_system.write_to_file(text_c.path, test_string)

    file_system.move(text_c.path, folder_bb.path)

    assert 'c' not in folder_b.get_names()
    assert 'c' in folder_bb.get_names()
    assert folder_b.size == 0
    assert folder_bb.size == len(test_string)


def test_file_system_write_to_file():

    file_system = FileSystem()

    drive_a = file_system.create('drive', 'a', '')

    folder_b = file_system.create('folder', 'b', 'a')

    text_c = file_system.create('text', 'c', 'a\\b')

    test_string = 'teststring'
    file_system.write_to_file(text_c.path, test_string)

    assert text_c.content == test_string
    assert text_c.size == len(test_string)
    assert folder_b.size == len(test_string)
    assert drive_a.size == len(test_string)
