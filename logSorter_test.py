from logSorter import *

import pytest
import os


def test_get_proper_directories():
    directory = LogBrowser()
    actual_directories = directory.get_directories('./logs')
    wanted_directories = ['TC1000_2135', 'TC3267_1032', 'TC3268_1032']
    assert actual_directories == wanted_directories


def test_find_test_name():
    init_class = LogBrowser()
    search_line = 'PASSED:root:Test case: \'ZSUBUNTU_12\' result: passed'
    found_name = init_class.find_test_name(search_line, 'ZSUBUNTU_([0-9]+)')
    expected_name = 'ZSUBUNTU_12'
    assert found_name == expected_name


def test_pattern_not_found():
    init_class = LogBrowser()
    search_line = 'PASSED:root:Test case: \'DUPA\' result: passed'
    found_name = init_class.find_test_name(search_line, 'ZSUBUNTU_([0-9]+)')
    expected_name = 'ZSUBUNTU_12'
    assert found_name == False

# def test_get_name_from_file():
#     init_class = LogBrowser()
#     os.chdir('./logs/TC1000_2135')
#     file_name = 'TC1000_2135.log'
#     found_name = init_class.get_test_case(file_name, 'ZSUBUNTU_([0-9]+)')
#     expected_name = 'ZSUBUNTU_12'
#     assert found_name == expected_name
