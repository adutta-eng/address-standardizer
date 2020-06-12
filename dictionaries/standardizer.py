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

print(usaddress.parse("1214 Georgetown Way"))
print(abbreviate('ALASKA', STATE_ABBREVIATIONS))