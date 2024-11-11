# Import modules
import json
from datetime import datetime

class Vehicle():
    """
    Retrieval of bus information from 'vehicle_activity.json'
    """

    def __init__(self, info):
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

        # Retrival of "PreviousCalls" and/or "OnwardCalls", when available
        try:
            self.PreviousCalls = busInfo["PreviousCalls"]["PreviousCall"]
        except Exception:
            pass

        try:
            self.OnwardCalls = busInfo["OnwardCalls"]["OnwardCall"]
        except Exception:
            pass




        # Initialised functions
        self.fixDataType()


    def fixDataType(self):
        self.RecordedAtTime = self.castDateTime(self.RecordedAtTime)

    @staticmethod
    def castDateTime(dt_str: str):
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f%z")

    def to_dict(self):
        # Convert the instance's attributes into a dictionary
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

    def to_json(self, filename):
        data = self.to_dict()

        # Write the dictionary to a JSON file
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)



if __name__ == "__main__":
    vehicle_activity_json = "vehicle_activity.json"

    # Load vehicle_activity_json
    with open(vehicle_activity_json, 'r') as f:
        data = json.load(f)

    # Get all vehicle essential data (list of Vehicle class)
    vehicle_activity_list = []
    for bus in data:
        vehicle_activity_list.append(Vehicle(bus))
