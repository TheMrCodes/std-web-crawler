"""
This file is a script that converts a csv file to a parquet file.
"""

import pandas as pd

# Script Variables
INPUT_FILE = 'out/urls.csv'
OUTPUT_FILE = 'out/urls.parquet'


def convert_csv_to_parquet():
    # Read the CSV file into a pandas DataFrame
    print('Reading CSV file...')
    df = pd.read_csv(INPUT_FILE)
    
    # Convert the DataFrame to Parquet format
    print('Converting to Parquet...')
    df.to_parquet(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    convert_csv_to_parquet()
