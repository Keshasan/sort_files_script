import sys
import pathlib
import shutil
import os


def main():
    #folder_path = sys.argv[1]
    folder_path = "/home/keshasan/Desktop/projects/test-folder-tree/"
    folder_path = pathlib.Path(folder_path)
    if not folder_path.exists():
        print("Invalid path to folder. Restart script with correct 'path'.")
        return
    ####
    list_files = get_files(folder_path)
    print(list_files)


def get_files(path):
    list_files = []
    recursive_walk_direcory(path, list_files)
    return list_files


def recursive_walk_direcory(path: pathlib.Path, list_files: list):

    if path.is_dir() and path.name not in ('archives', 'video', 'audio', 'documents', 'images'):
        for element in path.iterdir():
            recursive_walk_direcory(element, list_files)
    else:
        with open(path.as_posix(), 'rb') as f:
            file_bytes = f.read()
            list_files.append([path.as_posix(), path.name, file_bytes])


if __name__ == '__main__':
    main()
