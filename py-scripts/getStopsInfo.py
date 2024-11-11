import csv
import json
from filepaths import *

def process_stops_data(input_file, output_file):
    """
    Processes the CSV file containing stop data, filters out stops with 'stop_id' starting with 'V',
    and writes the filtered data to a JSON file.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output JSON file.
    """
    stops_data = []

    # Open the CSV file and read the contents
    with open(input_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        # Process each row
        for row in csv_reader:
            # Skip if stop_id starts with 'V'
            if row['stop_id'].startswith('V'):
                continue
            
            # Extract the required fields and add them to the list
            stop_info = {
                'stop_id': row['stop_id'],
                'stop_name': row['stop_name'],
                'stop_lat': row['stop_lat'],
                'stop_lon': row['stop_lon']
            }
            stops_data.append(stop_info)

    # Write the filtered data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(stops_data, json_file, indent=4)

    print(f"Data has been successfully written to {output_file}")

def main():
    process_stops_data(STOPS_TXT, STOPS_JSON)

if __name__ == "__main__":
    main()
