import numpy as np
import networkx as nx
from sklearn.cluster import AffinityPropagation



"""
transforms a list of matches into a graph
matching results: dataframe or list of matches as tuples (address1, address2, score) 
threshold: the minimum score value that counts as a match 
"""
def match_network(matching_results, threshold = 800):
    G = nx.Graph()
    # df
    if isinstance(matching_results, pd.DataFrame):
        for index, row in matching_results.iterrows():
            if row['FidScore'] >= threshold:
                G.add_edge(row['Address 1'], row['Address 2'], weight = row['FidScore'])
    # list of tuples?
    else:
        for (a, b, score) in matching_results:
            if score >= threshold:
                G.add_edge(a, b, weight = score)
    return G

## if networkx.to_pandas_adjacency was *working* this wouldn't be necessary
# important thing here is that ORDER IS PRESERVED - can index back into nodes
"""
makes a pandas dataframe that represents the adjacency matrix of an input graph
-- columns & indices are nodes, order is preserved after AffinityPropagation
"""
def make_adjacency_matrix(network):
    adj_matrix = pd.DataFrame(0, columns = network.nodes(), index = network.nodes())
    for (a, b) in network.edges():
        weight = network[a][b]['weight']
        adj_matrix.at[a, b] = weight
        adj_matrix.at[b, a] = weight
    return adj_matrix

"""
uses sklearn's AffinityPropagation implementation to find exemplars in a network
of addresses where edges are matches (can be weighted)
network: the overall network
subgraphs: if True, will run AffinityPropagation on each unique subgraph separately
           -- False will generally lead to a single address per cluster
output: a mapping from each node to its cluster center/exemplar
"""
def disentangle(network, subgraphs = True):
    if subgraphs:
        graphs = [network.subgraph(c).copy() for c in nx.connected_components(network)]
    else:
        graphs = [network]
    final_map = {}
    for g in graphs:
        if len(g.nodes()) < 2:
            continue
        adj_matrix = make_adjacency_matrix(g)
        model = AffinityPropagation(affinity='precomputed').fit(adj_matrix)

        ids = g.nodes()
        # the database ids of the deduplicated records; the "centers" of the clusters
        centers = [ids[index] for index in model.cluster_centers_indices_]
        # the mapping of each record id to its centralized record's id
        mapping = {ids[index]: centers[cluster] for index, cluster in enumerate(model.labels_)}
        final_map.update(mapping)
    # centers is just final_map.values()
    return final_map