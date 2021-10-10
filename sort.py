import sys
from pathlib import Path
import shutil
import os
import re

folder_names = ['archives', 'video', 'audio', 'documents', 'images']

sorting_dict = {
    'archives': ('ZIP', 'GZ', 'TAR'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
}


def main():
    folder_path = sys.argv[1]

    if len(sys.argv) > 2:
        print('Too much arguments.')
        return

    folder_path = Path(folder_path)
    main_dir = folder_path
    if not folder_path.exists():
        print("Invalid path to folder. Restart script with correct 'path'.")
        return

    recursive_sort_directory(folder_path, main_dir)
    remove_empty_folders(folder_path)
    unpack_archives(folder_path)


def recursive_sort_directory(path: Path, main_dir: Path):
    '''
         Recursive sort directory
    '''
    if path.is_dir() and path.name not in folder_names:
        for element in path.iterdir():
            recursive_sort_directory(element, main_dir)

    else:
        file_extension = path.name.split('.')[1]
        file_name = path.name.split('.')[0]

        for folder, extension in sorting_dict.items():
            if file_extension.upper() in extension:
                if main_dir.joinpath(folder).exists():
                    shutil.move(path.as_posix(),
                                main_dir.joinpath(folder).joinpath(normalize(file_name)+'.'+file_extension))
                else:
                    os.mkdir(main_dir.joinpath(folder))
                    shutil.move(path.as_posix(),
                                main_dir.joinpath(folder).joinpath(normalize(file_name)+'.'+file_extension))


def normalize(name: str):
    table_symbols = ('абвгґдеєжзиіїйклмнопрстуфхцчшщюяыэАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЫЭьъЬЪ',
                     (
                         *(u'abvhgde'), 'ye', 'zh', *
                         (u'zyi'), 'yi', *(u'yklmnoprstuf'),
                         'kh', 'ts',
                         'ch', 'sh', 'shch', 'yu', 'ya', 'y', 'ye', *
                         (u'ABVHGDE'),
                         'Ye', 'Zh', *(u'ZYI'),
                         'Yi', *(u'YKLMNOPRSTUF'), 'KH', 'TS', 'CH', 'SH',
                         'SHCH', 'YU', 'YA', 'Y', 'YE', 'Y',
                         *(u'_' * 4)
                     )
                     )
    map_cyr_to_latin = {ord(src): dest for src, dest in zip(*table_symbols)}
    rx = re.compile(r"[^\w_]")
    return rx.sub('_', name.translate(map_cyr_to_latin))


def remove_empty_folders(path: Path):
    '''
        Recursively removes empty folders + renames folders using 'normalize function'
    '''
    if path.is_dir() and path.name not in folder_names:

        for element in path.iterdir():
            if element.is_dir():
                shutil.move(element, element.parent.joinpath(
                    normalize(normalize(element.name))))
                element = element.parent.joinpath(
                    normalize(normalize(element.name)))
                remove_empty_folders(element)

        if len([element for element in path.iterdir()]) == 0:
            shutil.rmtree(path)


def unpack_archives(path: Path):
    '''
        Checks if folder "archives" exists, then unpack archive + removes it 
    '''
    archives_folder = path.joinpath('archives')

    if not archives_folder.exists():
        return

    for archive in archives_folder.iterdir():
        destination = archive.parent.joinpath(archive.name.split('.')[0])
        shutil.unpack_archive(archive, destination)
        archive.unlink()


if __name__ == '__main__':
    main()
