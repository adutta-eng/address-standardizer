import standardizer
import comparator
from amgScore import fidComparator
from itertools import combinations, product
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.cluster import AffinityPropagation


#TODO: figure out what the id/index for an address normally looks like & where it is
def loadTestData(inPath = 'H:/conda/address-standardizer-master/dictionaries/testData.txt' ):
    testDataPath = inPath
    with open(testDataPath, 'r') as temp:
        testData = [x[:-1] for x in temp.readlines()]

    # with ... csv dictreader


    # assume there's some kind of index/id - csv, or otherwise somehow parsable. let's just
    # self-generate it for now though
    # e.g. csv: indices = [x.split(",")[0] for x in testData]?
    indices = range(len(testData))
    # data = {zip}
    data = {index: address for index, address in zip(indices, testData)}
    return data

matchStrings = loadTestData()

#mocking up a fake demo rows hecre...
testStrings = """
101 north vinebridge street, anytown md 99999
101 north vineridge street, anytown md 99999
101 vinebridge street, anytown md 99999
101 north vine bridge street, anytown md 99999
101 north vine Rridge street, anytown md 99999
101 north pine bridge street, anytown md 99999
101 north pinebridge street, anytown md 99999
101 pinebridge street, anytown md 99999
101 pinebridge street south, anytown md 99999
101 pinebridge street north, anytown md 99999
""".strip().split('\n')

testStrings = {index: address for index, address in enumerate(testStrings)}

def report_format_errors(formatted_dict):
    formatErrors = formatted_dict['errors'] 
    if len(formatErrors)>0:
        print('the following test records failed and require code fixes:')
    for id, errorLine in formatErrors.items():
        print(id + ": " + errorLine)
        errorStan = standardizer.standardize(errorLine)
        for item in errorStan:
            print('\t',item[1],item[0])
        print('\n')

def format_strings(address_strings):
    format_dict = {}
    fidRows = {}
    formatErrors = {}
    for id, string in address_strings.items():
        try:
            standard_dict = standardizer.standardize(string)
            formatted_entry = comparator.fid_prepare(standard_dict)
            fidRows[id] = formatted_entry
        except:
            formatErrors[id] = string
    format_dict['matchable'] = fidRows
    format_dict['errors'] = formatErrors
    report_format_errors(format_dict)
    return format_dict

def pairwise_match(cleaned_data):
    scores = []
    counter = 0
    for fidA, fidB in combinations(cleaned_data.keys(), 2):
        fid_list = comparator.fid_pair(cleaned_data[fidA], cleaned_data[fidB])
        fid_score = -1
        counter += 1
        if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):
            fid_score = fidComparator(*fid_list)
    #     print(fidA, fidB, fid_score)
    # print(counter)
    scores.append(fid_score)

def find_matches(setA, setB):
    matchResults = []
    matchTestCounter = 0
    print('looping through match tests')
    
    for entryA, entryB in product(setA.keys(), setB.keys()):
        matchTestCounter += 1
        if matchTestCounter % 40 == 0:
            print('\tProgress: {}'.format(str(matchTestCounter)))

        fid_list = comparator.fid_pair(setA[entryA], setB[entryB])
        fid_score = -1
        if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):
            fid_score = fidComparator(*fid_list)
        matchResults.append(fid_score)

    return matchResults

def find_matches_in_df(setA, setB):
    df = pd.DataFrame(columns = ['Address 1', 'Address 2', 'FidScore'])
    matchTestCounter = 0
    for entryA, entryB in product(setA.keys(), setB.keys()):
        fid_list = comparator.fid_pair(setA[entryA], setB[entryB])
        fid_score = -1
        if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):
            fid_score = fidComparator(*fid_list)
        df.loc[matchTestCounter] = [entryA, entryB, fid_score]
        matchTestCounter += 1
    pd.set_option("display.max_rows", None, "display.max_columns", None)
#     print(df)
    return df       


## returns results as a dataframe, where value at row, index = score
## when deduplicating, this is basically an adjacency matrix
# def find_matches_in_df(setA, setB):
#     df = pd.DataFrame(0, columns = setA.keys(), index = setB.keys())
#     # df = pd.DatFrame(columns = ['Address 1', 'Address 2', 'FidScore'])
#     matchTestCounter = 0
#     for entryA, entryB in product(setA.keys(), setB.keys()):
#         fid_list = comparator.fid_pair(setA[entryA], setB[entryB])
#         fid_score = -1
#         if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):
#             fid_score = fidComparator(*fid_list)
#         df.at[entryB, entryA] = fid_score
#         matchTestCounter += 1
#     pd.set_option("display.max_rows", None, "display.max_columns", None)
#     print(df)
#     return df

def match_network(matching_results):
    G = nx.Graph()
    # df
    if isinstance(matching_results, pd.DataFrame):
        for index, row in matching_results.iterrows():
            if row['FidScore'] > 800:
                G.add_edge(row['Address 1'], row['Address 2'], weight = row['FidScore'])
    # list of tuples?
    else:
        for (a, b, score) in matching_results:
            if score > 800:
                G.add_edge(a, b, weight = score)
    return G

## if networkx.to_pandas_adjacency was *working* this wouldn't be necessary
# important thing here is that ORDER IS PRESERVED - can index back into nodes
def make_adjacency_matrix(network):
    adj_matrix = pd.DataFrame(0, columns = network.nodes(), index = network.nodes())
    for (a, b) in network.edges():
        weight = network[a][b]['weight']
        adj_matrix.at[a, b] = weight
        adj_matrix.at[b, a] = weight
    return adj_matrix

def disentangle(network):
    adj_matrix = make_adjacency_matrix(network)
    model = AffinityPropagation(affinity='precomputed').fit(adj_matrix)

    ids = network.nodes()
    
    # the database ids of the deduplicated records; the "centers" of the clusters
    centers = [ids[index] for index in model.cluster_centers_indices_]
    # the mapping of each record id to its centralized record's id
    mapping = {ids[index]: centers[cluster] for index, cluster in enumerate(model.labels_)}

    return (centers, mapping)



standardized_testing = format_strings(testStrings)
standardized_match = format_strings(matchStrings)

pairwise_match(standardized_match['matchable'])
pairwise_match(standardized_testing['matchable'])

results = find_matches(standardized_match['matchable'], standardized_testing['matchable'])
find_matches_in_df(standardized_match['matchable'], standardized_testing['matchable'])
anyMatch = [x for x in results if x > 0]
numMatches = len(anyMatch)

dedup = find_matches_in_df(standardized_testing['matchable'], standardized_testing['matchable'])
graph = match_network(dedup)
centers, label_map = disentangle(graph)
print(graph.nodes())
print(graph.edges())
print(centers)
print(label_map)

print('number of matches between "testStrings" and "matchStrings" (may include duplicates...)',str(numMatches))    
print("Done!")
