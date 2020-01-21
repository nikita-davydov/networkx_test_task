from typing import Tuple

import networkx as nx
import sys


def get_shortest_way(point_a: str, point_b: str, graph: nx.Graph) -> Tuple[int, list]:
    g_path = nx.shortest_path(graph, point_a, point_b, weight='weight')

    minutes_to_reach = 0

    for source_node, target_node in zip(g_path, g_path[1:]):
        edge = graph.edges[source_node, target_node]
        minutes_to_reach += edge['distance_in_minutes']
    return minutes_to_reach, g_path


def parse_graph(lines_list: list) -> nx.Graph:
    graph = nx.Graph()
    for line in lines_list:
        city1, city2, distance_in_minutes = line.split(',')
        graph.add_edge(
            city1,
            city2,
            distance_in_minutes=int(distance_in_minutes),
        )
    return graph


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('You have to specify input file name')

    file_name = sys.argv[1]
    file = open(file_name, 'r')
    lines = [line.replace('\n', '') for line in file.readlines()]
    file.close()

    a, b = lines.pop(0).split(',')
    minutes, g_path = get_shortest_way(a, b, parse_graph(lines))

    cities_in_shortest_way = ','.join([city for city in g_path]) + '\n'

    result_file = open('test.out', 'w+')
    result_file.write(cities_in_shortest_way)
    result_file.write(str(minutes))
    result_file.close()


