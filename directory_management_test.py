import shutil

import pytest
import os
from logSorter import DirectoryManagement


def test_change_directory():
    y = DirectoryManagement()
    y.go_into_directory('logs')
    found_directory = os.getcwd()
    expected_directory = 'D:\PycharmProjects\logSorter\logs'
    y.return_to_main_directory()
    os.remove('./directories.txt')
    assert found_directory == expected_directory


def test_return_to_primary_directory():
    x = DirectoryManagement()
    starting_directory = os.getcwd()
    x.go_into_directory('logs')
    x.return_to_main_directory()
    actual_directory = os.getcwd()
    os.chdir('D:\PycharmProjects\logSorter')
    os.remove('./directories.txt')
    assert starting_directory == actual_directory


def test_get_proper_directories():
    y = DirectoryManagement()
    y.go_into_directory('logs')
    x = DirectoryManagement()
    x.get_search_directories()
    expected_directories = ['TC0000_0000', 'TC1000_2135', 'TC3267_1032', 'TC3268_1032']
    y.return_to_main_directory()
    os.remove('./directories.txt')
    assert expected_directories == x.search_directories


def test_create_directory_with_found_group_name():
    os.chdir('D:\PycharmProjects\logSorter\logs')
    y = DirectoryManagement()
    y.go_into_directory('TC3268_1032')
    y.create_group_directory('TC3268_1032.log')
    expected_directory = 'OSX_tests'
    # Delete created directory after test.
    y.return_to_main_directory()
    shutil.rmtree('./OSX_tests')
    os.remove('./directories.txt')
    assert expected_directory in y.created_directories


def test_already_created_directory():
    os.chdir('D:\PycharmProjects\logSorter\logs')
    y = DirectoryManagement()
    y.go_into_directory('TC1000_2135')
    result = y.create_group_directory('TC1000_2135.log')
    expected = False
    y.return_to_main_directory()
    os.remove('./directories.txt')
    assert result == expected


def test_created_directories_updated():
    os.chdir('D:\PycharmProjects\logSorter\logs')
    y = DirectoryManagement()
    y.update_created_directories()
    expected_directories = ['Ubuntu_tests', 'Windows_tests']
    os.remove('./directories.txt')
    assert expected_directories == y.created_directories


def test_create_txt_with_directories_to_be_created():
    os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs')
    y = DirectoryManagement()
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
    os.remove('./directories.txt')
    assert found == expected


def test_found_group_name_again_should_not_append_log():
    os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs\more_logz')
    y = DirectoryManagement()
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
    os.remove('./directories.txt')
    assert found == expected

# probably tests won't work
