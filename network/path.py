from network.graph import NeighbourGraphBuilder

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__ method (if needed)
    - completing the "get_shortest_path" method (don't hesitate to divide your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        
        # Feel free to add anything else needed here.
        
    def validate_station_names(self, start_station_name, end_station_name):
        """ Check if station names are valid strings part of the tubemap list of stations."""
        # Check if inputs are strings
        if not (isinstance(start_station_name, str) and isinstance(end_station_name, str)):
            return False
               
        # Iterate through station instances and check if station names are there
        name_1_found = False
        name_2_found = False
        both_found = False
        name_1_id = str()
        name_2_id = str()

        for station in self.tubemap.stations.values():
            if (station.name == start_station_name) and not name_1_found:
                name_1_found = True
                name_1_id = station.id
            if (station.name == end_station_name) and not name_2_found:
                name_2_found = True
                name_2_id = station.id 

            both_found = name_1_found and name_2_found
            if both_found:
                break

        return both_found, name_1_id, name_2_id

    def get_full_path(self, end_station_id, prev_dict):
        """Create the full list of stations on from start to end station."""
        full_list = []
        current_station_id = end_station_id
        
        # Stop when previous station is None (start station reached)
        while current_station_id is not None:

            station = self.tubemap.stations[current_station_id]
            full_list.append(station)
            prev_id = prev_dict[current_station_id]
            current_station_id = prev_id 

        # Reverse list to order from start to end
        full_list.reverse()

        return full_list
        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path (in terms of duration) from start_station_name to end_station_name.

        For instance, get_shortest_path('Stockwell', 'South Kensington') should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.

        You can use the Dijkstra algorithm to find the shortest path from start_station_name to end_station_name.

        See here for more information: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not exist.
        """
        
        # Validate station names and return their id
        (are_names_valid, start_id, end_id) = self.validate_station_names(start_station_name,
                                                                          end_station_name)
        if not are_names_valid:
            # Return None if either station does not exist
            return None
        # Initialize set of unexplored stations
        unexplored_stations = {station for station in self.tubemap.stations.keys()}

        """
        # Initialize list of distances where each entry is the distance of the nth station
        dist = [float('inf')] * len(unexplored_stations)        
        dist[int(start_id)] = 0
        print(dist)
        print(len(dist))
        print(len(unexplored_stations))

        # Initialize list of previous node id
        prev_node_id = [None] * len(unexplored_stations) 
        print(prev_node_id)
        """
        
        # Initialize dictionary of distances from start to station
        dist_init = [float('inf')] * len(unexplored_stations)
        dist_dict = dict(zip(unexplored_stations,dist_init))
        dist_dict[start_id] = 0

        # Initialize dictionary of unexplored distances
        dist_unexplored_dict = dist_dict.copy()

        # Initialize dict of previous node on shortest path
        prev_node_init = [None] * len(unexplored_stations) 
        prev_dict = dict(zip(unexplored_stations,prev_node_init))   
        
        current_station_id = start_id
        while current_station_id != end_id:

            """
            # Find station from unexplored stations with shortest time
            dist_unexplored = [dist[id-2] for id in unexplored_stations]
            shortest_time = min(dist_unexplored)
            shortest_id = dist_unexplored.index(shortest_time)

            # Set unexplored station with shortest time to be current station
            current_station_id = shortest_id    

            # Remove current station from unexplored stations
            # del dist_dict[current_station_id]
            """ 

            # Find station from unexplored stations with shortest time
            shortest_time = min(dist_unexplored_dict.values())
            shortest_ids = [id for (id, dist) in dist_unexplored_dict.items() if dist==shortest_time]

            # Set unexplored station with shortest time to be current station
            current_station_id = shortest_ids[0]        

            # Remove current station from unexplored stations
            unexplored_stations.remove(current_station_id)
            del dist_unexplored_dict[current_station_id]
            
            for unexplored_id in unexplored_stations:
                try:
                    # Check if there is a connection between the two stations
                    connection_list = self.graph[current_station_id][unexplored_id]
                    
                    # Find fastest connection
                    fastest_time = connection_list[0].time
                    fastest_connection = connection_list[0]
                    # Check if any other connection is faster than the first one in the list
                    for i in range(len(connection_list)):
                        time =  connection_list[i].time
                        if time<fastest_time:
                            fastest_time = time
                            fastest_connection = connection_list[i]

                    # Update the distance to unexplored station if  
                    # the distance via current station is shorter
                    alt_distance = dist_dict[current_station_id] + fastest_time
                    if alt_distance < dist_dict[unexplored_id]:
                        dist_dict[unexplored_id] = alt_distance
                        dist_unexplored_dict[unexplored_id] = alt_distance
                        prev_dict[unexplored_id] = current_station_id                    
                except KeyError:
                    pass
 
        # print(dist_dict)
        station_path = self.get_full_path(end_id, prev_dict)

        return station_path  # TODO


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    # stations = path_finder.get_shortest_path("Ravenscourt Park", "Ravenscourt Park")
    # print(stations)

    station_names = [station.name for station in stations]
    print(station_names)
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected

def test_custom_path(station_1, station_2):
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path(station_1, station_2)
    print(stations)
    
    station_names = [station.name for station in stations]
    for station_name in station_names:
        print(station_name)

def test_all_paths_from_ravenscourt():
    import time
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    path_finder = PathFinder(tubemap)
    
    # Check for connection from Ravenscourt Park to all possible staitons
    start = time.time()
    for other_station in tubemap.stations.values():
        other_station_name = other_station.name
        print(other_station_name)

        stations = path_finder.get_shortest_path("Ravenscourt Park", other_station_name)
        # print(stations)

        # Check that a path has been calculated for all of them
        assert(stations != None)

        station_names = [station.name for station in stations]
        # print(station_names)

    end = time.time()
    total_time = end - start
    print(f"Success! It took just {total_time} seconds to check all possible paths from Ravenscourt Park.")

def test_all_paths():
    import time
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    path_finder = PathFinder(tubemap)
    
    # Check all possible combination of stations
    start = time.time()
    for station_1 in tubemap.stations.values():
            for station_2 in tubemap.stations.values():
                print((station_1.name, station_2.name))
                
                stations = path_finder.get_shortest_path(station_1.name, station_2.name)

                # Check that a path has been calculated for all of them
                assert(stations != None)

                # station_names = [station.name for station in stations]
                # print(station_names)
    end = time.time()
    total_time = end - start
    print(f"Success! It took just {total_time} seconds check all possible connections")

if __name__ == "__main__":
    # test_shortest_path()

    # Test my way to my friend's house
    test_custom_path("Ravenscourt Park", "Elephant & Castle")

    # Test very far stations
    test_custom_path("Heathrow Terminal 4", "Grange Hill")

    # Test my way to Imperial
    test_custom_path("Ravenscourt Park", "South Kensington")

    # Test random
    test_custom_path("Oxford Circus", "Charing Cross")

    # Test same start and end
    test_custom_path("Oxford Circus", "Oxford Circus")

    # Test all paths from Ravenscourt Park
    # test_all_paths_from_ravenscourt()

    # Test all possible combinations for errors or infinite loops
    # test_all_paths()
