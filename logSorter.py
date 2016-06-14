import glob
import re
import os


class LogBrowser(object):

    def get_directories(self, path):
        search_directory = os.listdir(path)
        wanted_directories = []
        for directory in search_directory:
            if re.match('TC[0-9]+', directory):
                wanted_directories.append(directory)
        return wanted_directories

    def get_test_case(self, file, pattern):
        log = open(file, 'r')
        try:
            search_string = log.readlines()
            for line in search_string:
                print(line)
                test_name = self.find_test_name(line[:-1], pattern)
                if test_name is not False and test_name[0] is 'ZSUBUNTU_12':
                    return test_name
        except ValueError:
            raise('%s not found.' % pattern)
        finally:
            log.close()

    def find_test_name(self, search_line, pattern):
        test_name = re.search(pattern, search_line)
        match = test_name.group()
        if type(match) is not None:
            return match
        else:
            return False


class TestCase(object):

    def __init__(self, TCid, test_group, status):
        self.TCid = TCid
        self.test_group = test_group
        self.status = status


# init_class = LogBrowser()
# os.chdir('./logs/TC1000_2135')
# file_name = 'TC1000_2135.log'
# found_name = init_class.get_test_case(file_name, 'ZSUBUNTU_([0-9]+)')
# expected_name = 'ZSUBUNTU_12'

# na później
# (ZSUBUNTU_[0-9])\w
# (?:abc)	non-capturing group