import networkx as nx
from collections import deque
import matplotlib.pyplot as plt


def transform_to_directed(graph, source, destination):
    directed_graph = nx.DiGraph()
    directed_graph.add_nodes_from(graph.nodes())

    queue = deque([(destination, None)])
    visited = set()

    while queue:
        current, parent = queue.popleft()
        visited.add(current)

        if current == source:
            neighbors = graph.neighbors(current)
            for neighbor in neighbors:
                directed_graph.add_edge(current, neighbor)

        else:
            neighbors = graph.neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    directed_graph.add_edge(neighbor, current)
                    queue.append((neighbor, None))

    return directed_graph


graph = nx.barabasi_albert_graph(10, 3)
pos = nx.spring_layout(graph)

nx.draw(graph, pos, node_size=500)
nx.draw_networkx_labels(graph, pos)
print(nx.find_cycle(graph))
plt.show()
source_node = 0
destination_node = 4

directed_graph = transform_to_directed(graph, source_node, destination_node)
graph = directed_graph
pos = nx.spring_layout(graph)

nx.draw(graph, pos, node_size=500)
nx.draw_networkx_labels(graph, pos)
plt.show()
