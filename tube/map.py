import json
from tube.components import Station, Line, Connection

class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json" method (don't hesitate to divide your code into several sub-methods, if needed)

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id (key=id, value=Station)
    - lines: a dictionary that indexes Line instances by their id (key=id, value=Line)
    - connections: a list of Connection instances for the tube map (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id, value: Station
        self.lines = {}  # key: id, value: Line
        self.connections = []  # list of Connections

    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During that import, the `stations`, `lines` and `connections` attributes should be updated.

        You can use the `json` python package to easily load the JSON file at `filepath`

        Note: when the indicated zone is not an integer (for instance: 2.5), 
            it means that the station is in two zones at the same time. 
            For example, if the zone of a station is "2.5", 
            it means that station is in zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to import

        Returns:
            None

        Note:
            If the filepath is invalid, no attribute should be updated, and no error should be raised.
        """
        
        # Read from filepath and return if read fails
        try:
            with open(filepath, "r") as jsonfile:
                data = json.load(jsonfile)
        except FileNotFoundError:
            return
            
        # Convert stations to dictionary
        all_stations = data["stations"]
        station_dict = dict()
        for station in all_stations:
            id = station["id"]
            name = station["name"]
            zone = float(station["zone"])

            # Convert non integer zones to a set of 2 zones
            if (zone % 1) == 0.5:
                zones = {int(zone-0.5), int(zone+0.5)}
            else:
                zones = {int(zone)}

            # Create station instance with extracted information
            station_instance = Station(id=id,
                                       name=name,
                                       zones=zones)
            station_dict.update({id: station_instance})

        self.stations = station_dict

        # Convert lines to dictionary
        all_lines = data["lines"]
        line_dict = dict()
        for line in all_lines:
            id = line["line"]
            name = line["name"]

            # Create line instance with extracted information
            line_instance = Line(id=id, name=name)
            line_dict.update({id: line_instance})

        self.lines = line_dict

        # Convert connections to list
        all_connections = data["connections"]
        connection_list = list()
        for connection in all_connections:
            id_station1 = connection["station1"]
            id_station2 = connection["station2"]

            # Find the 2 station instances using their ids
            station1 = self.stations[id_station1]
            station2 = self.stations[id_station2]

            # Find the corresponding Line instance using the line id
            id_line = connection["line"]
            line = self.lines[id_line]

            time_str = connection["time"]
            time = int(time_str)
  
            # Create connection instance using extracted information
            connection_instance = Connection(stations={station1, station2},
                                                       line=line,
                                                       time=time)
            connection_list.append(connection_instance)

        self.connections = connection_list

        return


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":

    test_import()
