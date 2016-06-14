import glob
import re
import os
import sqlite3


class DirectoryManagement(object):

    def __init__(self):
        self.working_directory = os.getcwd()
        self.search_directories = []

    def go_into_directory(self, path):
        os.chdir('./%s' % path)

    def return_to_main_directory(self):
        os.chdir(self.working_directory)

    def get_directories(self):
        search_directory = os.listdir('./')
        print(search_directory)
        for directory in search_directory:
            if re.match('TC[0-9]+_[0-9]+', directory):
                self.search_directories.append(directory)


# TODO: Basically DATABASE for next 2 classes
class TestGroup(object):
    def __init__(self, group_id, group_name, tc_count):
        self.group_id = group_id
        self.group_range = {}
        self.group_name = group_name
        self.tc_count = tc_count


class TestCase(TestGroup):

    def __init__(self, tc_id, tc_name, group_id, group_name, tc_status):
        super(TestGroup, self).__init__()
        self.tc_id = tc_id
        self.tc_name = tc_name
        self.group_id = group_id
        self.group_name = group_name
        self.tc_status = tc_status


class LogBrowser(object):

    def search_test_name(self, file, pattern):
        log = open(file, 'r')
        try:
            for line in log.readlines():
                found_name = self.find_pattern(line, pattern)
                if found_name:
                    return found_name
        finally:
            log.close()

    def find_pattern(self, search_line, pattern):
        searched_expression = re.search(pattern, search_line)
        try:
            match = searched_expression.group(0)
            return match
        except AttributeError:
            return False

    # TODO: stworzyć bazę danych z nazwami grup testów
    # TODO: odwoływać się do niej przy wyciąganiu nazwy grupy z loga
    # TODO: refactor this shit
    def get_group_name(self, match):
        group_name = 'ZS_UBUNTU'
        if group_name in match:
            return 'Ubuntu_tests'

# x = LogBrowser()
# print(x.get_directories('./logs'))

# na później
# (ZSUBUNTU_[0-9])\w
# (?:abc)	non-capturing group