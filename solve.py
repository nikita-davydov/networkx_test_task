import sys
import itertools
from typing import List, Tuple
import math
from pydantic import BaseModel


class Edge(BaseModel):
    node_from: str
    node_to: str
    distance_in_minutes: int


class Graph:
    edges: List[Edge] = []

    @property
    def nodes(self):
        return set(
            itertools.chain.from_iterable([[edge.node_from, edge.node_to] for edge in self.edges])
        )

    @property
    def neighbours_by_node(self):
        neighbours = {node: set() for node in self.nodes}
        for edge in self.edges:
            neighbours[edge.node_from].add((edge.node_to, edge.distance_in_minutes))

        return neighbours

    def add_edge(self, node_from, node_to, distance_in_minutes):
        self.edges.append(Edge(node_from=node_from, node_to=node_to, distance_in_minutes=distance_in_minutes))
        self.edges.append(Edge(node_from=node_to, node_to=node_from, distance_in_minutes=distance_in_minutes))

    def dijkstra(self, point_a: str, point_b: str) -> Tuple[List[str], int]:
        distances = {node: math.inf if node != point_a else 0 for node in self.nodes}
        visited_nodes = {node: None for node in self.nodes}
        nodes = self.nodes.copy()

        while nodes:
            current_node = min(nodes, key=lambda node: distances[node])

            if distances[current_node] == math.inf:
                break

            for node_to, distance_in_minutes in self.neighbours_by_node[current_node]:
                counted_distance = distances[current_node] + distance_in_minutes
                if counted_distance < distances[node_to]:
                    distances[node_to] = counted_distance
                    visited_nodes[node_to] = current_node

            nodes.remove(current_node)

        path, current_node = list(), point_b
        while visited_nodes[current_node] is not None:
            path.insert(0, current_node)
            current_node = visited_nodes[current_node]

        if path:
            path.insert(0, current_node)
        return path, distances[point_b]


def create_graph(data: list) -> Graph:
    g = Graph()

    for row in data:
        city1, city2, distance_in_minutes = row.split(',')
        g.add_edge(
            city1, city2, int(distance_in_minutes)
        )
    return g


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('You have to specify input file name')

    file_name = sys.argv[1]
    file = open(file_name, 'r')
    lines = [line.replace('\n', '') for line in file.readlines()]
    file.close()

    a, b = lines.pop(0).split(',')
    graph = create_graph(lines)

    g_path, minutes = graph.dijkstra(a, b)
    cities_in_shortest_way = ','.join([city for city in g_path]) + '\n'

    result_file = open('test.out', 'w+')
    result_file.write(cities_in_shortest_way)
    result_file.write(str(minutes))
    result_file.close()


