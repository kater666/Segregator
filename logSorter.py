import glob
import re
import os


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


class LogBrowser(object):

    def search_test_name(self, file, pattern):
        log = open(file, 'r')
        for line in log.readlines():
            found_name = self.find_pattern(line, pattern)
            if found_name is not False:
                return found_name

    def find_pattern(self, search_line, pattern):
        searched_expression = re.search(pattern, search_line)
        try:
            match = searched_expression.group(0)
            return match
        except AttributeError:
            return False


class TestCase(object):

    def __init__(self, TCid, test_group, status):
        self.TCid = TCid
        self.test_group = test_group
        self.status = status

# x = LogBrowser()
# print(x.get_directories('./logs'))

# na później
# (ZSUBUNTU_[0-9])\w
# (?:abc)	non-capturing group