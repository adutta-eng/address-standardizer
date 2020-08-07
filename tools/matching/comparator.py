from ..standardization.standardizer import standardize

# fidCompare: Name, Zip, PreType, SufType, ExtType, PreDir, SufDir
# -> StreetName, Zip, StreetNamePreType, StreetNamePostType, ??? StreetNamePreDirectional, StreetNamePostDirectional
# function: strip needed values; find defaults from amgScore.py


exact_matches = ['HN', 'HNPRE', 'HNSUF', 'WS', 'OccupancyType', 'OccupancyIdentifier']
fid_order = ['OSN', 'ZIP', 'SNPTC', 'SNSTC', 'SNEC', 'SNPDC', 'SNSDC']
HN_order = ['HN', 'HN1', 'HNSEP', 'HN2', 'HNPRE', 'HNSUF']
WS_order = ["WSDESC1", "WSID1"]

label_shortcuts = {'fid_order' : fid_order, 'HN_order' : HN_order, 'WS_order' : \
    WS_order, 'exact_matches' : exact_matches}

all_labels = {
    'OSN': '', 
    'ZIP': 0, 
    'SNPTC': 0, 
    'SNSTC': 0, 
    'SNEC': 0, 
    'SNPDC': 0, 
    'SNSDC': 0, 
    'HN': 0, 
    'HN1': 0, 
    'HNSEP': '', 
    'HN2': 0, 
    'HNPRE': '', 
    'HNSUF': '', 
    'WSDESC1': 0, 
    'WSID1': 0, 
    'WS': '', 
    'OccupancyType': '', 
    'OccupancyIdentifier': 0
}

"""
makes a list corresponding to the arguments to fidCompare, with zero if null
input: address_dict, the output of standardize in dict form
       labels, specific values for the function to pull from the dict
       substitutions, the default value if the label isn't in address_dict 
ouput: the relevant values of address_dict, in order, substituted if absent
Dict[label, word/code] -> List[word/code]
"""
def pull_labels(address_dict, labels = fid_order, substitutions = None):
        
    # add in any extra substitutions
    if substitutions is not None:
        master_substitutions = {**all_labels, **dict(substitutions)}
    else:
        master_substitutions = all_labels

    # add any quick label packages
    comparison_labels = []
    for label in labels:
        if label in label_shortcuts:
            comparison_labels.extend(label_shortcuts[label])
        else:
            comparison_labels.append(label)     
    
    result = [address_dict[label] if label in address_dict else \
        master_substitutions[label] for label in comparison_labels]
    return result



def pair_values(in_list, match_list):
    return [item for pair in zip(in_list, match_list) for item in pair]

