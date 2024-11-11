import os
import json
import xmltodict

from LoadBusInfo import Vehicle
from filepaths import *



def convert_xml(xml_file: str):
    # Open the XML file and read its content
    with open(xml_file, "r", encoding="ISO-8859-1") as f:
        xml_data = f.read()

    # Convert XML to a Python dictionary
    dict_data = xmltodict.parse(xml_data)

    # Convert the dictionary to JSON format
    json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)

    # Write the dictionary to a JSON file
    with open(JSON_FROM_XML, "w", encoding="utf-8") as file:
        json.dump(dict_data, file, indent=4, ensure_ascii=False)

    return dict_data


def get_vehicle_info(json_data):
    # Extract the list from "VehicleActivity"
    vehicle_activity_list = json_data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"]

    return vehicle_activity_list



def main():
    # Check if file exists
    assert os.path.exists(XML_FILE), f"File path is incorrect or file '{XML_FILE}' does not exist in {MAIN_DIR}"
    
    print(JSON_FROM_XML)

    # Get JSON data from XML file
    json_data = convert_xml(XML_FILE)
    vehicle_info_list = get_vehicle_info(json_data) # -> list of vehicles info

    # Get vehicle info
    vehicle_activity_list = []
    for bus in vehicle_info_list:
        vehicle_activity_list.append(Vehicle(bus))

    # # Test print
    # for i in vehicle_activity_list:
    #     print(i.LineRef)

    







if __name__ == "__main__":
    main()