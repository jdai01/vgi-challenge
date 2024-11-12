import folium
from folium.plugins import MarkerCluster, Search
import pandas as pd
import xmltodict
from folium import Icon, CustomIcon
from django.conf import settings
import os
from datetime import datetime
import re


def create_default_map():
    default_xml = os.path.join(settings.BASE_DIR,"folium_app","static", "default.xml")
    # print(default_xml)
    create_map(xml_filepath=default_xml)


def create_map(xml_filepath):
    #this function assumes that stops.txt isnt dynamic and wont be changed
    stops_path = os.path.join(settings.BASE_DIR,"folium_app","static", "stops.txt")
    bus_icon_path = os.path.join(settings.BASE_DIR,"folium_app","static", "sprites", "bus.png")
    bus_stop_icon_path = os.path.join(settings.BASE_DIR,"folium_app","static", "sprites", "bushaltestelle.png")
    destination_path = os.path.join(settings.BASE_DIR,"folium_app","templates", "map.html")
    # print(stops_path)

    #loading of datasets and xml file
    stops_df = pd.read_csv(stops_path)
    parent_station_list=stops_df['parent_station'].unique()
    filtered_df = stops_df[~stops_df['stop_id'].isin(parent_station_list)][['stop_id','stop_lat','stop_lon', 'stop_name']]

    with open(xml_filepath, "r", encoding="ISO-8859-1") as f:
        xml_data = f.read()
    raw_xml = xmltodict.parse(xml_data)
    live_vehicle_data = raw_xml["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"]
    timestamp = raw_xml["Siri"]["ServiceDelivery"]["ResponseTimestamp"]

    #this part just makes sure that the map starts off at the median location of the map
    mean_lat,mean_lon = filtered_df['stop_lat'].median(),filtered_df['stop_lon'].median()
    m = folium.Map(location=(mean_lat,mean_lon), zoom_start=16)

    #actual creation of map
    fg = folium.FeatureGroup(name="Bus Stop View")
    fg2 = folium.FeatureGroup(name="Live Bus View")
    m.add_child(fg)
    m.add_child(fg2)
    folium.LayerControl(collapsed=False, control=True).add_to(m)

    stops_cluster = MarkerCluster(
            name='Bus Stops',
            overlay=True,
            control=False,
            icon_create_function=None,
        ).add_to(fg)
    vehicles_cluster = MarkerCluster(
            name='Vehicles',
            overlay=True,
            control=True,
        ).add_to(fg2)

    for _, row in filtered_df.iterrows():
        bus_stop_icon = CustomIcon(icon_image=bus_stop_icon_path, icon_size=(30, 30))
        marker = folium.Marker(
            location=[row['stop_lat'], row['stop_lon']],
            popup=row['stop_name'],
            tooltip=row['stop_name'],
            icon=bus_stop_icon
        )
        stops_cluster.add_child(marker)

    #this if statement is to make sure that there are more than 1 busses in the xml
    if type(live_vehicle_data) == list:
        for vehicle in live_vehicle_data:
            try:
                lon = vehicle["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
                lat = vehicle["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
                line = vehicle["MonitoredVehicleJourney"]["LineRef"]
                destination = vehicle["MonitoredVehicleJourney"]["DestinationName"]
                delay = convert_delay(vehicle["MonitoredVehicleJourney"]["Delay"]) 
                occupation_absolute = vehicle["Extensions"]["init-o:OccupancyData"]["init-o:PassengersNumber"]
                occupation_percentage =vehicle["Extensions"]["init-o:OccupancyData"]["init-o:OccupancyPercentage"]
                monitored_call = vehicle["MonitoredVehicleJourney"]["MonitoredCall"] 
                
                try:
                    onward_call = vehicle["MonitoredVehicleJourney"]["OnwardCall"]
                except KeyError:
                    onward_call = None
                
                # Create a custom icon for the vehicles
                bus_icon = CustomIcon(icon_image=bus_icon_path, icon_size=(40, 40))
                
                # Create the popup with html content, and width
                popup_html = f"""
                    <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left; padding: 2px; background-color: white; border-radius: 5px;">
                        <meta charset="UTF-8">
                        <strong>Bus {line}</strong><br>
                        <strong>Direction: {destination}</strong><br>
                        
                        <hr style="border: 0; border-top: 1px solid #000;"/>
                        <strong>Next Stops ... <\strong><br>
                        <div style="display: flex; justify-content: space-between;">
                            <div style="text-align: left;"> - {monitored_call["StopPointName"]}</div>
                            <div style="text-align: right;">
                                <span>{convert_to_hm(monitored_call["AimedArrivalTime"])} +<\span>
                                <span style="color: {'red' if round(delay/60) >= 1 else 'green'};">{round(delay/60)}</span>
                            </div>
                        </div>
                        <hr style="border: 0; border-top: 1px solid #000;"/>
                        <strong>Bus Occupancy:</strong> {occupation_absolute} passengers, {occupation_percentage}% full
                    </div>
                """
                popup = folium.Popup(popup_html, max_width=300)  # Adjust max_width to set the width of the popup

                # Create marker for vehicle
                marker = folium.Marker(
                    location=[lat,lon],
                    popup=popup,
                    tooltip=f"Line {line} to {destination}",
                    name = line,
                    icon=bus_icon
                )
                vehicles_cluster.add_child(marker)
            except KeyError:
                # Handle the case where the vehicle data does not have valid location info
                continue
    else:
        try:
            lon = vehicle["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
            lat = vehicle["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
            line = vehicle["MonitoredVehicleJourney"]["LineRef"]
            destination = vehicle["MonitoredVehicleJourney"]["DestinationName"]
            delay = vehicle["MonitoredVehicleJourney"]["Delay"] 
            occupation_absolute = vehicle["Extensions"]["init-o:OccupancyData"]["init-o:PassengersNumber"]
            occupation_percentage =vehicle["Extensions"]["init-o:OccupancyData"]["init-o:OccupancyPercentage"]
            
            # Create a custom icon for the vehicles
            bus_icon = CustomIcon(icon_image=bus_icon_path, icon_size=(40, 40))
            
            # Create marker for vehicle
            marker = folium.Marker(
                location=[lat,lon],
                popup=f"Vehicle on Line {line} to {destination},\nDelay:{delay},\nBus Occupancy: {occupation_absolute} passengers, {occupation_percentage}% full",
                tooltip=f"Line {line} to {destination}",
                name = line,
                icon=bus_icon
            )
            vehicles_cluster.add_child(marker)
        except KeyError:
            pass
            # Handle the case where the vehicle data does not have valid location info
    


    Search(
        layer=stops_cluster,
        geom_type="Point",
        placeholder="Search for a Bus Stop",
        collapsed=True,
        search_label="tooltip",
    ).add_to(m)

    Search(
        layer=vehicles_cluster,
        geom_type="Point",
        placeholder="Search for a Bus Stop",
        collapsed=True,
        search_label="name",
    ).add_to(m)



    m.save(destination_path)


def convert_to_hm(date_str):
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%H:%M")

def convert_delay(delay_str):
    """Output: seconds (int) or None"""
    match = re.match(r"(-?P?T?(\d+)S)", delay_str)
    
    if match:
        return int(match.group(2)) if match.group(1)[0] != '-' else -int(match.group(2))
    return None