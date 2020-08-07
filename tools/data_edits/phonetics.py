import phonetics
import editdistance
import fuzzy
from itertools import combinations, product

print(phonetics.dmetaphone('catherine'))
print(phonetics.dmetaphone('kathryn'))
print(phonetics.dmetaphone('335 Deinhard Lane, Mc Call, ID 83638'))
print(phonetics.dmetaphone('5105 Berwyn Road, College Park, MD 20740'))
print(phonetics.dmetaphone('5105 Berwin Road, College Park, MD 20740'))

name1 = '5105 Berwyn Road, College Park, MD 20740'
name2 = '5105 Berwin Road, College Park, MD 20740'
name3 = '335 Deinhard Lane, Mc Call, ID 83638'
nysiis_score = editdistance.eval(fuzzy.nysiis(name1), fuzzy.nysiis(name2))
other_nysiis_score = editdistance.eval(fuzzy.nysiis(name1), fuzzy.nysiis(name3))
print(nysiis_score)
print(other_nysiis_score)

#copied over from polish.py
def loadTestData(inPath = r'testData.txt' ):
    testDataPath = inPath
    with open(testDataPath, 'r') as temp:
        testData = [x[:-1] for x in temp.readlines()]
    return testData

matchStrings = loadTestData()

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
5105 Berwin Road, College Park, MD 20740
""".strip().split('\n')

#Given the tuple output by usaddress, return a dictionary
def usAdr2Dict(inTuple):
    outDict = {}
    for item in inTuple:
        outDict[item[1]]=item[0]
    return outDict

#Given a dictionary of formatted errors, report each address
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

#Given two raw input files, standardize and clean each address
#output a formatted dictionary containing each category and its standardized result
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

#Deduplicate all the adddresses within a single cleaned file
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

#Identify all matches between two standardized files
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

#return output as dataframe
def find_matches_in_df(setA, setB):
    df = pd.DataFrame(columns = ['Address 1', 'Address 2', 'FidScore'])
    matchTestCounter = 0
    for entryA, entryB in product(setA, setB):
        fid_list = comparator.fid_pair(entryA, entryB)
        fid_score = -1
        if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):
            fid_score = fidComparator(*fid_list)
        df.loc[matchTestCounter] = [entryA, entryB, fid_score]
        matchTestCounter += 1
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(df)
    return df

def find_matches_output_file(setA, setB, file_path):
    f = open(file_path, "w")
    for entryA, entryB in product(setA, setB):
        fid_list = comparator.fid_pair(entryA, entryB)
        fid_score = -1
        if (isinstance(fid_list[0], str) and isinstance(fid_list[1], str)):
            fid_score = fidComparator(*fid_list)
        # nysiis_score = editdistance.eval(fuzzy.nysiis(entryA), fuzzy.nysiis(entryB))

        string_entryA = ', '.join([str(item) for item in entryA])
        string_entryB = ', '.join([str(item) for item in entryB])
        f.write(string_entryA + " | " + string_entryB + " | " + str(fid_score) + " | " + str(nysiis_score) + "\n")
    f.close()

def find_phonetic_matches(setA, setB, file_path):
    f = open(file_path, "w")
    for entryA, entryB in product(setA, setB):
        nysiis_score = editdistance.eval(fuzzy.nysiis(entryA), fuzzy.nysiis(entryB))
        f.write(entryA + " | " + entryB + " | " + str(nysiis_score) + "\n")
    f.close()


standardized_testing = format_strings(testStrings)
standardized_match = format_strings(matchStrings)

pairwise_match(standardized_match['matchable'])
pairwise_match(standardized_testing['matchable'])

find_matches_output_file(standardized_match['matchable'], standardized_testing['matchable'], "match.txt")
find_phonetic_matches(testStrings, matchStrings, 'phonetics.txt')
