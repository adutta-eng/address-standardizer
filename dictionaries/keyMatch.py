import standardizer
import comparator
from amgScore import fidComparator
from itertools import combinations, product
import pandas as pd
import csv


#TODO: get rid of all of this terrible garbage
#TODO: figure out what the id/index for an address normally looks like & where it is
def loadTestData(inPath = r'testData.txt', ):
    testDataPath = inPath
    with open(testDataPath, 'r') as temp:
        testData = [x[:-1] for x in temp.readlines()]

    csv = False
    if csv: 
        ## column names if csv or something similar
        id_name = None
        address_name = None

        # with ... csv dictreader
        with open(inpath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = {row['id_name']: row['address_name'] for row in reader}

    # assume there's some kind of index/id - csv, or otherwise somehow parsable. let's just
    # self-generate it for now though
    # e.g. csv: indices = [x.split(",")[0] for x in testData]?
    indices = range(len(testData))
    # data = {zip}
    data = {index: address for index, address in zip(indices, testData)}
    return data

def load_csv(inPath = r'testData.txt', id_name = None, address_name = None, delimiter = ','):
    if id_name and address_name:
        with open(inPath, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter = delimiter)
            data = {row[id_name]: row[address_name] for row in reader}
    else:
        with open(inPath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = delimiter)
            data = {row[0]: row[1] for row in reader}
    return data

matchStrings = loadTestData('H:/conda/address-standardizer-master/dictionaries/testData.txt')

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
        try:
            errorStan = standardizer.standardize(errorLine)
            for item in errorStan:
                print('\t',item[1],item[0])
        except:
            print("standardizing failed")
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

## add verbose flag
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


# idea: modes of output - dataframe/list of matches, matrix of scores, directly as a network, etc.
def find_matches(setA, setB, score_threshold = 800, block = None, output = 'list'):
    # matchTestCounter = 0
    # print('looping through match tests')

    if output = 'matrix':
        matchResults = pd.DataFrame(-1, columns = setA.index, index = setB.index)
    elif output = 'network':
        matchResults = nx.Graph()
    elif output = 'list':
        matchResults = []

    for entryA, entryB in blocking(setA, setB, block):    #  product(setA.keys(), setB.keys()):
        # matchTestCounter += 1
        # if matchTestCounter % 40 == 0:
        #     print('\tProgress: {}'.format(str(matchTestCounter)))

        ## update
        fid_list = comparator.fid_pair(fid_prepare(setA.loc[entryA]), fid_prepare(setB.loc[entryB]))
        # fid_score = -1
        # find a better way to error-handle/check here
            
        # the type error should no longer be a problem; try/catch is probably better?
        # if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):

        # use a try/catch instead? or not at all?
        # try:
        fid_score = fidComparator(*fid_list)

        # we can decide where to put this - could also be put somewhere else
        if fid_score >= score_threshold:

            if output = 'matrix':
                matchResults.at[entryB, entryA] = fid_score
            elif ouput = 'network':
                matchResults.add_edge(entryB, entryA, weight = fid_score)
            elif output = 'list':
                matchResults.append((entryA, entryB, fid_score))

    return matchResults

def find_matches_in_df(setA, setB):
    df = pd.DataFrame(columns = ['Address 1', 'Address 2', 'FidScore'])
    # matchTestCounter = 0
    for entryA, entryB in product(setA.keys(), setB.keys()):
        ## update
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
label_map = disentangle(graph)
print(graph.nodes())
print(graph.edges(data = True))
print(set(label_map.values()))
print(label_map)

print('number of matches between "testStrings" and "matchStrings" (may include duplicates...)',str(numMatches))    
print("Done!")

# assume standardized rows?
def deduplicate(cleaned_data, block = None, output):

    if output = 'matrix':
        matchResults = pd.DataFrame(-1, columns = cleaned_data.index, index = cleaned_data.index)
    elif output = 'network':
        matchResults = nx.Graph()
    elif output = 'list':
        matchResults = []


    # df = pd.DatFrame(columns = ['Address 1', 'Address 2', 'FidScore'])
    # matchTestCounter = 0
    # if unstandardized, it would look like this
    # addresses = cleaned_data[address_col]
    # else, call fid_prepare on cleaned_data.loc[fidA]
    for entryA, entryB in blocking(cleaned_data, block = block):

        fid_list = comparator.fid_pair(fid_prepare(setA.loc[entryA]), fid_prepare(setB.loc[entryB]))
        # fid_score = -1
        # find a better way to error-handle/check here
            
        # the type error should no longer be a problem; try/catch is probably better?
        # if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):

        # use a try/catch instead? or not at all?
        # try:
        fid_score = fidComparator(*fid_list)

        # we can decide where to put this - could also be put somewhere else
        if fid_score >= score_threshold:

            if output = 'matrix':
# very technically this is redundant when you go down the diagonal... but do we care?
                matchResults.at[entryA, entryB] = fid_score
                matchResults.at[entryB, entryA] = fid_score
            elif ouput = 'network':
                matchResults.add_edge(entryB, entryA, weight = fid_score)
            elif output = 'list':
                matchResults.append((entryA, entryB, fid_score))


        # standardize now, or standardize before?
        # standardize now requres ~n^2 standardizations... as opposed to n
    for entry in cleaned_data.index:
        fid_list = comparator.fid_pair(fid_prepare(setA.loc[entryA]), fid_prepare(setB.loc[entryB]))
        # fid_score = -1
        # find a better way to error-handle/check here
            
        # the type error should no longer be a problem; try/catch is probably better?
        # if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):

        # use a try/catch instead? or not at all?
        # try:
        fid_score = fidComparator(*fid_list)

        if fid_score >= score_threshold:

            if output = 'matrix':
                matchResults.at[entry] = fid_score
            elif ouput = 'network':
                matchResults.add_edge(entry, entry, weight = fid_score)
            elif output = 'list':
                matchResults.append((entry, entry, fid_score))


    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    # print(df)
    return df


## figure out how to make this work for both deduplication & two pairs

"""
generates all the tuple pairs of record indices to be matched
-- implements one column for blocking 

"""

def blocking(dataA, dataB = None, block = None):
    if block != None:
        blockedA = dataA.groupby(block)
        pairs = []
        # combinations = [combinations(blocked.get_group(block), 2) for block in blocked.groups.keys()]
        if dataB:
            blockedB = dataB.groupby(block)
            groupsB = blockedB.group.keys()
            for blk in blockedA.groups.keys():
                if blk in groupB:
                    groupA = blockedA.get_group(block)
                    groupB = blockedB.get_group(block)
                    pairs.extend(product(blockedA.index, blockedB.index))
        else:
            for blk in blockedA.groups.keys():
                groupA = blockedA.get_group(blk)
                pairs.extend(combinations(groupA.index, 2))
    else:
        if dataB:
            pairs = product(dataA.index, dataB.index)             
        else:
            pairs = combinations(dataA.index, 2)
            # should we do this here or in the deduplication function?
            pairs.extend([(x, x) for x in dataA.index])
    return pairs



