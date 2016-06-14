from logSorter import *

import pytest
import os


def test_change_directory():
    os.chdir('./logs')
    x = DirectoryManagement()
    expected_directory = 'D:\PycharmProjects\logSorter\logs\TC1000_2135'
    path = 'TC1000_2135'
    x.go_into_directory(path)
    actual_directory = os.getcwd()
    os.chdir('D:\PycharmProjects\logSorter')
    assert expected_directory == actual_directory


def test_return_to_primary_directory():
    x = DirectoryManagement()
    starting_directory = 'D:\PycharmProjects\logSorter'
    x.go_into_directory('logs')
    x.return_to_main_directory()
    actual_directory = os.getcwd()
    os.chdir('D:\PycharmProjects\logSorter')
    assert starting_directory == actual_directory


def test_get_proper_directories():
    os.chdir('./logs')
    x = DirectoryManagement()
    x.get_directories()
    wanted_directories = ['TC1000_2135', 'TC3267_1032', 'TC3268_1032']
    os.chdir('../')
    print(x.search_directories)
    assert wanted_directories == x.search_directories


def test_pattern_found():
    x = LogBrowser()
    search_line = 'PASSED:root:Test case: \'ZS_UBUNTU_12\' result: passed'
    found_name = x.find_pattern(search_line, 'ZS_UBUNTU_([0-9]+)')
    expected_name = 'ZS_UBUNTU_12'
    assert found_name == expected_name


def test_pattern_not_found():
    x = LogBrowser()
    search_line = 'PASSED:root:Test case: \'DUPA\' result: passed'
    pattern = 'ZS_UBUNTU_([0-9]+)'
    found_name = x.find_pattern(search_line, pattern)
    expected_name = 'ZS_UBUNTU_12'
    assert found_name != expected_name


def test_get_name_from_file():
    os.chdir('./logs/TC1000_2135')
    x = LogBrowser()
    file_name = 'TC1000_2135.log'
    pattern = 'ZS_UBUNTU_([0-9]+)'
    found_name = x.search_test_name(file_name, pattern)
    expected_name = 'ZS_UBUNTU_12'
    os.chdir('../../')
    assert found_name == expected_name


def test_no_test_name_found_in_file():
    os.chdir('./logs/TC1000_2135')
    x = LogBrowser()
    file_name = 'TC1000_2135.log'
    pattern = 'ZS_UBUNTU_([0-9]+)'
    found_name = x.search_test_name(file_name, pattern)
    expected_name = 'DUPA'
    os.chdir('../../')
    assert found_name != expected_name


def test_get_group_name():
    x = LogBrowser()
    search_line = 'PASSED:root:Test case: \'ZS_UBUNTU_12\' result: passed'
    pattern = 'ZS_UBUNTU_([0-9]+)'
    expected_name = 'Ubuntu_tests'
    found_name = x.get_group_name(x.find_pattern(search_line, pattern))
    assert expected_name == found_name


# def test_id_name_group_name_and_id_returned():
#     x = LogBrowser()
#     expected = [1000, 'ZS_UBUNTU_12', 'Ubuntu_tests', 'ZS_UBUNTU']
#     x.returner()
#     actual = [x.tc_id, x.tc_name, x.group_name, x.group_id]
#     assert expected == actual