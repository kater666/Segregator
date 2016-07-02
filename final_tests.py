import glob
import os
import shutil
import unittest

from ddt import ddt, data
from logSorter import DirectoryManagement
from relocator import move_many_directories


@ddt
class FinalTest(unittest.TestCase):

    def setUp(self):
        os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs')

    def create_envionment(self):
        path = 'D:\PycharmProjects\logSorter\logs\move_directory_test'
        os.chdir(path)
        actual = os.listdir('./')
        required = ['TC0000_0000', 'TC0001_0000', 'TC1000_2135', 'TC1000_4587',
                    'TC1001_2548', 'TC1002_5435', 'TC3267_1032', 'TC3268_1032']

        if actual != required:
            shutil.rmtree(path, ignore_errors=True)
            s = 'D:\PycharmProjects\logSorter\Test directories'
            d = 'D:\PycharmProjects\logSorter\logs\move_directory_test'
            move_many_directories(s, d)

    def remove_test_directories(self):
        # Remove tests directories
        for crap in glob.glob('*_tests'):
            shutil.rmtree(crap)

    def test_get_search_directories(self):
        y = DirectoryManagement()
        y.get_search_directories()
        expected_directories = ['TC0000_0000', 'TC0001_0000', 'TC1000_2135', 'TC3267_1032', 'TC3268_1032']
        assert y.search_directories == expected_directories

    def test_created_directories_should_be_empty(self):
        y = DirectoryManagement()
        expected = []
        assert y.created_directories == expected

    def test_created_directories_not_empty(self):
        os.chdir('D:\PycharmProjects\logSorter\logs')
        y = DirectoryManagement()
        expected = ['Ubuntu_tests', 'Windows_tests']
        assert expected == y.created_directories

    def test_directiories_to_be_created(self):
        y = DirectoryManagement()
        y.collect_directories_to_be_created()
        expected = ['OSX_tests', 'Ubuntu_tests', 'Windows_tests']
        assert y.required_directories == expected

    def test_create_group_directory(self):
        os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs\more_logz')
        y = DirectoryManagement()
        y.create_group_directory2()
        expected = ['OSX_tests', 'Ubuntu_tests', 'Windows_tests']

        self.remove_test_directories()

        assert expected == y.created_directories

    @data(('TC1000_2135', 'PASSED'), ('TC3267_1032', 'FAILED'), ('TC3268_1032', 'BLOCKED'))
    def test_get_test_case_status(self, value):
        x = DirectoryManagement()
        x.go_into_directory('%s' % value[0])
        status = x.get_test_case_status('%s.log' % value[0])
        expected = value[1]
        x.return_to_main_directory()
        self.assertEqual(status, expected)

    def test_status_not_found(self):
        x = DirectoryManagement()
        x.go_into_directory('TC0001_0000')
        status = x.get_test_case_status('TC0001_0000.log')
        expected = 'Not found'
        x.return_to_main_directory()
        self.assertEqual(status, expected)

    def test_single_test_case(self):
        y = DirectoryManagement()
        test_data = y.get_test_cases()[2]
        actual = [
            test_data.tc_id,
            test_data.tc_name,
            test_data.group_name,
            test_data.tc_status
        ]
        expected = ['TC1000_2135', 'FIRSTPART_UBUNTU_12', 'Ubuntu_tests', 'PASSED']
        self.assertEqual(actual, expected)

    def test_create_groups(self):
        y = DirectoryManagement()
        y.create_group_directory2()
        y.get_group_directory_paths()

        self.remove_test_directories()
        created_groups = y.create_test_groups()
        actual = created_groups.keys()
        expected = ['OSX_tests', 'Ubuntu_tests', 'Windows_tests']
        self.assertEqual(sorted(actual), expected)

    def test_sort_tests_into_groups(self):
        y = DirectoryManagement()
        y.create_group_directory2()
        y.get_group_directory_paths()

        self.remove_test_directories()

        # Get required test data.
        test_cases = y.get_test_cases()
        created_groups = y.create_test_groups()

        # Tested method.
        y.sort_test_cases_into_groups(test_cases, created_groups)

        first_test = created_groups['Ubuntu_tests'].test_cases[0].tc_name
        second_test = created_groups['Windows_tests'].test_cases[0].tc_name
        third_test = created_groups['OSX_tests'].test_cases[0].tc_name

        self.assertEqual(first_test, 'FIRSTPART_UBUNTU_12')
        self.assertEqual(second_test, 'FIRSTPART_Windows_452')
        self.assertEqual(third_test, 'FIRSTPART_OSX_87')

    def test_set_group_directory_path(self):
        self.create_envionment()
        y = DirectoryManagement()
        y.create_group_directory2()
        y.get_group_directory_paths()
        groups = y.create_test_groups()

        osx = groups['OSX_tests']
        ubuntu = groups['Ubuntu_tests']
        windows = groups['Windows_tests']

        self.remove_test_directories()

        expectedOSX = r'D:\PycharmProjects\logSorter\logs\move_directory_test\OSX_tests'
        expectedUbuntu = r'D:\PycharmProjects\logSorter\logs\move_directory_test\Ubuntu_tests'
        expectedWindows = r'D:\PycharmProjects\logSorter\logs\move_directory_test\Windows_tests'

        self.assertEqual(osx.directory_path, expectedOSX)
        self.assertEqual(ubuntu.directory_path, expectedUbuntu)
        self.assertEqual(windows.directory_path, expectedWindows)

    def test_set_test_case_path(self):

        """" Pointless test. """

        self.create_envionment()
        y = DirectoryManagement()

        # Tested method.
        test_cases = y.get_test_cases()

        expected = [
            'D:\PycharmProjects\logSorter\logs\move_directory_test\TC0000_0000',
            'D:\PycharmProjects\logSorter\logs\move_directory_test\TC0001_0000',
            'D:\PycharmProjects\logSorter\logs\move_directory_test\TC1000_2135',
            'D:\PycharmProjects\logSorter\logs\move_directory_test\TC1000_4587',
            'D:\PycharmProjects\logSorter\logs\move_directory_test\TC1001_2548',
            'D:\PycharmProjects\logSorter\logs\move_directory_test\TC1002_5435',
            'D:\PycharmProjects\logSorter\logs\move_directory_test\TC3267_1032',
            'D:\PycharmProjects\logSorter\logs\move_directory_test\TC3268_1032'
        ]
        found = []
        for case in test_cases:
            found.append(case.directory_path)

        self.assertEqual(sorted(found), sorted(expected))

    def test_move_to_directories(self):
        self.create_envionment()

        y = DirectoryManagement()
        y.create_group_directory2()
        y.get_group_directory_paths()
        test_cases = y.get_test_cases()
        groups = y.create_test_groups()
        y.sort_test_cases_into_groups(test_cases, groups)

        # Tested method.
        y.sort_directories_into_group_directories(groups)
        main = os.listdir('./')

        y.go_into_directory('Ubuntu_tests')
        ubuntu = os.listdir('./')
        y.return_to_main_directory()

        y.go_into_directory('OSX_tests')
        osx = os.listdir('./')
        y.return_to_main_directory()

        y.go_into_directory('Windows_tests')
        windows = os.listdir('./')
        y.return_to_main_directory()

        expected_main = ['TC0000_0000', 'TC0001_0000', 'Ubuntu_tests', 'OSX_tests', 'Windows_tests']
        expected_ubuntu = ['TC1000_2135', 'TC1000_4587', 'TC1001_2548', 'TC1002_5435']
        expected_osx = ['TC3268_1032']
        expected_windows = ['TC3267_1032']

        self.assertEqual(sorted(main), sorted(expected_main))
        self.assertEqual(sorted(ubuntu), sorted(expected_ubuntu))
        self.assertEqual(sorted(osx), sorted(expected_osx))
        self.assertEqual(sorted(windows), sorted(expected_windows))


if __name__ == '__main__':
    unittest.main()

# D:\PycharmProjects\logSorter\logs\move_directory_test
# TC0000_0000
# TC0001_0000
# 'Ubuntu_tests',
# 'OSX_tests',
# 'Windows_tests'

# D:\PycharmProjects\logSorter\logs\move_directory_test\Ubuntu_tests
# TC1000_2135
# TC1000_4587
# TC1001_2548
# TC1002_5435

# D:\PycharmProjects\logSorter\logs\move_directory_test\Windows_tests
# TC3267_1032

# D:\PycharmProjects\logSorter\logs\move_directory_test\OSX_tests
# TC3268_1032

