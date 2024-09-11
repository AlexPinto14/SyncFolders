# SyncFolders

## Overview
SyncFolders is a Python program that synchronizes two folders: a **source** folder and a **replica** folder. 
The replica folder will be an exact copy of the source folder. This is a one-way synchronization, 
meaning that changes made in the **source** folder are reflected in the **replica** folder, 
but not the other way around.

## Features
- Synchronizes files and folders from the source to the replica.
- Removes files and folders from the replica if they no longer exist in the source.
- Performs periodic synchronization based on a user-defined interval.
- Supports logging of synchronization actions (file creation, deletion, etc.).

## Setup
# 1. Download the ZIP or clone the repository:
- Download the project as a ZIP file from the GitHub repository or clone it.
- Extract the ZIP to a folder on your computer.

# 2. Use a terminal that supports Python:
- Open a terminal with Python 3.x installed (e.g., system terminal or VS Code terminal).

# 3. Navigate to the SyncFolders folder:
cd /path/to/SyncFolders

# 4. The source and replica folders are already created but you can replace these folders with any other folders of your choice.

# 5. Run the script:(source and replica may differ if you change/replace the original folders)
python main.py ./source ./replica ./log.txt 10

- The log.txt is created the first time you execute the script.
- The periodicity of the synchronization is set to 10 seconds but can also be modified

# 6. Create a file in the source folder:
- Add a file inside the source folder.
- After the next synchronization cycle, the file will be copied to the replica folder.

# 7. Verify that the file is copied to the replica folder:
- Check the replica folder and confirm the file has been copied.

# 8. Create a file in the replica folder that doesn’t exist in the source folder:
- Add a file in the replica folder that doesn’t exist in the source folder.
- In case that a folder is created by mistake it will also be removed after the synchronization cycle

# 9. Verify that the file/folder is removed from the replica folder:
- After the next synchronization cycle, the file will be removed from the replica folder.