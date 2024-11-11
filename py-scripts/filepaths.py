import os

# Function to reduce repetition of os.path.join
def makePath(*paths):
    return os.path.join(MAIN_DIR, *paths)


# Main directory
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Default directory

# Folder
GTFS = "GTFS-Daten"
GTFS_M = "GTFS-human-readable"
DJANGO_HTML = makePath("vgi_site", "folium_app", "templates")


# Data provided by VGI
XML_FILE = makePath("SIRI_VM_Test_VGI.xml") 
AGENCY_TXT = makePath(GTFS, "agency.txt")
CALENDAR_DATES_TXT = makePath(GTFS, "calendar_dates.txt")
CALENDAR_TXT = makePath(GTFS, "calendar.txt")
FEED_INFO_TXT = makePath(GTFS, "feed_info.txt")
ROUTES_TXT = makePath(GTFS, "routes.txt")
STOP_TIMES_TXT = makePath(GTFS, "stop_times.txt")
STOPS_TXT = makePath(GTFS, "stops.txt")
TRANSFERS_TXT = makePath(GTFS, "transfers.txt")
TRIPS_TXT = makePath(GTFS, "trips.txt")


# Created filepaths
JSON_FROM_XML = XML_FILE[:-4] + ".json"
STOPS_JSON = makePath(GTFS_M, "stops.json")

MAP_HTML_DJANGO = makePath(DJANGO_HTML, "map2.html")









# Function to check if a path is valid
def check_path_validity(path):
    return os.path.exists(path)

def main():
    """
    Check if provided data are valid paths
    """
    for var_name, var_value in globals().items():
        if isinstance(var_value, str) and var_value:  # Ensure var_value is a non-empty string
            if var_value.endswith('.txt') or var_value.endswith('.xml'):
                # Use assert to check if the path is valid
                assert check_path_validity(var_value), f"Invalid path: {var_name} = {var_value}"
    print("All paths are valid.")

if __name__ == "__main__":
    main()