import os
import json
import xmltodict
from datetime import datetime

class Vehicle:
    """
    Class to represent a vehicle and its data.
    """

    def __init__(self, info):
        """
        Initialize the vehicle with data.
        """
        # Recorded Info
        self.RecordedAtTime = info["RecordedAtTime"]                    # dtype: str / datetime
        self.ProgressBetweenStops = info["ProgressBetweenStops"]        # dtype: dict

        # Bus Info
        busInfo = info["MonitoredVehicleJourney"]
        self.LineRef = busInfo["LineRef"]                               # dtype: str
        self.OriginName = busInfo["OriginName"]                         # dtype: str
        self.DestinationName = busInfo["DestinationName"]               # dtype: str
        self.Monitored = busInfo["Monitored"]                           # dtype: bool
        self.InCongestion = busInfo["InCongestion"]                     # dtype: bool
        self.InPanic = busInfo["InPanic"]                               # dtype: bool
        self.VehicleLocation = busInfo["VehicleLocation"]               # dtype: dict
        self.Delay = busInfo["Delay"]                                   # dtype: str
        self.PreviousCalls = None                                       # dtype: list / None
        self.MonitoredCall = busInfo["MonitoredCall"]                   # dtype: dict
        self.OnwardCalls = None                                         # dtype: list / None

        # Retrieve additional call information if available
        self._extract_additional_calls(busInfo)

        # Fix data types (e.g., datetime)
        self._fix_data_types()

    def _extract_additional_calls(self, bus_info):
        """
        Extract extra call data if available (PreviousCalls, OnwardCalls).
        """
        try:
            self.PreviousCalls = bus_info["PreviousCalls"]["PreviousCall"]
        except KeyError:
            pass  # No PreviousCalls

        try:
            self.OnwardCalls = bus_info["OnwardCalls"]["OnwardCall"]
        except KeyError:
            pass  # No OnwardCalls

    def _fix_data_types(self):
        """
        Fix data types, such as converting string to datetime.
        """
        self.RecordedAtTime = self._cast_to_datetime(self.RecordedAtTime)

    @staticmethod
    def _cast_to_datetime(dt_str: str):
        """
        Convert string to datetime.
        """
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f%z")

    def to_dict(self):
        """
        Convert the vehicle data to a dictionary.
        """
        return {
            "RecordedAtTime": self.RecordedAtTime.isoformat() if isinstance(self.RecordedAtTime, datetime) else self.RecordedAtTime,
            "ProgressBetweenStops": self.ProgressBetweenStops,
            "LineRef": self.LineRef,
            "OriginName": self.OriginName,
            "DestinationName": self.DestinationName,
            "Monitored": self.Monitored,
            "InCongestion": self.InCongestion,
            "InPanic": self.InPanic,
            "VehicleLocation": self.VehicleLocation,
            "Delay": self.Delay,
            "PreviousCalls": self.PreviousCalls,
            "MonitoredCall": self.MonitoredCall,
            "OnwardCalls": self.OnwardCalls
        }




def parse_xml(xml_file: str):
    """
    Convert an XML file to JSON format and save it.
    """
    with open(xml_file, "r", encoding="ISO-8859-1") as f:
        xml_data = f.read()

    # Convert XML to dictionary
    dict_data = xmltodict.parse(xml_data)

    return dict_data
