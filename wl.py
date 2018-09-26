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
def normalizeSize(size):
    SIZES = ['KB', 'MB', 'GB']
    s = str(size) + 'Bytes'
    for i in SIZES:
        div, mod = divmod(size, 1024)
        if div == 0:
            break
        s = str(div) + '.' + str(mod) + i
        size = div
    return s

# получаем размер папки, погружаясь в неё рекурсивно и суммируя размеры всех файлов
def getFolderSize(folder):
    size = 0
    try:
        for i in os.listdir(folder):
            try:
                file = join(folder, i)
                if os.path.isfile(file):
                    size += getsize(file)
                if os.path.isdir(file):
                    try:
                        size += getFolderSize(file)
                    except PermissionError:
                        print(setColor(Fore.RED, "Недосccтаточно прав для папки: " + file))
            except PermissionError:
                break
    except PermissionError:
        print(setColor(Fore.RED, "Недостаточно прав для папки: " + folder))
        return 0
    return size

# получаем список файлов и директорий в директории folder
def getAll(folder):
    files = []
    folders = []
    for file in os.listdir(folder):
        # print(join(folder, file))
        pathToFile = join(folder, file)
        type = '<UNKNOWN>'
        size = ''
        if os.path.isfile(join(folder, file)):
            size = normalizeSize(getsize(pathToFile))
            files.append(file)
            type = '<FILE>'
        if os.path.isdir(join(folder, file)):
            # print(normalizeSize(getFolderSize(join(folder,file))), ' - ', file)
            type = '<DIR>'
            size = normalizeSize(getFolderSize(join(folder, file)))
        print('{:<20}'.format(file),
              '{:^8}'.format(type),
              setColor(Fore.GREEN, '{:>10}'.format(size)))

def test():
    for path in os.walk(root):
        # print(path)
        for i in path[2]:
            file = os.path.join(root, path[0], i)
            s = i + ' - '
            try:
                s += str(getsize(file) // 1024) + 'кб'
            except FileNotFoundError as ex:
                s += 'ERROR'
            print(s)

if __name__ == '__main__':
    getAll(root)
    print(setColor(Fore.BLUE, '{} size is: '.format(root)), setColor(Fore.GREEN, normalizeSize(getFolderSize(root))))
