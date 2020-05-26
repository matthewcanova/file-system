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

    print('4. Adding Folder a')
    file_system.create('folder', 'foldera', 'DriveA')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('5. Adding Folder b')
    folder_b = file_system.create('folder', 'folderb', 'DriveB')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('6. Adding Folder c')
    file_system.create('folder', 'folderc', 'DriveB\\folderb')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('7. Adding Zip d')
    zip_d = file_system.create('zip', 'zipd', 'DriveA')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('8. Adding Text 1')
    text = file_system.create('text', 'text1', 'DriveB\\folderb\\folderc')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('9. Updating Text 1 Content')
    file_system.write_to_file(text.path, 'testabcd')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('10. Adding Text 2')
    text2 = file_system.create('text', 'text2', 'DriveA\\zipd')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('11. Updating Text 2 Content')
    file_system.write_to_file(text2.path, 'testabcdtestabcd')
    print('Current File System Structure: \n' + str(file_system))
    print()

    print('12. Move Folder B into Zip D')
    file_system.move(folder_b.path, zip_d.path)
    print('Current File System Structure: \n' + str(file_system))
    print()


if __name__ == '__main__':
    main()
