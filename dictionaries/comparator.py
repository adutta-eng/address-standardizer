from standardizer import standardize
from collections import OrderedDict
import amgScore

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
    # as per SNSDC: ["OSN", "ZIP", "SNPTC", "SNSTC", "SNEC", "SNPDC", "SNSDC"]
    # the labels in order, with their appropriate default/null values
    fid_order = OrderedDict([("OSN", ''), ("ZIP", 0), ("SNPTC", 0), ("SNSTC", 0), \
        ("SNEC", 0), ("SNPDC", 0), ("SNSDC", 0)])
    
    # # could theoretically get rid of the list & use an ordered dict but that's a lot of work
    # fid_defaults = {"OSN", '', "ZIP", 0, "SNPTC", 0, "SNSTC", 0, "SNEC", 0, "SNPDC", 0, "SNSDC", 0}
    # HN_order = ["HN1", "HNSEP", "HN2"]
    HN_order =OrderedDict([("HN1", 0), ("HNSEP", ""), ("HN2", 0)])
    WS_order = OrderedDict([("WSDESC1", 0), ("WSID1", 0)])
    #["StreetName", "Zip", "SteetPreTypeCode", "SteetPostTypeCode", "SNEC", "PreDirectionalCode", "PostDirectionalCode"]
    # figure out how this works in dataframes/NaN/nulls? .isnull?
    result = [address_dict[label] if label in address_dict else \
        fid_order[label] for label in fid_order.keys()]
    # result[0] = str(result[0])
    # result[1] = str(result[1])
    #is this the appropriate way to handle this?
    return result

def fid_pair(in_list, match_list):
    return [item for pair in zip(in_list, match_list) for item in pair]

# def compare(address1, address2):

