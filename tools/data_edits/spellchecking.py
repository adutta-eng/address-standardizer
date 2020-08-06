"""
REASONING FOR DESIGN DECISIONS:
Scoring is based off of raw word count, not anything like tf-idf
-- because everything is already being parsed into categories, there are rarely
   more than a few words in a given document, they almost never repeat, and
   repetition (or inverse frequency, for that matter) does not predict as much
   importance, as words in addresses rarely have weighted meanings 
   (within a category, that is; "Red Street" and "Red Red Street" very well may
   be different street names)
-- 


FLOW OF DATA:
raw file (e.g. csv) -> pandas dataframe -> standardized/parsed dataframe ->
blocked series of dataframes/single dataframe -> dictionary of dictionaries;
first keys being block values (_____ if unblocked), second keys being parsed
address components
"""

import numpy as np
import pandas as pd
from jellyfish import damerau_levenshtein_distance
from math import log
from usaddress import tag, RepeatedLabelError
from ..standardization.standardizer import label_mappings, label_order
import string

#### READING/PARSING DATA
def csv_to_frame(file_path, id_col, address_col, delimiter = ',', nrows = None):
    result = pd.read_csv(file_path, usecols = [id_col, address_col], \
        sep = delimiter, nrows = nrows)
    result = result.rename(columns = {id_col : 'ID', address_col : 'Address'})
    result = result.set_index('ID')
    return result





"""
input: address, any given address
output: a dict of [label, component] that breaks the address into components
"""
def label_parsing(address):

    try:
        # make case insensitive, apply usaddress parsing
        tagged = tag(address.upper(), label_mappings)
    # exit if parsing fails 
    except RepeatedLabelError:
        return {'ERROR' : address}

    tagged = tagged[0]
    # remove punctuation from results (not removed beforehand, as punctuation can affect parsing)
    stripped = {label: words if label == 'HN' else \
        words.translate(str.maketrans('', '', string.punctuation)).strip() \
            for (label, words) in tagged.items()}

    if 'HN' in stripped:
        HN = stripped['HN']
        separator = "".join([x for x in HN if not x.isnumeric()])
        if separator:
            parts = HN.split(separator)
            if len(parts) == 2:
                    stripped["HN1"] = parts[0]
                    stripped["HNSEP"] = separator
                    stripped["HN2"] = parts[1]

    # add concatenated WSN
    if "WSDESC1" in stripped or "WSID1" in stripped:
        if "WSDESC1" not in stripped:
            stripped["WS"] = stripped["WSID1"]
        elif "WSID1" not in stripped:
            stripped["WS"] = stripped["WSDESC1"]
        else:
            stripped["WS"] =" ".join([stripped["WSDESC1"], stripped["WSID1"]])
    return stripped


def parse_df(input_df, original = False):


    
    result_df = pd.DataFrame(list(input_df['Address'].apply(label_parsing)), \
        index = input_df.index, columns = label_order)
    if original:
        result_df['Address'] = input_df['Address']
    
    return result_df



"""
inputs
    raw_records: incoming address records
    columns: the columns for corrections/scoring
    blocking: parsed address features to block on
    show_errors: a flag to return the optional errors output

outputs:
    blocks_dict: a dict of block values to blocked dataframes with the given columns
    errors: an optional output, of records that failed to standardize properly
"""
def process_data(documents, columns, blocking = None, show_errors = False):
    data = parse_df(documents)

    # columns = ['OSN', ...]
    #this should always be disjoint with blocking cols

    errors = pd.DataFrame([], columns = ["ERROR"])
    #ERROR HANDLING
    if show_errors and 'ERROR' in data.columns:
        errors.append(data['ERROR'].dropna())

    block_keys = ["UNBLOCKED"]

    # GROUPING/BLOCKING
    if blocking is not None:
        # I know, not a great solution, but I don't have pandas 1.1 
        data = data.fillna({cat: "NaN" for cat in blocking})
        blocked = data.groupby(blocking)
        block_keys = blocked.groups.keys()
        ## doing a multiindex would make more sense
        block_dict = {blk: blocked.get_group(blk)[columns] for blk in block_keys}
    else: 
        block_dict = {blk: data[columns] for blk in block_keys}
    return (block_dict, errors) if show_errors else block_dict


### CORPUS HANDLING/SCORING


def aggregate_counts(documents):
    return documents.value_counts().apply(log)

"""
converts a raw dataframe into the score values for spell checking
inputs:
    block_dict: a dict of [block, dataframe] of parsed addresses, from process_data
outputs:
    scores: a Dict[block_key, dataframe] with each frame having aggregated counts
            of terms for each column
"""
def score_corpus(block_dict):

    scores = {}
    for key, block in block_dict.items():
        category_dicts = {}
        for category in block:
            category_dicts[category] = aggregate_counts(block[category])
        scores[key] = category_dicts

    return scores




### SEARCHING


"""
inputs:
    queries_dict: a dict of [block, dataframe] of queried addresses, from process_data
    scores: a dict of [block, dataframe] from score 
    threshold: minimum score to replace a word
    n_distance: minimum edit distance to consider a substitution
output:
    a dict of [block, dataframe], with words in the dataframe correctly substituted
"""

def correct_corpus(queries_dict, scores, threshold = 1, n_distance = None):

    results = {}

    for key, block in queries_dict.items():

        results[key] = pd.DataFrame([], columns = block.columns)
        # handle not found case
        block_scores = scores.get(key)
        # TODO: handle block not found
        if block_scores is None:
            block_scores = pd.DataFrame([], columns = block.columns)

        # iterate through columns
        for entry in block:
            results[key][entry] = block[entry].apply(search_query, scores = \
                block_scores[entry], threshold = threshold, n_distance = n_distance)

    return results






"""
inputs:
    query: address, or address part(?) 
    scores: the pandas series corresponding with this address label & in this block
    n_distance: if you have a certain DL distance to serach within; n_distance must be >= 0
    threshold: cutoff for a meaningful score; level of certainty needed to correct
    show_scores: display the score values for results
    all_matches: show all matches above the threshold, instead of top result
outputs: 
"""
def search_query(query, scores, threshold = 1, n_distance = None, \
    show_scores = False, all_matches = False):

    default_result = (query, threshold)

    if n_distance is not None:
        DL_scores = candidates(query, scores, n_distance)                
    else:
        DL_scores = pd.Series(scores.index, index = scores.index).\
            astype(str).apply(damerau_levenshtein_distance, s2 = str(query))

    # TODO: play around with the scoring formula
    scores = ((10.0**(1-DL_scores))*scores).dropna()

    # list of all viable matches
    if all_matches:
        results = scores[lambda score : score > threshold]
        if results.empty:
            results = pd.Series(threshold, index = [query])
        return results.indexes if not show_scores else results

    # find the top match
    else:
        if not scores.empty:
            top_word = scores.idxmax()
            top_score = scores[top_word]
            if top_score > default_result[1]:
                default_result = (top_word, top_score)
        return default_result[0] if not show_scores else default_result


# # TODO: evaluate need for subtracting one for an exact match
# # subtracting count by one for the exact match is only needed if you're
# # correcting a query from within the corpus
# def score_correction(query, correction, count):
#     DL = damerau_levenshtein_distance(query, correction)
#     if DL == 0:
#         if count == 1:
#             return 0
#         else:
#             return log(count-1)*(10**(1-DL))
#     else:
#         return log(count)*(10**(1-DL))


##### GENERATE POSSIBLE MATCHES
"""
returns the possible candidates to consider
-- will return an exact match if present, then distance-one, then distance two, then no corrections
-- runtime scales mainly with length of query, not corpus

-- may have holes for characters outside of A-Z (accents?)
"""
def candidates(word, scores, n, output = "all"): 
    # "Generate possible spelling corrections for word."
    if output == "all":
        return pd.Series({w: distance for distance, corrections in \
            edits_n(word, n).items() for w in corrections if w in scores})
    # maybe a short-circuit "DL distance being closest" kinda deal?
    if output == "nearest":
    # short-circuits once the closest (in D-L) results are found
        for distance, correction_set in edits_n(word, n).items():
            known = {w: distance for w in correction_set if w in scores}
            if len(known) != 0:
                return known

# All combinations that are n away from word
def edits_n(word, n):

    def edits_1(word):
        # All edits that are one edit away from word
        letters    = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    distanced_sets = {0 : {word}}
    for distance in range(n):
        distanced_sets[distance+1] = set(e2 for e1 in \
            distanced_sets[distance] for e2 in edits_1(e1))
    return distanced_sets



#########

# consolidated / flow function
def spellcheck(corpus, checking, columns, blocking = None, n_distance = None, \
    threshold = 1, show_errors = False):
    errors = pd.DataFrame([], columns = ["ERROR"])
    if show_errors:
        corpus, errors1 = process_data(corpus, columns, blocking, show_errors)
        queries, errors2 = process_data(checking, columns, blocking, show_errors)
        errors.append(errors1)
        errors.append(errors2)
    else:
        corpus = process_data(corpus, columns, blocking, show_errors)
        queries = process_data(checking, columns, blocking, show_errors)
    corpus = score_corpus(corpus)

    results = correct_corpus(queries, corpus, threshold, n_distance)

    originals = parse_df(checking)
    for block in results.values():
        originals.update(block)
    originals.fillna("", inplace = True)

    def concat(words_list):
        return " ".join([word for word in words_list if word])
    
    corrected = originals.astype(str).apply(concat, axis = 1)

    return (corrected, errors) if show_errors else results

    ## dump to file