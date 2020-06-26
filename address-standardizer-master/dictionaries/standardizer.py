import usaddress
import string
from constants import (
    DIRECTIONAL_ABBREVIATIONS,
    STATE_ABBREVIATIONS,
    STREET_NAME_ABBREVIATIONS,
    STREET_NAME_POST_ABBREVIATIONS,
    OCCUPANCY_TYPE_ABBREVIATIONS,
    STREET_POST_TYPE_CODES,
    DIRECTION_CODES
)

def abbreviate(potential_key, dictionary):
    if potential_key in dictionary:
        return dictionary.get(potential_key)
    else:
        return potential_key

# USADDRESS CATEGORIES THAT WE ARE CONCERNED WITH
# AddressNumberPrefix
# AddressNumber
# AddressNumberSuffix
# StreetNamePreModifier
# StreetNamePreDirectional
# StreetNamePreType
# StreetName
# StreetNamePostType
# StreetNamePostDirectional
# SubaddressType
# SubaddressIdentifier
# BuildingName?

# built for usaddress.parse, not usaddress.tag
# very preliminary, can be improved; let's talk about if we should parse replacements outside of specific labels
# applies abbreviate to each word parsed by usaddress

# input: parsed_address - output from usaddress.parse, in format List[(word, label)]
#        master_dict - a dict of dicts of substitutions, in format Dict[label, Dict[word, substitution]
# output: a parsed address with words substituted when possible, in format List[(substitution, label)]
# List[(String, String)], Dict[String, Dict[String, String]] -> List[(String, String)] 
def clean(parsed_address, master_dict):
    return [(abbreviate(word, master_dict.get(label)), label) if label in master_dict else (word, label) for (word, label) in parsed_address]

# TODO: change to a map from label to individualized function (?)
label_dict = {
    'StreetNamePostType' : STREET_NAME_POST_ABBREVIATIONS,
    'StreetNamePreType' : STREET_NAME_POST_ABBREVIATIONS,
    'StreetNamePreDirectional' : DIRECTIONAL_ABBREVIATIONS,
    'StreetNamePostDirectional' : DIRECTIONAL_ABBREVIATIONS,
    'StateName' : STATE_ABBREVIATIONS,
    'SubaddressType' : OCCUPANCY_TYPE_ABBREVIATIONS,
    'StreetName' : STATE_ABBREVIATIONS # not sure if we want this for only StreetName; should "Washington Heights" in NYC become "WA HTS"?
}
# not sure what category street name substitutions fall under

# substitution codes
code_dict = {
    'StreetNamePostDirectional' : DIRECTION_CODES,
    'StreetNamePreDirectional' : DIRECTION_CODES,
    #'StreetNamePostType' : OCCUPANCY_TYPE_CODES
}

code_label_dict = {
    'StreetNamePostDirectional' : 'PostDirectionalCode',
    'StreetNamePreDirectional' : 'PreDirectionalCode',
    'StreetNamePostType' : 'OccupancyTypeCode'
}


# function dict
# processing_dict = {
#     'StreetNamePostType' : (lambda x : abbreviate(x, STREET_NAME_POST_ABBREVIATIONS)),
#     'StreetNamePreType' : (lambda x : abbreviate(x, STREET_NAME_POST_ABBREVIATIONS)),
#     'StreetNamePreDirectional' : (lambda x : abbreviate(x, DIRECTIONAL_ABBREVIATIONS)),
#     'StreetNamePostDirectional' : (lambda x : abbreviate(x, DIRECTIONAL_ABBREVIATIONS)),
#     'StateName' : (lambda x : abbreviate(x, STATE_ABBREVIATIONS)),
#     'SubaddressType' : (lambda x : abbreviate(x, OCCUPANCY_TYPE_ABBREVIATIONS)),
#     'StreetName' : (lambda x : abbreviate(x, STATE_ABBREVIATIONS))
# }


# label_mappings = {
#     'AddressNumberPrefix' : 'HNPRE',
#     'AddressNumber' : 'HN1', # requires parsing into HN2 and HNSEP
#     'AddressNumberSuffix' : 'HNSUF',
#     'StreetNamePreModifier' : 'OSN', # will concat w/ StreetName
#     'StreetNamePreDirectional' : 'SNPD',
#     'StreetNamePreType' : 'SNST',
#     'StreetName': 'OSN',
#     'StreetNamePostType' : 'SNST',
#     'StreetNamePostModifier' : 'SNE', # Not sure if this is the correct correspondence
#     'StreetNamePostDirectional' : 'SNSD',
#     'SubaddressType' : 'WSD',
#     'SubaddressIdentifier' : 'WSI',
#     'BuildingName' : 'SI',
#     'OccupancyType',
#     'OccupancyIdentifier',
#     'CornerOf',
#     'LandmarkName',
#     'PlaceName',
#     'StateName',
#     'ZipCode' : 'ZIP',
#     'USPSBoxType',
#     'USPSBoxID' : 'BXI',
#     'USPSBoxGroupType',
#     'USPSBoxGroupID',
#     'IntersectionSeparator',
#     'Recipient',
#     'NotAddress',
# }

# input: address, any given address
#        code, which can be "a" (append), "r" (replace), or "n" (none)
#        output, which can be "l" (list) or "d" (dictionary)
# output: a list formatted like that of usaddress.parse, but with certain key words abbreviated and standardized
# String -> List[(word: String, label: String)]
def standardize(address, code = "a", output = "l"):
    if code not in ["a", "r", "n"]:
        raise InputError("code must be a (append), r (replace), or n (none)")
    if output not in ["l", "d"]:
        raise InputError("output must be l (list) or d (dict)")
    # make case insensitive, apply usaddress parsing
    parsed = usaddress.parse(address.upper())
    # remove punctuation from results (not removed beforehand, as punctuation can affect parsing)
    stripped = [(word.translate(str.maketrans('', '', string.punctuation)), label) for (word, label) in parsed]
    # apply replacements
    substituted = clean(stripped, label_dict)
    # add codes for directions, extensions, etc.
    if code != "n":
        if code == "a":
            for (word, label) in substituted:
                # confirm label is substitutable
                if label in code_dict and label in code_label_dict:
                    # confirm substitution is known
                    if word in code_dict[label]:
                        # append to the end of the list
                        substituted.append((code_dict[label].get(word), code_label_dict[label]))
        if code == "r":
            for index in range(len(substituted)):
                # confirm label is substitutable
                word, label = substituted[index]
                if label in code_dict and label in code_label_dict:
                    # confirm substitution is known
                    if word in code_dict[label]:            
                        substituted[index] = (code_dict[label].get(word), code_label_dict[label])
    if output == 'd':
        result = {}
        for (word, label) in substituted:
            if label in result:
                result[label] = result[label] + " " + word
            else:
                result[label] = word
        return result
    else:
        return substituted

# fidCompare: Name, Zip, PreType, SufType, ExtType, PreDir, SufDir
# -> StreetName, Zip, StreetNamePreType, StreetNamePostType, StreetNamePreDirectional, StreetNamePostDirectional
# function: strip needed values; find defaults from amgScore.py
		
if __name__== '__main__':
    """
    condition allows for 'interactive' testing and development when not being used as a library
    
    None of this will be run when it is "imported" which is helpful/cleaner
    """
    #as a rule, try to avoid typing the same term over and over again, a standard input file helps with testing
    testDataPath = r'testData.txt' # stored in current dir, for reasons...
    with open(testDataPath, 'r') as temp:
        data = [x[:-1] for x in temp.readlines()] #no header, 1 line per input, remove newline character
    
    for item in data[3:]:
        print('\n\n\nraw input string:\t\t', item, '\n\nusaddress standardized output:')
        print(standardize(item))
        break
        
    print('\n\nDone!') #old habits die hard, helpful to know if something is hanging...
		
