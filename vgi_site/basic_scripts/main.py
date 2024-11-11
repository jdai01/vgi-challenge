import os
import json
import xmltodict

from LoadBusInfo import Vehicle


# Initialise filenames
XML_FILE = "SIRI_VM_Test_VGI.xml"
JSON_FILE = XML_FILE[:-4] + ".json"
vehicle_activity_json = "vehicle_activity.json"

# Create the full path for XML_FILE
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Default directory
XML_FILEPATH = os.path.join(PARENT_DIR, XML_FILE) 



def convert_xml(xml_file: str):
    # Open the XML file and read its content
    with open(xml_file, "r", encoding="ISO-8859-1") as f:
        xml_data = f.read()

    # Convert XML to a Python dictionary
    dict_data = xmltodict.parse(xml_data)

    # Convert the dictionary to JSON format
    json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)

    # Write the dictionary to a JSON file
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(dict_data, file, indent=4, ensure_ascii=False)

    return dict_data


def get_vehicle_info(json_data):
    # Extract the list from "VehicleActivity"
    vehicle_activity_list = json_data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"]

    return vehicle_activity_list



def main():
    # Check if file exists
    assert os.path.exists(XML_FILEPATH), f"File path is incorrect or file '{XML_FILE}' does not exist in {PARENT_DIR}"
    
    # Get JSON data from XML file
    json_data = convert_xml(XML_FILEPATH)
    vehicle_info_list = get_vehicle_info(json_data) # -> list of vehicles info

    # Get vehicle info
    vehicle_activity_list = []
    for bus in vehicle_info_list:
        vehicle_activity_list.append(Vehicle(bus))

    # Test print
    # for i in vehicle_activity_list:
    #     print(i.LineRef)

    







if __name__ == "__main__":
    main()