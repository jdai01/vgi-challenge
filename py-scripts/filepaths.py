import os

# Main directory
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Default directory

# Folder
GTFS = "GTFS-Daten"
GTFS_M = "GTFS-human-readable"


# Data provided by VGI
XML_FILE = os.path.join(MAIN_DIR, "SIRI_VM_Test_VGI.xml") 
AGENCY_TXT = os.path.join(MAIN_DIR, GTFS, "agency.txt")
CALENDAR_DATES_TXT = os.path.join(MAIN_DIR, GTFS, "calendar_dates.txt")
CALENDAR_TXT = os.path.join(MAIN_DIR, GTFS, "calendar.txt")
FEED_INFO_TXT = os.path.join(MAIN_DIR, GTFS, "feed_info.txt")
ROUTES_TXT = os.path.join(MAIN_DIR, GTFS, "routes.txt")
STOP_TIMES_TXT = os.path.join(MAIN_DIR, GTFS, "stop_times.txt")
STOPS_TXT = os.path.join(MAIN_DIR, GTFS, "stops.txt")
TRANSFERS_TXT = os.path.join(MAIN_DIR, GTFS, "transfers.txt")
TRIPS_TXT = os.path.join(MAIN_DIR, GTFS, "trips.txt")


# Created filepaths
JSON_FROM_XML = XML_FILE[:-4] + ".json"
STOPS_JSON = os.path.join(MAIN_DIR, GTFS_M, "stops.json")










# Function to check if a path is valid
def check_path_validity(path):
    return os.path.exists(path)

def main():
    for var_name, var_value in globals().items():
        if isinstance(var_value, str) and var_value:  # Ensure var_value is a non-empty string
            if var_value.endswith('.txt') or var_value.endswith('.xml'):
                # Use assert to check if the path is valid
                assert check_path_validity(var_value), f"Invalid path: {var_name} = {var_value}"
    print("All paths are valid.")

if __name__ == "__main__":
    main()