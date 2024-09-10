from csv_parser import CSVParser
import os
from dotenv import load_dotenv

load_dotenv()

input_path = os.getenv('INPUT_PATH')
output_path = os.getenv('OUTPUT_PATH')
api_url = os.getenv('API_URL')

# In order to start processing
if __name__ == "__main__":
    CSVParser.csv_to_curl(
        input_path=input_path,
        output_path=output_path,
        api_url=api_url
    )
