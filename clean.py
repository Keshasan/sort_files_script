import sys
import pathlib
import shutil


def main():
    folder_path = sys.argv[1]
    folder_path = pathlib.Path(folder_path)
    if not folder_path.exists():
        print("Invalid path to folder. Restart script with correct 'path'.")
        return
    ####


if __name__ == '__main__':
    main()
