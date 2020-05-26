from file_system.file_system import FileSystem


def main():
    """
    Demonstrates the FileSystem implementation.
    Executes methods and prints the file system structure after each operation.
    """

    print('\n##############')
    print('# File System')
    print('##############\n')

    print('Package in /file_system\n')

    print('Pytest suite in /tests\n')

    print('###################')
    print('# File System Demo')
    print('###################\n')

    print('1. Creating File System')
    file_system = FileSystem()

    print('2. Adding Drive A')
    file_system.create('drive', 'DriveA', '')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('3. Adding Drive B')
    file_system.create('drive', 'DriveB', '')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('4. Adding Folder A')
    file_system.create('folder', 'FolderA', 'DriveA')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('5. Adding Folder B')
    folder_b = file_system.create('folder', 'FolderB', 'DriveB')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('6. Adding Folder C')
    file_system.create('folder', 'FolderC', 'DriveB\\FolderB')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('7. Adding Zip D')
    zip_d = file_system.create('zip', 'ZipD', 'DriveA')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('8. Adding Text A')
    text_a = file_system.create('text', 'TextA', 'DriveB\\FolderB\\FolderC')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('9. Updating Text A Content')
    file_system.write_to_file(text_a.path, 'testabcd')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('10. Adding Text B')
    text_b = file_system.create('text', 'TextB', 'DriveA\\ZipD')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('11. Updating Text B Content')
    file_system.write_to_file(text_b.path, 'testabcdtestabcd')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('12. Move Folder B into Zip D')
    file_system.move(folder_b.path, zip_d.path)
    print('Current File System Structure: \n' + str(file_system))
    print()


if __name__ == '__main__':
    main()
