from csv_parser import CSVParser
import unittest

path_to_actual_result = '../test_GroupingByKey_result.txt'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

class CSVParserTest(unittest.TestCase):

    # must SUCCESS
    def test_grouping_by_key_SUCCESS(self):
        CSVParser.public_csv_to_curl(
            input_path='../GroupingByKey.csv',
            output_path=path_to_actual_result,
            api_url='expected_host'
        )

        with open('../ExpectedResultGroupingByKey.txt', 'r', encoding='utf-8') as expected, open(path_to_actual_result, 'r', encoding='utf-8') as actual:
            for line1, line2 in zip(expected, actual):
                self.assertEquals(line1, line2)

            print(f'\n{GREEN}Файлы равны{RESET}')

    # must FAIL
    def test_grouping_by_key_FAIL(self):
        CSVParser.public_csv_to_curl(
            input_path='../GroupingByKey.csv',
            output_path=path_to_actual_result,
            api_url='unexpected_host'
        )

        with open('../ExpectedResultGroupingByKey.txt', 'r', encoding='utf-8') as expected, open(path_to_actual_result, 'r', encoding='utf-8') as actual:
            for line1, line2 in zip(expected, actual):
                self.assertEquals(line1, line2)
