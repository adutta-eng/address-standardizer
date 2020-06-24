# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 08:20:43 2020

@author: watso330
"""


import standardizer, os, amgScore


def loadTestData(inPath = r'testData.txt' ):
    testDataPath = inPath
    with open(testDataPath, 'r') as temp:
        testData = [x[:-1] for x in temp.readlines()]
    return testData



#load stancodes from textfile...
metadataDir = r'\\It171oafs-oa06.boc.ad.census.gov\RM_SHARED\Frames\Geospatial Frame\Data\metadata'
#did someone make an empty untyped file?
"""
\\It171oafs-oa06.boc.ad.census.gov\RM_SHARED\Frames\Geospatial Frame\Data\metadata\mafdata_StanCode
"""

stanCodePath = os.path.join(metadataDir,'mafdata_StanCode.csv')
with open(stanCodePath, 'r') as temp:
    stanData = [x[:-1].split('|') for x in temp.readlines()[1:]]

stanCode = {}
for row in stanData:
    categoryVal = row[2]
    descrVal = row[1]
    codeVal = int(row[0]) #this needs to eventually be an int, so do it now
    if categoryVal not in stanCode.keys():
        #only need to initailize once
        stanCode[categoryVal]={}
        #I've become a big fan of symetric dictionaries so I can convert back and forth between the code value and the lookup value
        stanCode[categoryVal][descrVal]=codeVal
        stanCode[categoryVal][codeVal]=descrVal
    else:
        #need to populate every time
        stanCode[categoryVal][descrVal]=codeVal
        stanCode[categoryVal][codeVal]=descrVal        



def format4FidCompare(inAddrString):
    adrStrA = inAddrString
    #I'm going to hard code this part, but there are smarter ways to do this
    """
    use this as a simple reference address with important fields
    standardizer.standardize('101 north main street apartment 1 anytown md 99999')
    """
    simpleCrossWalk = {}
    simpleCrossWalk['StreetName']='OSN'
    simpleCrossWalk['ZipCode']='ZIP'
    simpleCrossWalk['StreetNamePreType']='SNPTC' #this term will be repeated for an input like "county road" so at some point a simple patch will be needed
    simpleCrossWalk['StreetNamePostType']='SNSTC'
    #this is sloppy but its a demo, just kludge SNEC for now
    #simpleCrossWalk['0']='SNEC'
    simpleCrossWalk['StreetNamePreDirectional']='SNPDC'
    #since codes aren't provided for every entry, its easier to just treat this all as the same thing
    simpleCrossWalk['StreetNamePostDirectional']='SNSDC'
    
    
    #now bridge this to mpStaging  - ignore the print statements, my todo lists are very informal when i'm working my own code in a vacuum - but its a real thing i/someone should get to eventually
    import mpStaging
    
    #i know the parser will work on this

    
    #no harm in following someone else's lead initially, but usaddress's tuple pairs really bother me - so i'm converting
    #a dict has unquie keys, but it should work for this example at least.  a more reliable substitute will eventually be required.
    
    def usAdr2Dict(inTuple):
        outDict = {}
        for item in inTuple:
            outDict[item[1]]=item[0]
        return outDict
    
    adrA_dict = usAdr2Dict(standardizer.standardize(adrStrA))

    
    """
    NOW we can use this:
    from my notes/exsting code in mpStaging
    fidOrder = ['OSN','ZIP','SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    """
    #mpStaging.fidOrder
    
    #mpStaging expects ordered lists/tuples, so I'll oblige
    
    fidAdrA = [x for x in mpStaging.fidOrder] #i think this is not needed, could be removed?
    
    #I goofed up my crosswalk and need to reverse it - normally I'd do it right, but showing my work
    #https://stackoverflow.com/questions/483666/reverse-invert-a-dictionary-mapping
    
    simpleCrossWalk2 = {v: k for k, v in simpleCrossWalk.items()}
    
    #and THIS is why you should pick a schema and stick with it, because crosswalks get old.  20+ years of legacy code and competing standards is colliding here
    stanCode2amgScore = {'StreetNamePreDirectional':'DIR',
                         'StreetNamePostDirectional':'DIR',
                         'StreetNamePostType':'TYPE',
                         'StreetNamePreType':'TYPE'}
    
    
    #this is... embarasingly bad code.  there are smarter ways to structure this.  this is a perfect example of a functional but terrible first draft that techically works but is impossible to maintain
    #this is bad in part because usaddress and amgScore are not originally deisgned to work together so bridging them takes some nuance i don't have time for right now
    fidA = []
    for col in mpStaging.fidOrder:    
        if col in ('OSN','ZIP'):
            fidA.append(adrA_dict[simpleCrossWalk2[col]])
            
        elif col in simpleCrossWalk2.keys():
            #this is... really bad form.  don't ever do this for real.
            try:
                #this is like a master class in bad code, really.  sometimes "clever" is a bad thing            
                fidA.append(stanCode[stanCode2amgScore[simpleCrossWalk2[col]]][adrA_dict[simpleCrossWalk2[col]]])
            except:
                fidA.append(0) #be sure to hard code to int
        else:
            #hardcode SNEC...
            fidA.append(0)
    return fidA
    

def fidPairMerge(fidA, fidB):
    from itertools import chain
    fidList = [y for y in chain.from_iterable([x for x in zip(fidA,fidB)])]
    return fidList
    

#ALL THAT to reuse this function
if __name__== '__main__':
    adrStrA = '101 VineBridge street SW apartment 1 anytown md 99999'
    adrStrB = '101 VineBri st SW apt 1 anytown MD 99999'
    
    fidA = format4FidCompare(adrStrA)
    fidB = format4FidCompare(adrStrB)
    
    #someone else wrote the input format for fidComparator, all I did was make a faithful python version
    #https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    from itertools import chain
    fidList = [y for y in chain.from_iterable([x for x in zip(fidA,fidB)])]
    
    streetNameMatchResults = amgScore.fidComparator(*fidList)
    print("fidscore = ", streetNameMatchResults)
    
    
    
    #for item in data:
    #    print(standardizer.standardize(item))
        
    print('\n\nDone!') 