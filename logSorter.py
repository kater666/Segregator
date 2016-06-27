import os
import re


class TestGroup(object):

    def __init__(self):
        #self.group_range = {}  #maybe will not be used
        self.group_name = ''
        self.tc_count = 0
        self.passes = 0
        self.fails = 0
        self.blocks = 0


class TestCase(TestGroup):

    def __init__(self):
        super(TestGroup, self).__init__()
        self.tc_id = ''
        self.tc_name = ''
        self.group_name = ''
        self.tc_status = 'Unknown'


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

    def get_test_case_status(self, file):
        statuses = ['PASSED', 'FAILED', 'BLOCKED']
        log = open(file, 'r')
        try:
            for line in log.readlines():
                for i in statuses:
                    status = re.search(i, line)
                    try:
                        return status.group(0)
                    except AttributeError:
                        continue
            else:
                return 'Not found'
        finally:
            log.close()


class DirectoryManagement(LogBrowser):

    def __init__(self):
        LogBrowser.__init__(self)
        self.working_directory = os.getcwd()
        self.search_directories = []
        self.created_directories = []
        self.required_directories = []

        # Call methods to collect required data.
        self.update_created_directories()
        self.get_search_directories()
        self.collect_directories_to_be_created()

    def go_into_directory(self, path):
        os.chdir('./%s' % path)

    def return_to_main_directory(self):
        os.chdir(self.working_directory)

    #1
    def get_search_directories(self):
        """
        Method browses cwd searching for folders with TCXXXX in name.
        It updates self.search_directories which will be entered by later methods.
        """
        search_directory = os.listdir('./')
        for directory in search_directory:
            if re.match(r'TC[0-9]+_[0-9]+', directory) and directory not in self.search_directories:
                self.search_directories.append(directory)

        self.search_directories.sort()

    #2
    def update_created_directories(self):
        self.return_to_main_directory()
        found_directories = os.listdir('./')
        for directory in found_directories:
            # If directory should be in self.created_directories but !It is not!
            if directory in self.groups.values() and directory not in self.created_directories:
                self.created_directories.append(directory)

        self.created_directories.sort()

    #3
    def collect_directories_to_be_created(self):
        """ Go into file, read group name, write it's name to .txt """
        for directory in self.search_directories:
            self.go_into_directory(directory)
            # TODO: change file extension to log's extension.
            group_name = self.get_group_name(self.search_pattern_in_file(directory + '.log'))
            self.return_to_main_directory()
            if group_name and group_name not in self.required_directories:
                self.required_directories.append(group_name)
            else:
                pass

        self.required_directories.sort()

    #4
    def create_group_directory2(self):
        for directory in self.required_directories:
            if directory not in self.created_directories:
                os.mkdir(self.working_directory + '\\%s' % directory)

        self.required_directories = self.required_directories[:]
        self.update_created_directories()

    def get_test_case_data(self, test_case):

        test_case_object = TestCase()

        for directory in self.search_directories:
            # case: TC1000_2135
            if test_case in directory:
                self.go_into_directory(directory)
                file_name = ('%s.log' % directory)
                # Returns test case's id. This might need to be changed - obtained from something else.
                test_case_object.tc_id = test_case
                # Returns whole found expression, at least I hope.
                test_case_object.tc_name = self.search_pattern_in_file(file_name)
                # Gets group's name based on found expression.
                test_case_object.group_name = self.get_group_name(test_case_object.tc_name)
                # Gets test case's status. I hope...
                test_case_object.tc_status = self.get_test_case_status(file_name)

        return test_case_object


# (ZSUBUNTU_[0-9])\w
# (?:abc)	non-capturing group
