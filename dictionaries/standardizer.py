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
    'StreetNamePostType' : OCCUPANCY_TYPE_CODES
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
# output: a list formatted like that of usaddress.parse, but with certain key words abbreviated and standardized
# String -> List[(word: String, label: String)]
def standardize(address):
    # make case insensitive, apply usaddress parsing
    parsed = usaddress.parse(address.upper())
    # remove punctuation from results (not removed beforehand, as punctuation can affect parsing)
    stripped = [(word.translate(str.maketrans('', '', string.punctuation)), label) for (word, label) in parsed]
    # apply replacements
    substituted = clean(stripped, label_dict)
    # add codes for directions, extensions, etc.
    for (word, label) in substituted:
        # confirm label is substitutable
        if label in code_dict and label in code_label_dict:
            # confirm substitution is known
            if x in code_dict[label]:
                # append to the end of the list
                substituted.append((code_dict[label].get(word), code_label_dict[label]))
    return substituted


print(usaddress.parse("1214 Georgetown Way"))
print(abbreviate('ALASKA', STATE_ABBREVIATIONS))
print(clean(usaddress.parse("1214 Georgetown Way"), label_dict))
print(standardize("Homer Spit Road, Homer, Arkansas 99603"))
print(standardize("Lnlck Shopping Center, Anniston, AL 36201"))
print(standardize("Center Ridge, AR 72027"))
print(standardize("9878 North Metro Parkway East, Phoenix, AZ 85051"))
print(standardize("2896 Fairfax Street, Denver, CO 80207"))
print(standardize("Mesa Mall, Grand Junction, CO 81501"))
print(standardize("168 Hillside Avenue, Hartford, CT 06106"))
print(standardize("1025 Vermont Avenue Northwest, Washington, DC 20005"))
print(standardize("697 North Dupont Boulevard, Milford, DE 19963"))
print(standardize("1915 North Republic De Cuba Avenue, Tampa, FL 33602"))
print(standardize("2406 North Slappey Boulevard, Albany, GA 31701"))
print(standardize("98-1247 Kaahumanu, Aiea, HI 96701"))
print(standardize("103 West Main, Ute, IA 51060"))
print(standardize("335 Deinhard Lane, Mc Call, ID 83638"))
print(standardize("8922 South 1/2 Greenwood Avenue, Chicago, IL 60619"))
print(standardize("239 West Monroe Street, Decatur, IN 46733"))
print(standardize("827 Frontage Road, Agra, KS 67621"))
print(standardize("508 West 6th Street, Lexington, KY 40508"))
print(standardize("5103 Hollywood Avenue, Shreveport, LA 71109"))
print(standardize("79 Power Road, Westford, MA 01886"))
print(standardize("5105 Berwyn Road, College Park, MD 20740"))
print(standardize("47 Broad Street, Auburn, ME 04210"))
print(standardize("470 South Street, Ortonville, MI 48462"))
print(standardize("404 Wilson Avenue, Faribault, MN 55021"))
print(standardize("5933 Mc Donnell Boulevard, Hazelwood, MO 63042"))
print(standardize("918 East Main Avenue, Lumberton, MS 39455"))
print(standardize("107 A Street East, Poplar, MT 59255"))
print(standardize("Village Shps Of Bnr, Banner Elk, NC 28604"))
print(standardize("2601 State Street, Bismarck, ND 58501"))
print(standardize("207 South Bell Street, Fremont, NE 68025"))
print(standardize("107 State Street, Portsmouth, NH 03801"))
print(standardize("1413 State Highway #50, Mays Landing, NJ 08330"))
print(standardize("I-25 Highway 87, Raton, NM 87740"))
print(standardize("516 West Goldfield Avenue, Yerington, NV 89447"))
print(standardize("2787 Bway Way, New York, NY 10001"))
print(standardize("1380 Bethel Road, Columbus, OH 43220"))
print(standardize("305 Main, Fort Cobb, OK 73038"))
print(standardize("17375 Southwest Tualatin Valley Hwy, Beaverton, OR 97006"))