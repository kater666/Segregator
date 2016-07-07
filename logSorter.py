import glob
import logging
import os
import re
import relocator as r
import shutil


class TestGroup(object):

    def __init__(self, group_name):
        self.group_name = group_name
        self.test_cases = []
        self.tc_count = len(self.test_cases)
        self.passes = 0
        self.fails = 0
        self.blocks = 0
        self.directory_path = None
        self.blocked_directory = None


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
        self.paths = {}

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
                path = self.working_directory + '\\%s' % directory
                logging.info('Creating %s group directory.' % directory)
                logging.info('Directory path: %s' % path)
                os.mkdir(path)

        self.required_directories = self.required_directories[:]
        self.update_created_directories()

    def get_test_cases(self):

        test_cases = []

        for directory in self.search_directories:
            self.go_into_directory(directory)

            test_case_object = TestCase()
            file_name = ('%s.log' % directory)
            test_case_object.tc_id = directory
            test_case_object.tc_name = self.search_pattern_in_file(file_name)
            test_case_object.group_name = self.get_group_name(test_case_object.tc_name)
            test_case_object.tc_status = self.get_test_case_status(file_name)
            test_cases.append(test_case_object)

            if test_case_object.tc_name is None:
                pass
            else:
                logging.info('Created %s, %s test case. Status: %s' % (directory,
                                                                       test_case_object.tc_name,
                                                                       test_case_object.tc_status))

            self.return_to_main_directory()

        return test_cases

    def get_group_directory_paths(self):

        self.return_to_main_directory()
        paths = {}
        for directory in self.created_directories:
            path = os.path.join(self.working_directory, directory)
            paths[directory] = path
        self.paths = paths

    def get_test_case_directory_path(self, tc_name):
        path = ''
        for directory in glob.glob('TC*'):
            if directory == tc_name:
                path = os.path.join(self.working_directory, directory)
        return path

    def create_test_groups(self):
        created_groups = {}

        for directory in self.created_directories:
            logging.info('Creating group: %s.' % directory)

            # directory is a name of a group
            # directory = 'Ubuntu_tests'
            group = TestGroup(directory)
            group.directory_path = self.paths[directory]
            created_groups[directory] = group

        return created_groups

    def sort_test_cases_into_groups(self, test_cases, test_groups):
        """
        test_cases is a list of TestCase class objects.
        test_group is a dictionary with keys - group names, values - TestGroup class objects.
        """
        for test in test_cases:
            # test is a single TestCase class object.
            for group in test_groups.keys():
                # group is a single string ('Ubuntu_tests')
                if group == test.group_name:
                    test_groups[group].test_cases.append(test)
                    if test.tc_status == 'PASSED':
                        test_groups[group].passes += 1
                    elif test.tc_status == 'FAILED':
                        test_groups[group].fails += 1
                    elif test.tc_status == 'BLOCKED':
                        test_groups[group].blocks += 1

    def sort_directories_into_group_directories(self, groups):
        group_names = groups.keys()
        test_cases = {}
        for group in groups:
            if groups[group].group_name in group_names:
                test_cases[group] = [case.tc_id for case in groups[group].test_cases]

            r.move_single_directory(self.working_directory, groups[group].directory_path, test_cases[group])


def create_envionment():
    path = 'D:\PycharmProjects\logSorter\logs\move_directory_test'
    os.chdir(path)
    actual = os.listdir('./')
    required = ['TC0000_0000', 'TC0001_0000', 'TC1000_2135', 'TC1000_4587',
                'TC1001_2548', 'TC1002_5435', 'TC3267_1032', 'TC3268_1032']

    if actual != required:
        shutil.rmtree(path, ignore_errors=True)
        s = 'D:\PycharmProjects\logSorter\Test directories'
        d = 'D:\PycharmProjects\logSorter\logs\move_directory_test'
        r.copy_many_directories(s, d)


def main():

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-7s %(message)s',
                        datefmt='[%d-%m-%Y %H:%M:%S]',
                        filename='sorting.txt',
                        filemode='w')

    logging.info('Started.')

    # TODO: delete create_invironment before using this module.
    create_envionment()
    y = DirectoryManagement()
    y.create_group_directory2()
    y.get_group_directory_paths()
    test_cases = y.get_test_cases()
    groups = y.create_test_groups()
    y.sort_test_cases_into_groups(test_cases, groups)
    y.sort_directories_into_group_directories(groups)

    for group in groups:

        # Create blocked directory if blocked/failed test cases appear in group.
        if groups[group].blocks > 0 or groups[group].fails > 0:
            directory_path = groups[group].directory_path
            blocked = 'blocked'
            make_dir = os.path.join(directory_path, blocked)
            os.makedirs(make_dir)
            groups[group].blocked_directory = make_dir

        # Sort blocked/failed test cases into 'blocked' directory.
        y.go_into_directory(group)
        test_cases = groups[group].test_cases
        logging.info('%s group.' % group)
        for case in test_cases:
            if case.tc_status == 'BLOCKED' or case.tc_status == 'FAILED':
                r.move_single_directory(groups[group].directory_path, groups[group].blocked_directory, [case.tc_id])

                logging.info('%s, %s status: %s' % (case.tc_id, case.tc_name, case.tc_status))
            else:
                logging.info('%s, %s status: %s' % (case.tc_id, case.tc_name, case.tc_status))

        y.return_to_main_directory()
    logging.info('Finished.')


if __name__ == '__main__':
    main()
