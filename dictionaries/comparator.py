from standardizer import standardize
import amgScore

# fidCompare: Name, Zip, PreType, SufType, ExtType, PreDir, SufDir
# -> StreetName, Zip, StreetNamePreType, StreetNamePostType, ??? StreetNamePreDirectional, StreetNamePostDirectional
# function: strip needed values; find defaults from amgScore.py
"""
makes a list corresponding to the arguments to fidCompare, with zero if null
input: address_dict, the output of standardize in dict form
ouput: the relevant values of address_dict, in appropriate order
Dict[label, word/code] -> List[word/code]
"""
def fid_prepare(address_dict):
    # as per SNSDC: ["OSN", "ZIP", "SNPTC", "SNSTC", "SNEC", "SNPDC", "SNSDC"]
    fid_order = ["StreetName", "Zip", "SteetPreTypeCode", "SteetPostTypeCode", "SNEC", "PreDirectionalCode", "PostDirectionalCode"]
    return [address_dict[label] if label in address_dict else 0 for label in fid_order]

def fid_pair(in_list, match_list):
    return [item for pair in zip(in_list, match_list) for item in pair]

# def compare(address1, address2):

