import usaddress
import string
from constants import (
    DIRECTIONAL_ABBREVIATIONS,
    STATE_ABBREVIATIONS,
    STREET_NAME_ABBREVIATIONS,
    STREET_NAME_POST_ABBREVIATIONS,
    OCCUPANCY_TYPE_ABBREVIATIONS,
    OCCUPANCY_TYPE_CODES,
    DIRECTION_CODES
)


def abbreviate(potential_key, dictionary):
    if potential_key in dictionary:
        return dictionary.get(potential_key)
    else:
        return potential_key

test_input_a = ">Mi >K Beach Road #2, Kenai, AK 99611"
print(usaddress.parse(test_input_a))

# USADDRESS
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

# def clean(parsed_address, master_dict):
#     result = []
#     for (word, label) in parsed_address:
#         if label in master_dict:
#             function = master_dict[label]
#             result.append(tuple(function(word), label))
#         else:
#             result.append((word, label))
#     return result
#     return [(master_dict[label](word), label) if label in master_dict else (word, label) for (word, label) in parsed_address]

# TODO: change to a map from label to individualized function
	
	
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
# output: a list formatted like that of usaddress.parse, but with certain key words abbreviated and standardized
# String -> List[(word: String, label: String)]
def process(address):
    # make case insensitive, apply usaddress parsing
    parsed = usaddress.parse(address.upper())
    # remove punctuation from results (not removed beforehand, as punctuation can affect parsing)
    stripped = [(word.translate(str.maketrans('', '', string.punctuation)), label) for (word, label) in parsed]
    # apply replacements
    return clean(stripped, label_dict)
	
	
print(usaddress.parse("1214 Georgetown Way"))
print(abbreviate('ALASKA', STATE_ABBREVIATIONS))
print(clean(usaddress.parse("1214 Georgetown Way"), label_dict))
