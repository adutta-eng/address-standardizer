import standardizer
# from standardizer import standardize
import comparator
from amgScore import fidComparator
import pandas as pd
import csv
import networkx as nx
from sklearn.cluster import AffinityPropagation

"""
read a .txt file and turn it into a dataframe
"""
def convertInputFileToFrame(file_path):
    input_file = open(file_path, 'r')
    lines = input_file.readlines()
    id = 0
    df = pd.DataFrame(columns = ['ID', 'Address'])
    for line in lines:
        line = line.rstrip('\n')
        df.loc[id] = [id, line]
        id += 1
    return df

"""
!!assumes there are csv headings!!
turns a csv into a dataframe, standardizing columns
    file_path: the filepath to the csv
    id_col: the column name of the id/index values
    address_col: the column name of the raw address data
    delimiter: the delimiter for the csv
    nrows: the number of rows to take
"""
def csv_to_frame(file_path, id_col, address_col, delimiter = ',', nrows = None):
    result = pd.read_csv(file_path, usecols = [id_col, address_col], sep = delimiter, nrows = nrows)
    result = result.rename(columns = {id_col : 'ID', address_col : 'Address'})
    result = result.set_index('ID')
    return result

#TODO: find a better way of error-catching
"""
at least one of labels or fidlist must be True
labels, fidlist, and original are boolean flags
-- labels gives every parsed label category that has at least one value
-- fidlist gives the needed values for fidCompare in a list
-- original maintains the original address

if you want to block on a parsed label, labels should be True!
    input_df: a dataframe with an 'Address' column and indexed by unique ids
    labels: flag to put all outputs from standardize() into the frame
    fidlist: flag to put the condensed values from fid_prepare in its own column
    original: flag to retain the original address as a column
"""     
def standardize_df(input_df, labels = True, fidlist = True, original = True):

    # nested function that handles individual addresses
    def clean(addr, labels, fidlist):
        try:        
            stan = standardizer.standardize(addr)
            if fidlist:
                flist = {"FidList" : comparator.fid_prepare(stan)}
                if labels:
                    stan.update(flist)
                    return stan
                else:
                    return flist
            else:
                return stan
        except:
            # maybe add an ERROR column? with specific error codes?
            return {'ERROR' : addr}
    
    result_df = pd.DataFrame(list(input_df['Address'].apply( \
        clean, labels = labels, fidlist = fidlist)), index = input_df.index)
    if original:
        result_df['Address'] = input_df['Address']
    
    return result_df

# TODO: do some real error handling, ya loser
"""
a helper function for df.apply() in deduplicate() and match()
    col_address, constant: two address records stripped by fid_prepare
    -- list of six values each
returns fidCompare's score, or fails with -1
"""
def column_matches(col_address, constant):
    try:
        fid_list = comparator.fid_pair(col_address, constant)
        return fidComparator(*fid_list)
    except:
        return -1

"""
matches a dataframe of records with itself and generates a frame of match scores
    data: the input dataframe
    score_threshold: two records match if their score >= the threshold
    block: a single label (i.e. ZIP) to block on
"""
def deduplicate(data, score_threshold = 800, block = None):

    result = pd.DataFrame(columns = ['Address1', 'Address2', 'FidList'])
    # breaks down df into blocked df slices
    if block:
        blocked = data.groupby(block)
        blocked_chunks = [blocked.get_group(blk)['FidList'] for blk in blocked.groups.keys()]
    else:
        blocked_chunks = [data['FidList']]

    # iterate through blocks
    for b in blocked_chunks:    
        for idx, x in zip(b.index, b):
            matches = b.apply(column_matches, constant = x)
            matches = pd.DataFrame(matches)
            matches['Address1'] = matches.index
            matches['Address2'] = idx
            cleaned = matches.loc[matches['FidList'] >= score_threshold]
            result = result.append(cleaned, ignore_index = True)
            b = b.drop(idx)

    # apply this here or in each iteration? memory vs. speed
    # better to clean in iterations if lots of matches

    return result

"""
compares two dataframes of records and generates a frame of match scores
    dataA, dataB: two input dataframes
    score_threshold: two records match if their score >= the threshold
    block: a single label (i.e. ZIP) to block on
"""
def match(dataA, dataB, score_threshold = 800, block = None):

    result = pd.DataFrame(columns = ['Address1', 'Address2', 'FidList'])
    # make blocked pairs of grouped df slices
    if block:
        blockedA = dataA.groupby(block)
        blockedB = dataB.groupby(block)
        blocked_pairs = [(blockedA.get_group(blk)['FidList'], \
            blockedB.get_group(blk)['FidList']) for blk in \
                blockedA.groups.keys() if blk in blockedB.groups.keys()]
    else:
        blocked_pairs = [(dataA['FidList'], dataB['FidList'])]

    # iterate through paired blocks
    for a, b in blocked_pairs:    
        for idx, x in zip(a.index, a):
            matches = b.apply(column_matches, constant = x)
            matches = pd.DataFrame(matches)
            matches['Address1'] = matches.index
            matches['Address2'] = idx
            cleaned = matches.loc[matches['FidList'] >= score_threshold]            
            result = result.append(cleaned, ignore_index = True)

    # apply this here or in each iteration? memory vs. speed
    # better to clean in iterations if lots of matches

    return result

"""
transforms a dataframe of matches into a graph, with match scores as weights
df_matches: dataframe of matches [address1, address2, score] 
"""
def match_network(df_matches):
    G = nx.Graph()
    G.add_weighted_edges_from(cleaned.values.tolist())
    # if input isn't df, but something like a list of lists, the code is 
    # basically the same
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
returns: a mapping from each node to its cluster center/exemplar
"""
def disentangle(network, subgraphs = True):
    if subgraphs:
        graphs = [network.subgraph(c).copy() for c in \
            nx.connected_components(network) if len(c) > 1]
    else:
        graphs = [network] if len(network.nodes()) > 1 else []
    final_map = {}
    for g in graphs:
        adj_matrix = make_adjacency_matrix(g)
        # will break if there is only one node passed in
        model = AffinityPropagation(affinity='precomputed').fit(adj_matrix)

        ids = g.nodes()
        # the database ids of the deduplicated records; the "centers" of the clusters
        centers = [ids[index] for index in model.cluster_centers_indices_]
        # the mapping of each record id to its centralized record's id
        mapping = {ids[index]: centers[cluster] for index, cluster in enumerate(model.labels_)}
        final_map.update(mapping)
    # centers is just final_map.values()
    return final_map

