import usaddress

from constants import (
    DIRECTIONAL_ABBREVIATIONS,
    STATE_ABBREVIATIONS,
    STREET_NAME_ABBREVIATIONS,
    STREET_NAME_POST_ABBREVIATIONS,
    OCCUPANCY_TYPE_ABBREVIATIONS
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
        word = category_pair[0]
        address_category = category_pair[1]
        
        # Checks if there is a standardization dictionary for a particular category
        # For example, we want to skip over the SubaddressType since there is no abbreviation for it
        if address_category in label_dict.keys():
            address_category_mappings = label_dict.get(address_category)
            for key in address_category_mappings.keys():
                # If the input word matches one of the keys in the abbreviation dictionary
                # We standardize by converting to the preferred abbreviation
                if key in word:
                    parsed_address[index] = update_tuple(address_category_mappings.get(key), category_pair)
    return(parsed_address)

print(standardize("Homer Spit Road, Homer, Arkansas 99603"))


    # for (word, address_category) in parsed_address:
    #     if address_category in label_dict.keys():
    #         print(word)
    #         print(address_category)
    #         # Dictionary mapping for all possible misspellings of the category to their preferred abbreviations
    #         address_category_mappings = label_dict.get(address_category)
    #         for key in address_category_mappings.keys():
    #             # print(key)
    #             if key in word:
    #                 # parsed_address.pop(word)
    #                 print(type(parsed_address[0]))
    #                 print(type(parsed_address))
    #                 print(update_tuple(address_category_mappings.get(key), (word, address_category)))
                    # print("original word = " + word)
                    # word = address_category_mappings.get(key)
                    # parsed_address[word] = address_category_mappings.get(key)
                    # print("replaced word = " + word)
        
        # if label in label_dict.keys():
        #     corresponding_dict = label_dict.get(label)
        #     print(str(corresponding_dict.get(word)))
            # print(str(label_dict.get(label).keys()))
            # print("type aka label_dict = " + label_dict.get(label))
            # print("word = " + word)
            # print ("matching key in label_dict = " + label_dict.get(label).get(word))
        # if label in label_dict.keys and word in label_dict.get(label).keys:
        #     print(word + " " + label + " " + label_dict.get(label).get(word))