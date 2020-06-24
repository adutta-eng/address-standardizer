# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 08:30:45 2020

@author: watso330
"""
print('Loading custom libraries, these might not be optimized yet...')
import standardizer
import polish
from amgScore import fidComparator
from itertools import combinations, product

#test using training data from file
#spilers, the standaridzation training data isn't actually useful for 
#deduplication examples
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


formatErrors = []
fidRows = []

for line in testStrings:
    try:
        fidLine = polish.format4FidCompare(line)
        fidRows.append(fidLine)
    except:
        formatErrors.append(line)
        
#"standardize" second dataset using identical logic, maybe a function next time?
formatErrors2 = []
fidRows2 = []

for line in matchStrings:
    try:
        fidLine = polish.format4FidCompare(line)
        fidRows2.append(fidLine)
    except:
        formatErrors2.append(line)        

#find errors, report out
if len(formatErrors)>0:
    print('the following test records failed and require code fixes:')
    for errorLine in formatErrors:
        print(errorLine)
        errorStan = standardizer.standardize(errorLine)
        for item in errorStan:
            print('\t',item[1],item[0])
        print('\n')


#using combinations to do pairwise matching within a single dataset, good for "deduplication"
scoreResults1 = []
dedupCounter = 0
print('verbose deduplication testing results:')
for fidA, fidB in combinations(fidRows, 2):
    dedupCounter = dedupCounter + 1
    fidList = polish.fidPairMerge(fidA,fidB)
    fidScore = fidComparator(*fidList)
    print(fidA, fidB, fidScore)
    scoreResults1.append(fidScore)
print('\n\n')

#a nested for loop would work, but so will itertools.product
matchResults = []
matchScores = []
matchTestCounter = 0
print('looping through match tests')
for fidA, fidB in product(fidRows, fidRows2):
    matchTestCounter=matchTestCounter+1
    if matchTestCounter%40==0:
        print('\tProgress: {}'.format(str(matchTestCounter)))
    fidList = polish.fidPairMerge(fidA,fidB)
    fidScore = fidComparator(*fidList)
    #print(fidA, fidB, fidScore)
    matchResults.append(fidScore)

#are there any matches?  I "cheated" and rigged the data so there should be

anyMatch = [x for x in matchResults if x > 0]
numMatches = len(anyMatch)
print('number of matches between "testStrings" and "matchStrings" (may include duplicates...)',str(numMatches))    
print("Done!")