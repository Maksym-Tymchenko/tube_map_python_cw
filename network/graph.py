from tube.map import TubeMap


class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code into several sub-methods, if needed)
    """

    def __init__(self):
        pass

    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building the graph.

        Return:
            graph (dict) : as described above.

        Note:
            If the input data (tubemap) is invalid, the method should return an empty dict.
        """

        # Initialize graph
        graph = dict() 
       
        # Check if tubemap input is valid, if not return empty dictionary
        if not isinstance(tubemap, TubeMap):
            return graph


        # Iterate over Connections and add each to corresponding place in graph
        for connection in tubemap.connections:
            (station_1, station_2) = connection.stations
            id_station_1 = station_1.id
            id_station_2 = station_2.id
            
            try:
                # Check if there is an existing list of connections for this combination of stations
                existing_list = graph[id_station_1][id_station_2]

                # Append the connection to the existing list of connections
                existing_list.append(connection)

            except KeyError:
                try:
                    # Check if there is an existing dictionary for station 1
                    test = graph[id_station_1]

                    # Add new item containing the connection to station 2
                    graph[id_station_1][id_station_2] = [connection]

                except KeyError:
                    # If there is no existing dictionary for station 1 create it and add connection
                    graph[id_station_1] = dict()
                    graph[id_station_1][id_station_2] = [connection]

        # Make connections symmetrical
        for key_1 in list(graph):
            for key_2 in list(graph[key_1]):
                try:
                    # Check if key_2 exists in graph, if so make symmetrical
                    test = graph[key_2]
                    graph[key_2][key_1] = graph[key_1][key_2]           
                except KeyError:
                    # If there is no existing dictionary for key_2 create it and make symmetrical
                    graph[key_2] = dict()
                    graph[key_2][key_1] = graph[key_1][key_2]

        return graph


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(graph)


if __name__ == "__main__":
    test_graph()
