from csv_parser import CSVParser
import unittest

path_to_actual_result = '../test_GroupingByKey_result.txt'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

class CSVParserTest(unittest.TestCase):

    def test_grouping_by_key_SUCCESS(self):
        CSVParser.csv_to_curl(
            input_path='../GroupingByKey.csv',
            output_path=path_to_actual_result,
            api_url='expected_host'
        )

        with open('../ExpectedResultGroupingByKey.txt', 'r', encoding='utf-8') as expected, open(path_to_actual_result, 'r', encoding='utf-8') as actual:
            for line1, line2 in zip(expected, actual):
                if line1 != line2:
                    raise RuntimeError(f'{RED}Файлы не равны{RESET}')

            print(f'\n{GREEN}Файлы равны{RESET}')

    # should throw exception
    def test_grouping_by_key_FAILURE(self):
        CSVParser.csv_to_curl(
            input_path='../GroupingByKey.csv',
            output_path=path_to_actual_result,
            api_url='unexpected_host'
        )

        with open('../ExpectedResultGroupingByKey.txt', 'r', encoding='utf-8') as expected, open(path_to_actual_result, 'r', encoding='utf-8') as actual:
            for line1, line2 in zip(expected, actual):
                if line1 != line2:
                    raise RuntimeError(f'{RED}Файлы не равны{RESET}')

            print(f'\n{GREEN}Файлы равны{RESET}')
