import os
import re


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
        """ Method will search for pattern like groups.keys() """
        log = open(file, 'r')
        try:
            for line in log.readlines():
                found_pattern = self.find_pattern(line)
                if found_pattern:
                    return found_pattern
        finally:
            log.close()

    def get_group_name(self, match):
        for key in self.groups.keys():
            if match is not None and key in match:
                # Returns group name from dictionary if found.
                return self.groups[key]
            else:
                pass

    def get_test_case_id(self, match):
        pass


class DirectoryManagement(LogBrowser):

    def __init__(self):
        LogBrowser.__init__(self)
        self.working_directory = os.getcwd()
        self.search_directories = []
        self.created_directories = []

        # Call methods to collect required data.
        self.update_created_directories()
        self.get_search_directories()
        self.search_directories.sort()
        self.collect_directories_to_be_created()


    def go_into_directory(self, path):
        os.chdir('./%s' % path)

    def return_to_main_directory(self):
        os.chdir(self.working_directory)

    def get_search_directories(self):
        """
        Method browses cwd searching for folders with TCXXXX in name.
        It updates self.search_directories which will be entered by later methods.
        """
        search_directory = os.listdir('./')
        for directory in search_directory:
            if re.match('TC[0-9]+_[0-9]+', directory) and directory not in self.search_directories:
                self.search_directories.append(directory)

    def update_created_directories(self):
        self.return_to_main_directory()
        found_directories = os.listdir('./')
        for directory in found_directories:
            # If directory should be in self.created_directories but !It is not!
            if directory in self.groups.values() and directory not in self.created_directories:
                self.created_directories.append(directory)

    def collect_directories_to_be_created(self):
        """ go into file, read group name, write it's name to .txt """
        dirs_2b_created = []
        for directory in self.search_directories:
            self.go_into_directory(directory)
            group_name = self.get_group_name(self.search_pattern_in_file(directory + '.log'))
            self.return_to_main_directory()
            if group_name and group_name not in dirs_2b_created:
                dirs_2b_created.append(group_name)
            else:
                pass

        dirs_2b_created.sort()
        directory_log = open('directories.txt', 'w')
        for line in dirs_2b_created:
            directory_log.write(line + '\n')

    def create_group_directory(self, file):
        match = self.search_pattern_in_file(file)
        group_name = self.get_group_name(match)
        if group_name not in self.created_directories:
            os.makedirs(self.working_directory + '\\%s' % group_name)
            self.created_directories.append(group_name)
        else:
            return False


# os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs')
# y = DirectoryManagement()
# y.get_search_directories()
# print(y.search_directories)
# y.collect_directories_to_be_created()

# na później
# (ZSUBUNTU_[0-9])\w
# (?:abc)	non-capturing group


"""
Create class object (start program) in the catalog with catalogs with logs:
logs
|--TCXXX
|--TCXXX
|--TCXXX
|--here y = DirectoryManagement()

y = DirectoryManagement()
After that:
- self.created_directories is appended,
- self.search_directories is appended and sorted,
- a file with directories that should be created is created in starting directory,
"""
