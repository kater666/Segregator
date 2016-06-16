from logSorter import LogBrowser, DirectoryManagement

import os
import pytest
import shutil


def test_pattern_found():
    x = LogBrowser()
    search_line = 'PASSED:root:Test case: \'FIRSTPART_UBUNTU_12\' result: passed'
    found_name = x.find_pattern(search_line)
    expected_name = 'FIRSTPART_UBUNTU_12'
    assert found_name == expected_name


def test_pattern_not_found():
    x = LogBrowser()
    search_line = 'PASSED:root:Test case: \'DUPA\' result: passed'
    found_name = x.find_pattern(search_line)
    expected_name = 'FIRSTPART_UBUNTU_12'
    assert found_name != expected_name


def test_get_name_from_file():
    os.chdir('D:\PycharmProjects\logSorter')
    y = DirectoryManagement()
    y.go_into_directory('logs/TC1000_2135')
    x = LogBrowser()
    file_name = 'TC1000_2135.log'
    found_name = x.search_pattern_in_file(file_name)
    expected_name = 'FIRSTPART_UBUNTU_12'
    y.return_to_main_directory()
    assert found_name == expected_name


def test_no_test_name_found_in_file():
    os.chdir('D:\PycharmProjects\logSorter')
    y = DirectoryManagement()
    y.go_into_directory('logs/TC0000_0000')
    x = LogBrowser()
    file_name = 'TC0000_0000.log'
    found_name = x.search_pattern_in_file(file_name)
    expected_name = None
    y.return_to_main_directory()
    assert found_name == expected_name


def test_get_group_name():
    x = LogBrowser()
    search_line = 'PASSED:root:Test case: \'FIRSTPART_UBUNTU_12\' result: passed'
    expected_name = 'Ubuntu_tests'
    found_name = x.get_group_name(x.find_pattern(search_line))
    assert expected_name == found_name


def test_no_group_should_be_found():
    x = LogBrowser()
    search_line = 'PASSED:root:Test case: \'FIRSTPART_DUPA_12\' result: passed'
    expected_name = None
    found_name = x.get_group_name(x.find_pattern(search_line))
    assert expected_name == found_name


def test_create_directory_with_found_group_name():
    os.chdir('D:\PycharmProjects\logSorter\logs')
    y = DirectoryManagement()
    y.go_into_directory('TC1000_2135')
    y.create_group_directory('TC1000_2135.log')
    expected_directory = 'Ubuntu_tests'
    # Delete created directory after test.
    y.return_to_main_directory()
    #shutil.rmtree('./Ubuntu_tests')
    assert expected_directory in y.created_directories


def test_created_directories_updated():
    os.chdir('D:\PycharmProjects\logSorter\logs')
    y = DirectoryManagement()
    y.update_created_directories()
    expected_directories = ['OSX_tests', 'Ubuntu_tests', 'Windows_tests']
    assert expected_directories == y.created_directories

# Sprawdź gdzie jest pobierane working_directory, czy może inaczej puszczać testy pod względem ścieżki
