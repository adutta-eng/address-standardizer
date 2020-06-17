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

# A mapping between each usaddress category to its standardizing dictionary
label_dict = {
    'StreetNamePostType' : STREET_NAME_POST_ABBREVIATIONS,
    'StreetNamePreDirectional' : DIRECTIONAL_ABBREVIATIONS,
    'StreetNamePostDirectional' : DIRECTIONAL_ABBREVIATIONS,
    'StateName' : STATE_ABBREVIATIONS,
    'SubaddressType' : OCCUPANCY_TYPE_ABBREVIATIONS
}

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

# Since tuples are immutable this function is needed when replacing values during standardization
# @param replacement_word = the standardized value for the category type given user input
# @param original_tuple = a category pair from parsed usaddress containing (user_input_value, corresponding_category)
# @return an updated tuple: (replacement_word, corresponding_category)
def update_tuple(replacement_word, original_tuple):
    converted_list = list(original_tuple)
    converted_list[0] = replacement_word
    return(tuple(converted_list))

# @param unparsed_address = an input address
# @return = list of tuples matching each category above to a standardized value
def standardize(unparsed_address):
    # Standardize the case to avoid conflicts between lower/upper case words
    unparsed_address = unparsed_address.upper()

    # Abbreviate the existence of any full state names if they are present in the streetname or otherwise
    for key in STATE_ABBREVIATIONS:
        if key in unparsed_address.split():
            unparsed_address = unparsed_address.replace(key, STATE_ABBREVIATIONS.get(key))
    
    # Parse the address using usaddress to utilize dictionary labels
    # parsed_address = a list of tuples
    parsed_address = usaddress.parse(unparsed_address)

    # Iterate through each tuple in our parsed_address, index is necessary for making conversions
    for index in range(len(parsed_address)):
        # category_pair contains a part of an address an its corresponding category
        # for example (NORTH, StreetNamePreDirectional)
        category_pair = parsed_address[index]
        word = category_pair[0].translate(str.maketrans('', '', string.punctuation)) #strips punctuation
        address_category = category_pair[1]
        
        # Checks if there is a standardization dictionary for a particular category
        # For example, we want to skip over the SubaddressType since there is no abbreviation for it
        if address_category in label_dict.keys():
            address_category_mappings = label_dict.get(address_category)
            for key in address_category_mappings.keys():
                # If the input word matches one of the keys in the abbreviation dictionary
                # We standardize by converting to the preferred abbreviation
                if key == word:
                    parsed_address[index] = update_tuple(address_category_mappings.get(key), category_pair)
    
    # Add direction codes and occupancy codes by appending another tuple to parsed_address when a match occurs
    for (word, label) in parsed_address:
        if label == "StreetNamePostDirectional":
            post_directional_code = (DIRECTION_CODES.get(word), "PostDirectionalCode")
            parsed_address.append(post_directional_code)
        if label == "StreetNamePreDirectional":
            pre_directional_code = (DIRECTION_CODES.get(word), "PreDirectionalCode")
            parsed_address.append(pre_directional_code)
        if label == "StreetNamePostType":
            if word in OCCUPANCY_TYPE_CODES.keys():
                parsed_address.append((OCCUPANCY_TYPE_CODES.get(word), "OccupancyTypeCode"))

    return(parsed_address)

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