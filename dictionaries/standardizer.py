import usaddress
from constants import (
    DIRECTIONAL_ABBREVIATIONS,
    STATE_ABBREVIATIONS,
    STREET_NAME_ABBREVIATIONS,
    STREET_NAME_POST_ABBREVIATIONS
)

## Checks if a potential key is contained in a dictionary 
## Returns corresponding value if so.
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
def clean(parsed_address, master_dict):
    return [(abbreviate(word, master_dict.get(label)), label) for (word, label) in parsed_address]

label_dict = {
    'StreetNamePostType' : STREET_NAME_POST_ABBREVIATIONS,
    'StreetNamePreDirectional' : DIRECTIONAL_ABBREVIATIONS,
    'StreetNamePostDirectional' : DIRECTIONAL_ABBREVIATIONS,
    'StateName' : STATE_ABBREVIATIONS    
}
# not sure what category street name substitutions fall under

print(usaddress.parse("1214 Georgetown Way"))
print(abbreviate('ALASKA', STATE_ABBREVIATIONS))
