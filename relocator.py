from os import listdir, path
import shutil


def copy_many_directories(src, dst, symlinks=False, ignore=None):
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def copy_single_directory(src, dst, files, symlinks=False, ignore=None):
    for item in listdir(src):
        for file in files:
            if item.split('\\')[-1] == file:
                s = path.join(src, item)
                d = path.join(dst, item)
                if path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)


def move_single_directory(src, dst, files):
    """ Optional: copy many directories. """

    for item in listdir(src):
        for file in files:
            if item.split('\\')[-1] == file:
                s = path.join(src, item)
                d = path.join(dst, item)
                if path.isdir(s):
                    shutil.move(s, d)

#
# import os
#
# os.chdir('D:\PycharmProjects\logSorter\logs\move_directory_test')
# s = 'D:\PycharmProjects\logSorter\logs\move_directory_test'
# d = 'D:\PycharmProjects\logSorter\logs\move_directory_test\OSX_tests'
# move_single_directory(s, d, ['TC0000_0000'])

# s = 'D:\PycharmProjects\logSorter\Test directories'
# d = 'D:\PycharmProjects\logSorter\\new'
# move_many_directories(s, d)
# move_single_directory(s, d, 'TC0000_0000')
