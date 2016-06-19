import os
import pytest

from logSorter import DirectoryManagement


def test_get_search_directories():
    os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs')
    y = DirectoryManagement()
    y.get_search_directories()
    expected_directories = ['TC0000_0000', 'TC1000_2135', 'TC3267_1032', 'TC3268_1032']
    assert y.search_directories == expected_directories


# add os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs')
def test_created_directories_should_be_empty():
    y = DirectoryManagement()
    expected = []
    assert y.created_directories == expected


def test_created_directories_not_empty():
    os.chdir('D:\PycharmProjects\logSorter\logs')
    y = DirectoryManagement()
    expected = ['Ubuntu_tests', 'Windows_tests']
    # Remove test file.
    os.remove('./directories.txt')
    assert expected == y.created_directories


def test_directiories_to_be_created():
    os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs')
    y = DirectoryManagement()
    y.collect_directories_to_be_created()

    found = []
    f = open('directories.txt', 'r')
    for i in f.readlines():
        if i is not '\n':
            found.append(i)
        else:
            pass

    f.close()
    found.sort()
    expected = ['OSX_tests\n', 'Ubuntu_tests\n', 'Windows_tests\n']
    # Remove test file.
    os.remove('./directories.txt')
    assert found == expected


def test_create_group_directory():
    os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs\\more_logz')
    y = DirectoryManagement()
