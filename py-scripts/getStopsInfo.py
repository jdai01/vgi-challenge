import csv
import json

from filepaths import *

# List to hold the processed data
stops_data = []

# Open the CSV file and read the contents
with open(STOPS_TXT, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    # Process each row
    for row in csv_reader:
        # Check if stop_id starts with 'V', and skip if so
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
with open(STOPS_JSON, 'w', encoding='utf-8') as json_file:
    json.dump(stops_data, json_file, indent=4)

print(f"Data has been successfully written to {STOPS_JSON}")
