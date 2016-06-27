import glob
import logging
import os
import shutil
import unittest


from logSorter import DirectoryManagement
from logSorter import TestCase as TC


class FinalTest(unittest.TestCase):
    def setUp(self):
        os.chdir('D:\PycharmProjects\logSorter\directory_management_test_logs')

    def test_get_search_directories(self):
        y = DirectoryManagement()
        y.get_search_directories()
        expected_directories = ['TC0000_0000', 'TC1000_2135', 'TC3267_1032', 'TC3268_1032']
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

    def test_get_test_case_status(self):
        x = DirectoryManagement()
        x.go_into_directory('TC1000_2135')
        status = x.get_test_case_status('TC1000_2135.log')
        expected = 'PASSED'
        x.return_to_main_directory()
        self.assertEqual(status, expected)

    # def test_single_test_case(self):
    #     y = DirectoryManagement()
    #     id = y.get_test_case_data('TC1000')
    #     actual = [
    #       id.tc_id,
    #       id.tc_name,
    #       id.group_name,
    #       id.tc_status
    #     ]
    #     expected = ['TC1000', 'FIRSTPART_UBUNTU_12', 'Ubuntu_tests', 'PASSED']
    #     self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
