import standardizer
import polish
import comparator
from amgScore import fidComparator
from itertools import combinations, product

matchStrings = polish.loadTestData()

#mocking up a fake demo rows here...
testStrings = """
101 north vinebridge street, anytown md 99999
101 north vineridge street, anytown md 99999
101 vinebridge street, anytown md 99999
101 north vine bridge street, anytown md 99999
101 north vine Rridge street, anytown md 99999
101 north pine bridge street, anytown md 99999
101 north pinebridge street, anytown md 99999
101 pinebridge street, anytown md 99999
101 pinebridge street south, anytown md 99999
101 pinebridge street north, anytown md 99999
""".strip().split('\n')

def usAdr2Dict(inTuple):
    outDict = {}
    for item in inTuple:
        outDict[item[1]]=item[0]
    return outDict

def report_format_errors(formatted_dict):
    formatErrors = formatted_dict['errors'] 
    if len(formatErrors)>0:
        print('the following test records failed and require code fixes:')
    for errorLine in formatErrors:
        print(errorLine)
        errorStan = standardizer.standardize(errorLine)
        for item in errorStan:
            print('\t',item[1],item[0])
        print('\n')

def format_strings(address_strings):
    format_dict = {}
    fidRows = []
    formatErrors = []
    for string in address_strings:
        try:
            standard_dict = usAdr2Dict(standardizer.standardize(string))
            formatted_entry = comparator.fid_prepare(standard_dict)
            fidRows.append(formatted_entry)
        except:
            formatErrors.append(string)
    format_dict['matchable'] = fidRows
    format_dict['errors'] = formatErrors
    report_format_errors(format_dict)
    return format_dict

def pairwise_match(cleaned_data):
    scores = []
    counter = 0
    for fidA, fidB in combinations(cleaned_data, 2):
        fid_list = comparator.fid_pair(fidA, fidB)
        fid_score = -1
        counter += 1
        if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):
            fid_score = fidComparator(*fid_list)
        print(fidA, fidB, fid_score)
    print(counter)
    scores.append(fid_score)

def find_matches(setA, setB):
    matchResults = []
    matchTestCounter = 0
    print('looping through match tests')
    
    for entryA, entryB in product(setA, setB):
        matchTestCounter += 1
        if matchTestCounter % 40 == 0:
            print('\tProgress: {}'.format(str(matchTestCounter)))

        fid_list = comparator.fid_pair(entryA, entryB)
        fid_score = -1
        if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):
            fid_score = fidComparator(*fid_list)
        matchResults.append(fid_score)

    return matchResults
        

standardized_testing = format_strings(testStrings)
standardized_match = format_strings(matchStrings)

pairwise_match(standardized_match['matchable'])
pairwise_match(standardized_testing['matchable'])

results = find_matches(standardized_match['matchable'], standardized_testing['matchable'])
anyMatch = [x for x in results if x > 0]
numMatches = len(anyMatch)
print('number of matches between "testStrings" and "matchStrings" (may include duplicates...)',str(numMatches))    
print("Done!")
