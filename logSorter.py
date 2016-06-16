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


class TestGroup(object):

    groups = {
        'FIRSTPART_UBUNTU': 'Ubuntu_tests',
        'FIRSTPART_Windows': 'Windows_tests',
        'FIRSTPART_OSX': 'OSX_tests'
    }

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

    groups = {
        'FIRSTPART_UBUNTU': 'Ubuntu_tests',
        'FIRSTPART_Windows': 'Windows_tests',
        'FIRSTPART_OSX': 'OSX_tests'
    }

    def __init__(self):
        self.pattern = 'FIRSTPART_.+_[0-9]+'

    def find_pattern(self, search_line):
        searched_expression = re.search(self.pattern, search_line)
        try:
            return searched_expression.group(0)
        except AttributeError:
            return False

    def search_pattern_in_file(self, file):
        log = open(file, 'r')
        try:
            for line in log.readlines():
                found_name = self.find_pattern(line)
                if found_name:
                    return found_name
        finally:
            log.close()

    def get_group_name(self, match):
        for key in self.groups.keys():
            if key in match:
                return self.groups[key]

    def get_test_case_id(self, match):
        pass


# y = DirectoryManagement()
# y.go_into_directory('logs/TC1000_2135')
# x = LogBrowser()
# line = 'PASSED:root:Test case: \'FIRSTPART_UBUNTU_12\' result: passed'
# print(x.search_pattern_in_file('TC1000_2135.log'))
#
# print('group name', x.get_group_name(x.find_pattern(line)))
# na później
# (ZSUBUNTU_[0-9])\w
# (?:abc)	non-capturing group
