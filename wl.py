import os
import sys
import click
from os.path import join, getsize
from colorama import Fore, Back, Style, init

init()

# получаем директорию из которой был запущен скрипт
root = os.path.abspath(os.curdir)


def setColor(color, s):
    return color + s + Style.RESET_ALL


# нормализируем размер дабы избежать 100500 bytes
def normalizeSize(size, bytes=None):
    SIZES = ['KB', 'MB', 'GB']
    s = str(size) + ' Bytes'
    if bytes:
        return s
    for i in SIZES:
        div, mod = divmod(size, 1024)
        if div == 0:
            break
        s = str(div) + '.' + str(mod) + i
        size = div
    return s


# получаем размер папки, погружаясь в неё рекурсивно и суммируя размеры всех файлов
def getFolderSize(folder, errors):
    size = 0
    try:
        for i in os.listdir(folder):
            try:
                file = join(folder, i)
                if os.path.isfile(file):
                    size += getsize(file)
                if os.path.isdir(file):
                    size += getFolderSize(file, errors)
            except PermissionError:
                break
    except PermissionError:
        if errors:
            print(setColor(Fore.RED, "Недостаточно прав для папки: " + folder))
        return 0
    return size


# получаем список файлов и директорий в директории folder
def getAll(folder, errors, bytes):
    files = []
    folders = []
    for file in os.listdir(folder):
        # print(join(folder, file))
        pathToFile = join(folder, file)
        type = '<UNKNOWN>'
        size = ''
        if os.path.isfile(join(folder, file)):
            size = normalizeSize(getsize(pathToFile), bytes)
            files.append(file)
            type = '<FILE>'
        if os.path.isdir(join(folder, file)):
            # print(normalizeSize(getFolderSize(join(folder,file))), ' - ', file)
            type = '<DIR>'
            size = normalizeSize(getFolderSize(join(folder, file), errors), bytes)
        print('{:<40}'.format(file),
              '{:^8}'.format(setColor(Fore.CYAN, type)),
              setColor(Fore.GREEN, '{:<10}'.format(size)))


@click.command()
@click.option('--errors', '-e', is_flag=1, flag_value=1, help="show all error messages")
@click.option('--bytes', '-b', is_flag=1, flag_value=1, help="show sizes in bytes")
def main(errors, bytes):
    getAll(root, errors, bytes)
    out_size = getFolderSize(root, errors)
    out_size = normalizeSize(out_size, bytes)
    print(setColor(Fore.BLUE, '{} size is: '.format(root)), setColor(Fore.GREEN, out_size))


if __name__ == '__main__':
    main()
    pass
