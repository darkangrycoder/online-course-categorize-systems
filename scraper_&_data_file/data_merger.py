import os
import pandas as pd


def find_csv_files(directory):
    csv_files = [filename for filename in os.listdir(
        directory) if filename.endswith('.csv')]
    return csv_files

# Function to get output filename based on input filename


def get_output_filename(input_filename):
    base_name, _ = os.path.splitext(input_filename)
    return f"{base_name}_details.csv"


try:
    current_directory = os.getcwd()
    csv_files = find_csv_files(current_directory)

finally:
    print(csv_files)
