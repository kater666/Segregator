from os import listdir, path
from shutil import copytree, copy2


def move_many_directories(src, dst, symlinks=False, ignore=None):
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            copy2(s, d)


def move_single_directory(src, dst, files, symlinks=False, ignore=None):
    for item in listdir(src):
        for file in files:
            if item.split('\\')[-1] == file:
                s = path.join(src, item)
                d = path.join(dst, item)
                if path.isdir(s):
                    copytree(s, d, symlinks, ignore)
                else:
                    copy2(s, d)

# s = 'D:\PycharmProjects\logSorter\Test directories'
# d = 'D:\PycharmProjects\logSorter\\new'
# move_many_directories(s, d)
# move_single_directory(s, d, 'TC0000_0000')
