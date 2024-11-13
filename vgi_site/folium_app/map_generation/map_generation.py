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
    destination = os.path.join(settings.BASE_DIR,"folium_app","templates", "default_map.html")
    # print(default_xml)
    create_map(xml_filepath=default_xml,output_file=destination)


def create_map(xml_filepath,output_file=os.path.join(settings.BASE_DIR,"folium_app","templates", "map.html")):
    #this function assumes that stops.txt isnt dynamic and wont be changed
    stops_path = os.path.join(settings.BASE_DIR,"folium_app","static", "stops.txt")
    bus_icon_path_red = os.path.join(settings.BASE_DIR,"folium_app","static", "sprites", "bus-red.png")
    bus_icon_path_orange = os.path.join(settings.BASE_DIR,"folium_app","static", "sprites", "bus-orange.png")
    bus_icon_path_green = os.path.join(settings.BASE_DIR,"folium_app","static", "sprites", "bus-green.png")
    bus_stop_icon_path = os.path.join(settings.BASE_DIR,"folium_app","static", "sprites", "bushaltestelle.png")
    # print(stops_path)

    #loading of datasets and xml file
    stops_df = pd.read_csv(stops_path)
    parent_station_list=stops_df['parent_station'].unique()
    filtered_df = stops_df[~stops_df['stop_id'].isin(parent_station_list)][['stop_id','stop_lat','stop_lon', 'stop_name']]

    with open(xml_filepath, "r", encoding="ISO-8859-1") as f:
        xml_data = f.read()
    raw_xml = xmltodict.parse(xml_data, force_list=("VehicleActivity"))
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
            icon=bus_stop_icon,
            name = row['stop_name']
        )
        stops_cluster.add_child(marker)

    #this if statement is to make sure that there are more than 1 busses in the xml
    for vehicle in live_vehicle_data:
        try:
            lon = vehicle["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
            lat = vehicle["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
            line = bus_line(vehicle["MonitoredVehicleJourney"]["LineRef"])
            destination = vehicle["MonitoredVehicleJourney"]["DestinationName"]
            delay = convert_delay(vehicle["MonitoredVehicleJourney"]["Delay"]) 
            occupation_absolute = vehicle["Extensions"]["init-o:OccupancyData"]["init-o:PassengersNumber"]
            occupation_percentage = int(vehicle["Extensions"]["init-o:OccupancyData"]["init-o:OccupancyPercentage"]) / 100
            monitored_call = vehicle["MonitoredVehicleJourney"]["MonitoredCall"] 
            # print(monitored_call["StopPointName"])
            
            try:
                onward_calls = vehicle["MonitoredVehicleJourney"]["OnwardCalls"]["OnwardCall"]
            except KeyError:
                onward_calls = None
            
            # Create a custom icon for the vehicles
            if occupation_percentage > 0.7:
                icon_path = bus_icon_path_red
            elif occupation_percentage > 0.5:
                icon_path = bus_icon_path_orange
            else:
                icon_path = bus_icon_path_green
            bus_icon = CustomIcon(icon_image=icon_path, icon_size=(40, 40))
            
            # Create html file for popup
            header = f"""
                <div style="font-size: 12px; font-family: Arial, sans-serif; text-align: left; padding: 2px; background-color: white; border-radius: 2px;">
                    <meta charset="UTF-8">
                    <strong>
                        Line {line}<br>
                        Direction: {destination}
                    </strong><br>
            """
            content = f"""
                <hr style="border: 0; border-top: 1px solid #000;"/>
                <strong>Next Stops ... </strong><br>
                <div style="display: flex; justify-content: space-between; font-weight: bold;">
                    <div style="text-align: left; padding-right: 5px;"> - {monitored_call["StopPointName"]}</div>
                    <div style="text-align: right;">
                        <span>{convert_to_hm(monitored_call["AimedArrivalTime"])} +</span>
                        <span style="color: {'red' if round(delay/60) >= 1 else 'green'};">{round(delay/60)}</span>
                    </div>
                </div>
            """
            footer = f"""
                <hr style="border: 0; border-top: 1px solid #000;"/>
                <strong>Bus Occupancy:</strong> {occupation_absolute} passengers, {occupation_percentage * 100}% full
            </div>
            """

            if onward_calls:
                for i in range(min(len(onward_calls), 5)):
                    next_stop = onward_calls[i]
                    content += f"""
                    <div style="display: flex; justify-content: space-between;">
                        <div style="text-align: left; padding-right: 5px;"> - {next_stop["StopPointName"]}</div>
                        <div style="text-align: right;">
                            <span>{convert_to_hm(next_stop["AimedArrivalTime"])} +</span>
                            <span style="color: {'red' if round(delay/60) >= 1 else 'green'};">{round(delay/60)}</span>
                        </div>
                    </div>
                    """
                if len(onward_calls) > 5:
                    content += f"""
                    <div style="display: flex; justify-content: space-between;">   ...</div>
                    """

            popup_html = header + content + footer
            popup = folium.Popup(popup_html, max_width=400)  # Adjust max_width to set the width of the popup

            # Create marker for vehicle
            marker = folium.Marker(
                location=[lat,lon],
                popup=popup,
                tooltip=f"Line {line} to {destination}",
                name = f"Line {line} to {destination}",
                icon=bus_icon
            )
            vehicles_cluster.add_child(marker)
        except KeyError:
            # Handle the case where the vehicle data does not have valid location info
            continue

    


    Search(
        layer=stops_cluster,
        geom_type="Point",
        placeholder="Search for a Bus Stop",
        collapsed=True,
        search_label="name",
    ).add_to(m)

    Search(
        layer=vehicles_cluster,
        geom_type="Point",
        placeholder="Search for a Bus Line",
        collapsed=True,
        search_label="name",
    ).add_to(m)



    m.save(output_file)


def convert_to_hm(date_str):
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%H:%M")

def convert_delay(delay_str):
    """Output: seconds (int) or 0"""
    match = re.match(r"(-?P?T?(\d+)S)", delay_str)
    
    if match:
        return int(match.group(2)) if match.group(1)[0] != '-' else 0
    return None

def bus_line(line):
    if line.startswith("INVG"):
        return line[4:]  # Removes the first 4 characters ("INVG")
    return line  # If "INVG" is not present, return the line as is