from ..standardization.standardizer import standardize
from collections import OrderedDict
# from . import amgScore

# fidCompare: Name, Zip, PreType, SufType, ExtType, PreDir, SufDir
# -> StreetName, Zip, StreetNamePreType, StreetNamePostType, ??? StreetNamePreDirectional, StreetNamePostDirectional
# function: strip needed values; find defaults from amgScore.py
fid_order = [("OSN", ''), ("ZIP", 0), ("SNPTC", 0), ("SNSTC", 0), \
    ("SNEC", 0), ("SNPDC", 0), ("SNSDC", 0)]
HN_order = [('HN', 0), ("HN1", 0), ("HNSEP", ""), ("HN2", 0), ('HNPRE', ""), ('HNSUF', "")]
WS_order = [("WSDESC1", 0), ("WSID1", 0)]

exact_matches =  [('HN', 0), ('HNPRE', ""), ('HNSUF', ""), ('WS', ""), \
    ('OccupancyType', ""), ('OccupancyIdentifier', 0)]
exact_match_labels =  ['HN', 'HNPRE', 'HNSUF', 'WS', 'OccupancyType', 'OccupancyIdentifier']

label_shortcuts = {'fid' : fid_order, 'HN' : HN_order, 'WS' : \
    WS_order, 'exact' : exact_matches}


"""
makes a list corresponding to the arguments to fidCompare, with zero if null
input: address_dict, the output of standardize in dict form
       labels, specific values for the function to pull from the dict
##### dict of comparison values?
ouput: the relevant values of address_dict, in appropriate order, substituted appropriately if absent
Dict[label, word/code] -> List[word/code]
"""
# def fid_prepare(address_dict):
#     # the labels in order, with their appropriate default/null values
#     fid_order = [("OSN", ''), ("ZIP", 0), ("SNPTC", 0), ("SNSTC", 0), \
#         ("SNEC", 0), ("SNPDC", 0), ("SNSDC", 0)]
#     HN_order = [("HN1", 0), ("HNSEP", ""), ("HN2", 0)]
#     WS_order = [("WSDESC1", 0), ("WSID1", 0)]

#     # compose a this dict.


#     comparison_labels = OrderedDict(fid_order)
#     result = [address_dict[label] if label in address_dict else \
#         comparison_labels[label] for label in comparison_labels.keys()]
#     return result


def pull_labels(address_dict, labels = ['fid']):
    # the labels in order, with their appropriate default/null values
    full_order = []
    for label in labels:
        if label in label_shortcuts:
            full_order.extend(label_shortcuts[label])
        else:
            full_order.append(label)
    # full_order = [label  for label in labels if label not in label_shortcuts else l for l in label_shortcuts[label]]
    # compose a full dict
    comparison_labels = OrderedDict(full_order)
    
    result = [address_dict[label] if label in address_dict else \
        comparison_labels[label] for label in comparison_labels.keys()]
    return result



def pair_values(in_list, match_list):
    return [item for pair in zip(in_list, match_list) for item in pair]

