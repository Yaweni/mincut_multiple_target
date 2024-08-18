import random
import networkx as nx

def generate_random_graph(num_nodes, num_entry_nodes, num_target_nodes):
    G = nx.Graph()
    entry_nodes = random.sample(range(num_nodes), num_entry_nodes)
    target_nodes = random.sample(set(range(num_nodes)) - set(entry_nodes), num_target_nodes)

    for i in range(num_nodes):
        G.add_node(i)
        if i in target_nodes:
            G.nodes[i]['value'] = random.randint(1, 10)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if i != j:
                weight = random.randint(1, 10)
                G.add_edge(i, j, weight=weight)

    return G, entry_nodes, target_nodes

def calculate_component_values(G, entry_nodes, target_nodes):
    max_spanning_tree = nx.maximum_spanning_tree(G)
    max_spanning_tree.remove_nodes_from(entry_nodes)
    components = list(nx.connected_components(max_spanning_tree))

    component_values = []
    for component in components:
        component_value = sum(G.nodes[node]['value'] for node in component if node in target_nodes)
        component_values.append(component_value)

    return component_values, components

def calculate_minimum_edge_cut_sets(G, components, target_nodes):
    min_cut_sets = []
    for component in components:
        cut_set = nx.minimum_edge_cut(G, component, target_nodes)
        min_cut_sets.append(cut_set)

    return min_cut_sets

# Example usage
num_nodes = 10
num_entry_nodes = 3
num_target_nodes = 3

G, entry_nodes, target_nodes = generate_random_graph(num_nodes, num_entry_nodes, num_target_nodes)
print("Random Graph:")
print("Nodes:", G.nodes)
print("Edges:", G.edges)

component_values, components = calculate_component_values(G, entry_nodes, target_nodes)
print("\nComponent Values:", component_values)
print("Components:", components)

min_cut_sets = calculate_minimum_edge_cut_sets(G, components, target_nodes)
print("\nMinimum Edge Cut Sets:")
for i, cut_set in enumerate(min_cut_sets):
    print("Component", i+1, ":", cut_set)
