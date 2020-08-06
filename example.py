# from standardization.standardizer import standardize

# print(standardize("1025 Vermont Avenue Northwest, Washington, DC 20005"))

# from .tools.matching import keyMatch

import sys
sys.path.append(r"C:\Users\aisha\CensusCDF\address-standardizer")

from tools.matching import keyMatch

frameA = keyMatch.csv_to_frame("comparisonData.csv", "CUSTID", "ADDRESS", delimiter='|')
frameB = keyMatch.csv_to_frame("testData.csv", "CUSTID", "ADDRESS", delimiter='|')

print(keyMatch.records_to_matches(frameA, frameB, show_errors=False))

print(keyMatch.records_to_matches(frameA, show_errors=False))