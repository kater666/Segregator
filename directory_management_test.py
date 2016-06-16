import pytest
import os
from logSorter import DirectoryManagement


def test_change_directory():
    y = DirectoryManagement()
    y.go_into_directory('logs')
    found_directory = os.getcwd()
    expected_directory = 'D:\PycharmProjects\logSorter\logs'
    y.return_to_main_directory()
    assert found_directory == expected_directory


def test_return_to_primary_directory():
    x = DirectoryManagement()
    starting_directory = os.getcwd()
    x.go_into_directory('logs')
    x.return_to_main_directory()
    actual_directory = os.getcwd()
    os.chdir('D:\PycharmProjects\logSorter')
    assert starting_directory == actual_directory


def test_get_proper_directories():
    y = DirectoryManagement()
    y.go_into_directory('logs')
    x = DirectoryManagement()
    x.get_directories()
    wanted_directories = ['TC0000_0000', 'TC1000_2135', 'TC3267_1032', 'TC3268_1032']
    y.return_to_main_directory()
    assert wanted_directories == x.search_directories
