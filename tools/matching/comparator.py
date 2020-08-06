from ..standardization.standardizer import standardize
from collections import OrderedDict
from . import amgScore

# fidCompare: Name, Zip, PreType, SufType, ExtType, PreDir, SufDir
# -> StreetName, Zip, StreetNamePreType, StreetNamePostType, ??? StreetNamePreDirectional, StreetNamePostDirectional
# function: strip needed values; find defaults from amgScore.py
"""
makes a list corresponding to the arguments to fidCompare, with zero if null
input: address_dict, the output of standardize in dict form
##### dict of comparison values?
ouput: the relevant values of address_dict, in appropriate order
Dict[label, word/code] -> List[word/code]
"""
def fid_prepare(address_dict):
    # the labels in order, with their appropriate default/null values
    fid_order = [("OSN", ''), ("ZIP", 0), ("SNPTC", 0), ("SNSTC", 0), \
        ("SNEC", 0), ("SNPDC", 0), ("SNSDC", 0)]
    HN_order = [("HN1", 0), ("HNSEP", ""), ("HN2", 0)]
    WS_order = [("WSDESC1", 0), ("WSID1", 0)]

    # compose a this dict.

    comparison_labels = OrderedDict(fid_order)
    result = [address_dict[label] if label in address_dict else \
        comparison_labels[label] for label in comparison_labels.keys()]
    return result

def fid_pair(in_list, match_list):
    return [item for pair in zip(in_list, match_list) for item in pair]

# def compare(address1, address2):

