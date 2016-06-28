import glob
import os
import shutil
import unittest

from ddt import ddt, data
from logSorter import DirectoryManagement


@ddt
class FinalTest(unittest.TestCase):

    def setUp(self):
        os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs')

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

        self.remove_test_directories()

        created_groups = y.create_test_group()
        actual = created_groups.keys()
        expected = ['OSX_tests', 'Ubuntu_tests', 'Windows_tests']
        self.assertEqual(sorted(actual), expected)

    def test_sort_tests_into_groups(self):
        y = DirectoryManagement()
        y.create_group_directory2()

        self.remove_test_directories()

        # Get required test data.
        test_cases = y.get_test_cases()
        created_groups = y.create_test_group()

        # Tested method.
        y.sort_test_cases_into_groups(test_cases, created_groups)

        first_test = created_groups['Ubuntu_tests'].test_cases[0].tc_name
        second_test = created_groups['Windows_tests'].test_cases[0].tc_name
        third_test = created_groups['OSX_tests'].test_cases[0].tc_name

        self.assertEqual(first_test, 'FIRSTPART_UBUNTU_12')
        self.assertEqual(second_test, 'FIRSTPART_Windows_452')
        self.assertEqual(third_test, 'FIRSTPART_OSX_87')

if __name__ == '__main__':
    unittest.main()
