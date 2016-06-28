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

        # Remove tests directories
        for crap in glob.glob('*_tests'):
            shutil.rmtree(crap)

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
        id = y.get_test_case_data()[2]
        actual = [
          id.tc_id,
          id.tc_name,
          id.group_name,
          id.tc_status
        ]
        expected = ['TC1000_2135', 'FIRSTPART_UBUNTU_12', 'Ubuntu_tests', 'PASSED']
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
