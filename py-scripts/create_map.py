import folium
from folium.plugins import MarkerCluster, Search
import pandas as pd
import json
from folium import Icon, CustomIcon

from filepaths import * 
from LoadBusInfo import main as load_bus_main, Vehicle


def create_bus_stop_and_vehicle_map(stop_data, vehicle_data, map_filename="map.html"):
    """
    Creates a folium map with bus stop markers, vehicle markers, clustering, and search functionality.

    Parameters:
    - stop_data: A list of dictionaries containing 'stop_lat', 'stop_lon', 'stop_name', and 'stop_id'.
    - vehicle_data: A list of Vehicle objects containing location information for active vehicles.
    - map_filename: Name of the HTML file where the map will be saved (default: 'map.html').
    """
    # Convert the stop data to a pandas DataFrame
    stops_df = pd.DataFrame(stop_data)

    # Create the base map centered on a specific location
    m2 = folium.Map(location=(48.7624060, 11.4257570), zoom_start=16)

    # Create feature groups for different layers (bus stops, live bus view, and vehicles)
    fg = folium.FeatureGroup(name="Bus Stop View")
    fg2 = folium.FeatureGroup(name="Live Bus View")

    # Add feature groups to the map
    m2.add_child(fg)
    m2.add_child(fg2)

    # Add LayerControl to allow toggling layers
    folium.LayerControl(collapsed=False, control=True).add_to(m2)

    # Create a marker cluster for bus stops
    stops_cluster = MarkerCluster(
        name='Bus Stops',
        overlay=True,
        control=False,
        icon_create_function=None,
    ).add_to(fg)

    # Add markers for each bus stop in the DataFrame
    for _, row in stops_df.iterrows():
        bus_stop_icon = CustomIcon(icon_image=BUSSTOP_PNG, icon_size=(30, 30))
        marker = folium.Marker(
            location=[row['stop_lat'], row['stop_lon']],
            popup=row['stop_name'],
            tooltip=row['stop_name'],
            icon=bus_stop_icon
        )
        stops_cluster.add_child(marker)

    # Add search functionality for bus stops
    stops_search = Search(
        layer=stops_cluster,
        geom_type="Point",
        placeholder="Search for a Bus Stop",
        collapsed=True,
        search_label="name",
    ).add_to(m2)

    # Create a marker cluster for vehicles
    vehicles_cluster = MarkerCluster(
        name='Vehicles',
        overlay=True,
        control=True,
    ).add_to(fg2)

    # Add markers for each vehicle's location from the Vehicle data
    for vehicle in vehicle_data:
        try:
            lat = float(vehicle.VehicleLocation["Latitude"])
            lon = float(vehicle.VehicleLocation["Longitude"])
            
            # Create a custom icon for the vehicles
            vehicle_icon = CustomIcon(icon_image=BUS_PNG, icon_size=(40, 40))
            
            # Create marker for vehicle
            marker = folium.Marker(
                location=[lat, lon],
                popup=f"Vehicle on Line {vehicle.LineRef}: {vehicle.OriginName} to {vehicle.DestinationName}",
                tooltip=f"Vehicle: {vehicle.LineRef}",
                icon=vehicle_icon
            )
            vehicles_cluster.add_child(marker)
        except KeyError:
            # Handle the case where the vehicle data does not have valid location info
            continue

    # Save the map as an HTML file
    m2.save(map_filename)
    print(f"Map saved as {map_filename}")


def load_stop_data_from_json(json_filename):
    """
    Loads the bus stop data from a JSON file.

    Parameters:
    - json_filename: The path to the JSON file containing the bus stop data.

    Returns:
    - A list of dictionaries with the bus stop information.
    """
    with open(json_filename, 'r', encoding='utf-8') as f:
        stop_data = json.load(f)
    
    # Ensure the stop data is in the correct format
    formatted_data = [{
        'stop_id': stop['stop_id'],
        'stop_name': stop['stop_name'],
        'stop_lat': float(stop['stop_lat']),
        'stop_lon': float(stop['stop_lon'])
    } for stop in stop_data]
    
    return formatted_data


def load_vehicle_data_from_json(json_filename):
    """
    Loads the vehicle data from a JSON file.
    """

    # Run the main function from LoadBusInfo to ensure required data is loaded or prepared
    load_bus_main()

    with open(json_filename, 'r', encoding='utf-8') as f:
        vehicle_data = json.load(f)

    # Extract vehicle information and create Vehicle objects
    vehicle_objects = [Vehicle(vehicle) for vehicle in vehicle_data]

    return vehicle_objects


def main():
    """
    Main function to load bus stop and vehicle data, then generate the map.
    """
    # Load the bus stop data from the JSON file
    stop_data = load_stop_data_from_json(STOPS_JSON)
    
    # Load the vehicle data from the JSON file
    vehicle_data = load_vehicle_data_from_json(VEHICLE_ACTIVITY_JSON)

    # Generate and save the map with bus stop and vehicle data
    create_bus_stop_and_vehicle_map(stop_data, vehicle_data, MAP_HTML_DJANGO)


if __name__ == "__main__":
    main()
