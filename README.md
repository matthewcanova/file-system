## In-Memory File System

### Description

This file-system consists of 5 types of entities: Roots, Drives, Folders, Text files, Zip files.

These entities, very much like their “real” file-system counterparts, obey the following relations:
- There is a single root per file system.
- Drives are only contained in the root, the root only contains drives.
- A folder, a drive or a zip file, may contain zero to many other folders, or files (text or zip).
- A text file does not contain any other entity.
- Any non-root entity must be contained in another entity.
- If entity A contains entity B then we say that A is the parent of B.

### Properties

- Type – The type of the entity (one of the 5 type above).
- Name - An alphanumeric string. Two entities with the same parent cannot have the same name.
- Path – The concatenation of the names of the containing entities, from the drive down to and including the entity.
    The names are separated by ‘\’.
- A text file has a property called Content which is a string.
- Root, Drive, Folder, and Zip are Containers and have a map of their children's
names to the children's object.
- Size – an integer defined as follows:
    - For a text file – it is the length of its content.
    - For a drive or a folder, it is the sum of all sizes of the entities it contains.
    - For a zip file, it is one half of the sum of all sizes of the entities it contains.

### Supported Operations:

####Create – Creates a new entity.
- Arguments: Type, Name, Path of parent.
- Exceptions: Path not found; Path already exists; Illegal File System Operation.

####Delete – Deletes an existing entity (and all the entities it contains).
- Arguments: Path
- Exceptions: Path not found.

####Move – Changing the parent of an entity.
- Arguments: Source Path, Destination Path.
- Exceptions: Path not found; Path already exists, Illegal File System Operation.

####WriteToFile – Changes the content of a text file.
- Arguments: Path, Content
- Exceptions: Path not found; Not a text file.