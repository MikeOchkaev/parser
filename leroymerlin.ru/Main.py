import os
from dotenv import load_dotenv
import CSVParser

load_dotenv()

input_path = os.getenv('INPUT_PATH')
output_path = os.getenv('OUTPUT_PATH')
api_url = os.getenv('API_URL')

if __name__ == "__main__":
    CSVParser.csv_to_json(input_path, output_path)
