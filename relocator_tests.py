import glob
import os
import relocator as r
import shutil
import unittest


class FinalTest(unittest.TestCase):

    path = r'D:\PycharmProjects\logSorter\relocator_tests'

    def setUp(self):
        os.chdir(self.path)

    def create_envionment(self):
        os.chdir(self.path)
        actual = os.listdir('./')
        required = ['TC0000_0000', 'destination']

        if actual != required:
            shutil.rmtree(self.path, ignore_errors=True)
            s = 'D:\PycharmProjects\logSorter\Test directories'
            d = self.path
            r.move_single_directory(s, d, required[0])
            os.mkdir('./destination')

    def test_move_single_directory(self):
        self.create_envionment()

if __name__ == '__main__':
    unittest.main()
