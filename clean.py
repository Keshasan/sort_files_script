import sys
import pathlib
import shutil


def main():
    folder_path = sys.argv[1]
    folder_path = pathlib.Path(folder_path)
    print(folder_path)
    if folder_path.exists():
        print('Exists')
    else:
        print('Not exists')


if __name__ == '__main__':
    main()
