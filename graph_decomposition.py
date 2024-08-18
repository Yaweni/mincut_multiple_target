import copy
import random
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, groupby
import pandas as pd
from tqdm import tqdm


def contract_edges(G, nodes, new_node, ):

    G2 = nx.MultiGraph()
    G2.add_nodes_from(G.nodes(data=True))
    G2.add_edges_from(G.edges(data=True))
    # Add the node with its attributes
    G2.add_node(new_node)
    # Create the set of the edges that are to be contracted
    cntr_edge_set = G.edges(nodes, data=True)
    edge_set = copy.deepcopy(cntr_edge_set)
    for edge in edge_set:
        if not isinstance(G,nx.MultiGraph):
            source_attr = G.edges[(edge[0], edge[1])]
            if edge[0] in nodes and edge[1] not in nodes:
                key=G2.number_of_edges(new_node,edge[1])
                G2.add_edge(new_node, edge[1],key)
                nx.set_edge_attributes(G2, {(new_node, edge[1],key): source_attr})
            elif edge[1] in nodes and edge[0] not in nodes:
                key=G2.number_of_edges(edge[0],new_node)
                G2.add_edge(edge[0], new_node,key)
                nx.set_edge_attributes(G2, {(edge[0], new_node,key): source_attr})

        else:
            for id in range(G2.number_of_edges(edge[0],edge[1])):
                source_attr = G.edges[(edge[0], edge[1],id)]
                if edge[0] in nodes and edge[1] not in nodes:
                    G2.add_edge(new_node, edge[1],id)
                    nx.set_edge_attributes(G2, {(new_node, edge[1],id): source_attr})
                elif edge[1] in nodes and edge[0] not in nodes:
                    G2.add_edge(edge[0], new_node,id)
                    nx.set_edge_attributes(G2, {(edge[0], new_node,id): source_attr})
    G2.remove_nodes_from(nodes)
    return G2.copy()


def gnp_random_connected_graph(n, p):
    """
    Generates a random undirected graph, similarly to an Erdős-Rényi
    graph, but enforcing that the resulting graph is conneted
    """

    z = 0
    edges = combinations(range(n), 2)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    if p <= 0:
        return G
    if p >= 1:
        return nx.complete_graph(n, create_using=G)
    for _, node_edges in groupby(edges, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        weight = random.randint(1, 10)
        G.add_edge(*random_edge, weight=weight, edge_id=z)
        z += 1
        for e in node_edges:
            if random.random() < p:
                weight = random.randint(1, 10)
                G.add_edge(*e, weight=weight, edge_id=z)
                z += 1
    #G = nx.barabasi_albert_graph(n,int(p*10))
    #for u,v,data in G.edges(data=True):
     #   G[u][v]['weight']= random.randint(1, 10)
      #  G[u][v]['edge_id']= z
       # z+=1

    return G


def generate_random_graph(num_nodes, num_entry_nodes, num_target_nodes, connection_probability):
    G = gnp_random_connected_graph(num_nodes, connection_probability)
    entry_nodes = random.sample(range(num_nodes), num_entry_nodes)
    target_nodes = random.sample(list(set(range(num_nodes)) - set(entry_nodes)), num_target_nodes)

    for i in range(num_nodes):
        if i in target_nodes:
            G.nodes[i]['value'] = random.randint(1, 10)
            G.nodes[i]['color'] = "blue"
            G.nodes[i]['id'] = i
        elif i in entry_nodes:
            G.nodes[i]['color'] = "red"
            G.nodes[i]['id'] = i
        else:
            G.nodes[i]['color'] = "gray"
            G.nodes[i]['id'] = i

    return G, entry_nodes, target_nodes


def calculate_component_values(G, entry_nodes, target_nodes):
    max_spanning_tree = nx.minimum_spanning_tree(G)
    max_spanning_tree.remove_nodes_from(entry_nodes)
    components = list(nx.connected_components(max_spanning_tree))

    component_values = []
    for component in components:
        component_value = sum(G.nodes[node]['value'] for node in component if node in target_nodes)
        component_values.append(component_value)

    return component_values, components


def calculate_minimum_edge_cut_sets(G, components, target_nodes, component_values, draw):
    min_cut_sets = []
    data = copy.deepcopy(G.edges(data=True))

    for i, component in enumerate(components, start=0):
        if component_values[i] > 0:

            nodes = list(set(target_nodes) & set(component))
            if len(nodes):
                # for node in nodes[1:]:
                #    G1 = nx.contracted_nodes(G, nodes[0], node, self_loops=False)
                #    G1.remove_nodes_from(nodes[1:])
                G1 = G.copy()
                G1 = contract_edges(G1, nodes, 'super_target')
                G1.nodes['super_target']['color'] = 'orange'
            if draw:
                pos = nx.spring_layout(G1)

                nx.draw(G1, pos, node_color=[G1.nodes[n]['color'] for n in G1.nodes()], node_size=500, )
                # Draw the graph
                node_labels = nx.get_node_attributes(G1, 'id')
                nx.draw_networkx_labels(G1, pos, labels=node_labels, )
                # edge_labels = nx.get_edge_attributes(G1,'weight')
                # nx.draw_networkx_edge_labels(G1, pos, edge_labels = edge_labels)

                # Display the graph
                plt.show()
            externs = [node for node in G.nodes if node in entry_nodes]
            # for node in externs[1:]:

            G2 = contract_edges(G1.copy(), externs, 'super_entry')
            G2.nodes['super_entry']['color'] = 'purple'

            # G2=nx.contracted_nodes(G1, externs[0], node,self_loops=False)
            # G2.remove_nodes_from(externs[1:])
            if draw:
                pos = nx.spring_layout(G2)

                nx.draw(G2, pos, node_color=[G2.nodes[n]['color'] for n in G2.nodes()], node_size=500, )
                # Draw the graph
                node_labels = nx.get_node_attributes(G2, 'id')
                nx.draw_networkx_labels(G2, pos, labels=node_labels, )
                # edge_labels = nx.get_edge_attributes(G2,'weight')
                # nx.draw_networkx_edge_labels(G2, pos, edge_labels = edge_labels)

                # Display the graph
                plt.show()

            cut_set = nx.minimum_edge_cut(G2, t='super_target', s='super_entry')
            final_set = []
            for edge in cut_set:
                a = list(edge)
                for j in range(G2.number_of_edges(a[0], a[1])):
                    # print('In graph',G2.edges[a[0],a[1],i])
                    edge_to_find_id = G2.edges[a[0], a[1], j]['edge_id']
                    edge_to_find = [edge for edge in data if edge[2]['edge_id'] == edge_to_find_id]

                    # edge_to_find=[edge for edge in G.edges(data=True) if edge[2]['edge_id']==G2[a[0]][a[1]]['edge_id']][0]
                    final_set.append((edge_to_find[0][0], edge_to_find[0][1]))

            min_cut_sets.append((final_set, f"Component {i + 1}", f"{len(final_set)} Edges", component_values[i]))

    return min_cut_sets


for a in [70]:
    values = [['Total Nodes', 'Entry Nodes', 'Target Nodes','Prob'
               'Global Cut', 'Span Cut', 'Edge Value Global', ' Max Edge Value Comp', 'Fraction']]
    for b in range(3, 8):
        for c in range(3, 9):
            for prob in tqdm([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]):
                for num in range(40):

                    num_nodes = a
                    num_entry_nodes = b
                    num_target_nodes = c
                    link_probability = prob
                    G, entry_nodes, target_nodes = generate_random_graph(num_nodes,
                                                                         num_entry_nodes,
                                                                         num_target_nodes,
                                                                         link_probability)
                    Ginit = G.copy()
                    # print("Random Graph:")
                    # print("Nodes:", G.nodes)
                    # print("Edges:", G.edges)
                    # print("Targets:",target_nodes)
                    # print("Entry:",entry_nodes)
                    component_values, components = calculate_component_values(G, entry_nodes, target_nodes)
                    # print("\nComponent Values:", component_values)
                    # print("Components:", components)
                    draw = False
                    G3 = Ginit.copy()
                    min_cut_sets_tot = calculate_minimum_edge_cut_sets(G3, list(nx.connected_components(G3)),
                                                                       target_nodes, [sum(component_values)], draw)
                    # print("\nMinimum Edge Cut Sets No Split:")
                    max_val_glob = 0
                    total_edges_glob = 0
                    total_val_glob = 0
                    for i, cut_set in enumerate(min_cut_sets_tot):
                        # print("Component", i+1, ":", cut_set)
                        total_edges_glob += len(cut_set[0])
                        if cut_set[3] / len(cut_set[0]) > max_val_glob:
                            max_val_glob = cut_set[3] / len(cut_set[0])
                            total_val_glob = cut_set[3]

                    min_cut_sets = calculate_minimum_edge_cut_sets(G, components, target_nodes, component_values, draw)
                    # print("\nMinimum Edge Cut Sets:")
                    max_val_comp = 0
                    total_edges_comp = 0
                    total_distinct = set()
                    percentage_sup = 0
                    for i, cut_set in enumerate(min_cut_sets):
                        # print("Component", i+1, ":", cut_set)
                        total_edges_comp += len(cut_set[0])
                        total_distinct = set.union(total_distinct, cut_set[0])
                        if cut_set[3] / len(cut_set[0]) > max_val_comp:
                            max_val_comp = cut_set[3] / len(cut_set[0])
                        if cut_set[3] / len(cut_set[0]) > max_val_glob:
                            percentage_sup += cut_set[3] / total_val_glob
                    # print("__________________________________________________________")
                    # print("|Max Value Honeypot Components| Max Value Honeypot Global|")
                    # print(f"|          {max_val_comp}                 |        {max_val_glob}                  |")
                    # print("__________________________________________________________")
                    # print("__________________________________________________________")
                    #  print("|Total Edges Components| Total Edges Global|")
                    #   print(f"|          {total_edges_comp}         |        {total_edges_glob}           |")
                    #    print("____________________________________________")
                    #     print("____________________________________________")
                    #      print("|Total Distinct Edges Components|")
                    #       print(f"|          {len(total_distinct)}                  |")
                    #        print("______________________________")
                    #         print("______________________________")
                    #          print("|% Over Average allocation|")
                    #           print(f"|          {percentage_sup}   |")
                    #            print("______________________________")

                    if draw:
                        pos = nx.spring_layout(Ginit)

                        nx.draw(Ginit, pos, node_color=[Ginit.nodes[n]['color'] for n in Ginit.nodes()],
                                node_size=500, )
                        # Draw the graph
                        node_labels = nx.get_node_attributes(Ginit, 'id')
                        nx.draw_networkx_labels(Ginit, pos, labels=node_labels, )
                        edge_labels = nx.get_edge_attributes(Ginit, 'weight')
                        nx.draw_networkx_edge_labels(Ginit, pos, edge_labels=edge_labels)

                        # Display the graph
                        plt.show()
                    holder = [num_nodes, num_entry_nodes, num_target_nodes,prob,
                              total_edges_glob, len(total_distinct),
                              max_val_glob, max_val_comp, percentage_sup]
                    # print(holder)
                    values.append(holder)

    df = pd.DataFrame(values[1:], columns=values[0])
    name = f"Component Gain Erdos.csv+{a}"
    df.to_csv(name)
