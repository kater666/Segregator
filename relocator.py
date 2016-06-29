from os import listdir, path
from shutil import copytree, copy2


def movedirectories(src, dst, symlinks=False, ignore=None):
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            copy2(s, d)


# s = 'D:\PycharmProjects\logSorter\Test directories'
# d = 'D:\PycharmProjects\logSorter\\new'
# movedirectories(s, d)
