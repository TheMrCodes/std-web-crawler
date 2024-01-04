"""
This file is a script that converts a csv file to a parquet file.
"""

import pandas as pd
import dotenv
import os
from typing import NoReturn
dotenv.load_dotenv()

def error(msg: str) -> NoReturn:
    raise ValueError(msg)

# Script Variables
OUTPUT_DIR = os.getenv("APP_OUTPUT_DIR") or error("APP_OUTPUT_DIR not set!")
INPUT_FILE = 'urls.csv'
OUTPUT_FILE = 'urls.parquet'


def convert_csv_to_parquet():
    # Read the CSV file into a pandas DataFrame
    print('Reading CSV file...')
    df = pd.read_csv(OUTPUT_DIR +'/'+ INPUT_FILE, sep=';', dtype={'loc': str, 'lastmod': str}, quotechar='"', encoding='utf-8')
    
    # Convert the DataFrame to Parquet format
    print('Converting to Parquet...')
    df.to_parquet(OUTPUT_DIR +'/'+ OUTPUT_FILE, index=False)


if __name__ == "__main__":
    convert_csv_to_parquet()
