# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:09:45 2020

@author: watso330
"""

"""
source file at D:\maf_tally\FID_COMPARE\AMG_API\AMGScore.java
"""

import sys
sys.path.append(r'D:\maf_tally\pyLib\jellyfish-0.5.1')
import jellyfish

def pyNvl(var, val):
  if var is None:
    return val
  return var

#global variable used for... something:
#mfObjValue == mfObj.setFuncVal/getFuncVal
mfObj_FuncVal = 0
# try an alteration where you keep track of every instance it is set and if ANY = -1. then fail the final value...
#raise('you need to figure out how to handle mfObj.setFuncVal(-1); right!!!')
mfObj_FuncVal_Dict = {}
mfObj_MissFlag_Dict = {}

mfObj_MissFlag = ' '
# BOTH MISSING
dirBW = 0
typeBW = 110
nameBW = -900
zipBW = 0
extBW = 0

# MISSING
dirMW = -50
typeMW = 0
nameMW = -900
zipMW = -600
extMW = -100

#AGREE
dirAW = 50
typeAW = 0
nameAW = 900
zipAW = 200
extAW = 100

#DISAGREE
dirDW = -600
typeDW = -300
nameDW = -3850
zipDW = -600
extDW = -100

#Cutoffs for Agree vs. Disagree weights  
hiNameCutoff= 90
loNameCutoff= 60
dirCutoff= 50
zipCutoff= 0
typeCutoff= 70

defTypeWt= 370
defPreTypeWt= 175

#Comparator Cutoffs
minCompScore = 94

#Arrays for stringComparator

#notes for standardizer values...
dirCodes = {}
dirCodes['N']=1
dirCodes['S']=2
dirCodes['E']=3
dirCodes['W']=4
dirCodes['NE']=5
dirCodes['NW']=6
dirCodes['SE']=7
dirCodes['SW']=8

#This is used by dirComparator...
def dirScore(dir1, dir2):
    score = 0
    loDir = 0
    hiDir = 0
    
    if dir1 == dir2:
        score = 100
        return score
    elif dir1 < dir2:
        loDir = dir1
        hiDir = dir2
    else:
        loDir = dir2
        hiDir = dir1
    # N, S, E, and W are 1-4 OR NE, NW, SE, SW, are 5-8 , see dirCodes
    if((loDir <= 4 and hiDir <= 4) or (loDir > 4 and hiDir > 4)):
        score = 0
        return score
    #print ('dirScore here!0')
    if ((loDir == 1 and (hiDir == 5 or hiDir == 6)) or
		   (loDir == 2 and (hiDir == 7 or hiDir == 8)) or
		   (loDir == 3 and (hiDir == 5 or hiDir == 7)) or
		   (loDir == 4 and (hiDir == 6 or hiDir == 8))):
        score = 50
        return score
    else:
        #print ('dirScore here!1')
        #print (loDir, hiDir)
        #new logic not present in original AMGScore:
        score = 0
        return score


"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def dirComparator(InPreDir, MatchPreDir, InSufDir, MatchSufDir):
    score = 0
    p1 = InPreDir
    p2 = MatchPreDir
    s1 = InSufDir
    s2 = MatchSufDir
    mfObj_MissFlag = ' '
    
    if (p1 == 0 and p2 == 0 and s1 == 0 and s2 == 0):
        mfObj_MissFlag = 'B'
        mfObj_MissFlag_Dict['dirComparator']='B'
        score = 100
        return score
    
    # Both prefix directions present
    if (p1 != 0 and p2 != 0):
        #print('here!')
        score = dirScore(p1, p2)
        #print(score)
        if s1 != s2:
            if score > 5:
                score = score - 5
        return score
    
    # Both suffix directions present
    elif (s1 != 0 and s2 != 0):
        score = dirScore(s1, s2)
        if p1 != p2:
            if score > 5:
                score = score - 5
        return score

    # One prefix direction present
    elif (p1 != 0 and p2 == 0):
        if s2 != 0:
            score = dirScore(p1, s2)
        else:
            score = 0
            mfObj_MissFlag = 'M'
            mfObj_MissFlag_Dict['dirComparator']='M'
    elif (p2 != 0 and p1 == 0):
        if s1 != 0:
            score = dirScore(p2, s1)
        else:
            score = 0
            mfObj_MissFlag = 'M'
            mfObj_MissFlag_Dict['dirComparator']='M'
    
    # One suffix direction present, no transposition
    elif (s1 != 0 or s2 != 0):
        score = 0
        mfObj_MissFlag = 'M'
        mfObj_MissFlag_Dict['dirComparator']='M'
    return score
        
"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def scoreDirection(dirScore):
    #global mfObj_Value
    #global mfObj_MissFlag
    
    dirWt = 0
    if mfObj_MissFlag == 'M' or mfObj_MissFlag_Dict.get('dirComparator', ' ') == 'M':
        dirWt = dirMW
        dirScore = 1
    elif mfObj_MissFlag == 'B' or mfObj_MissFlag_Dict.get('dirComparator', ' ') == 'B':
        dirWt = dirBW
        dirScore = 2
    elif dirScore > dirCutoff:
        dirWt = ((dirScore * dirAW) / 100.0 + 0.5)
    else:
        dirWt = dirDW
        mfObj_FuncVal = -1
        mfObj_FuncVal_Dict['scoreDirection']=-1
        #print('setting dir FuncVal')
    
    return dirWt


def typeScore(type1, type2):
    hold = 0
    sameType = 0
    
    #Quick check for equality
    if type1 == type2:
        sameType = 100
        return sameType
    
    # Make type1 be the lesser numerical value, to make checking easier 
    if type1 > type2:
        hold = type1
        type1 = type2
        type2 = hold
    
    # State Routes
    if (type1 >= 257 and type1 <= 259 and type2 >= 257 and type2 <= 259):
        sameType = 90
    # County Routes 
    elif (type1 >= 67 and type1 <= 70 and type2 >= 67 and type2 <= 70):
        sameType = 90
    # US Routes
    elif (type1 == 282 and type2 == 283):
        sameType = 90
    #*** Avenida vs. Avenue
    elif (type1 == 18 and type2 == 19):
        sameType = 90
    #cou hwy
    else:
        if ((type1 == 67 and type2 == 122) or (type1 == 122 and type2 == 257) or (type1 == 122 and type2 == 272) or (type1 == 122 and type2 == 282) or (type1 == 122 and type2 == 258) or (type1 == 122 and type2 == 259)):
            sameType = 80    
        else: #/* cou rte */
            if ((type1 == 70 and type2 == 227) or (type1 == 227 and type2 == 259) or (type1 == 227 and type2 == 283)):
                #/* *** Route to state rte, county rte, etc.  */
                sameType = 80
    return sameType
        
    

"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def typeComparator(InPreType, MatchPreType, InSufType, MatchSufType):
    try:
        #typeScore = 0
        preType1 = InPreType
        preType2 = MatchPreType
        sufType1 = InSufType
        sufType2 = MatchSufType
        
        #If both suffix types present, score'em. 
        #replace assignment of typeScore variable with "score"
        if (sufType1 != 0 and sufType2 != 0):
            score = typeScore(sufType1,sufType2)
            return score
    
        #If suffix type 1 present and suffix type 2 blank, assign
        #as 'missing', unless a transposition, in which case give 80.
        elif (sufType1 != 0 and sufType2 == 0):
            score = typeScore(preType2,sufType1)
            if score == 0:
                mfObj_MissFlag = 'M'
                mfObj_MissFlag_Dict['typeComparator']='M'
                #print('setting M flag A...')
            else:
                score = score - 20 #Transposition
        #If suffix type 2 present and suffix type 1 blank, assign
        #as 'missing', unless a transposition, in which case give 80.     
        elif (sufType2 != 0 and sufType1 == 0):
            score = typeScore(preType1,sufType2)
            if score == 0:
                mfObj_MissFlag = 'M'
                mfObj_MissFlag_Dict['typeComparator']='M'
                #print('setting M flag B...')
            else:
                score = score - 20 #Transposition
        #If suffix type 1 and suffix type 2 blank, check prefixes. 
        elif (sufType1 == 0 and sufType2 == 0):
            if (preType1 != 0 or preType2 != 0):
                score = typeScore(preType1,preType2)
        #All prefix and suffix types are blank: 
#i think this is eliminated by following code...        
#    elif sufType1 == 0 and sufType2 == 0 and preType1 != 0 and preType2 != 0:
#            score = 100
#            mfObj_MissFlag = 'B'
#            mfObj_MissFlag_Dict['typeComparator']='B'
#            print('setting B flag A...')
#        else:
#            print('should never get here...')
#            raise()
        if sufType1 == 0 and sufType2 == 0 and preType1 == 0 and preType2 == 0:
            score = 100
            mfObj_MissFlag = 'B'
            mfObj_MissFlag_Dict['typeComparator']='B'
            #print('setting B flag B B...')
            #print('All prefix and suffix types are blank')
        return score
    except:
        print('dealing with an error using inputs:')
        print(InPreType, MatchPreType, InSufType, MatchSufType)
        #raise()
    
"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def scoreType(inTypeScore, inPreType, MatchPreType):
    typeWt = 0
    #One type Missing
    if mfObj_MissFlag == 'M' or mfObj_MissFlag_Dict.get('typeComparator', ' ')  == 'M':
        typeWt = typeMW
        inTypeScore = 1
    # Both types missing
    elif mfObj_MissFlag == 'B' or mfObj_MissFlag_Dict.get('typeComparator', ' ') == 'B':
        typeWt = typeBW
        typeScore = 2
    # Types Disagree
    elif inTypeScore < typeCutoff:
        typeWt = typeDW
    # Types Agree
    else:
        typeWt = defTypeWt
        if inPreType != 0:
            if defPreTypeWt < typeWt:
               typeWt = defPreTypeWt
        if MatchPreType != 0:
            if (defPreTypeWt < typeWt):
                typeWt = defPreTypeWt
        # If inTypeScore was less than 100 decrease typeWt accordingly
        typeRatio = (inTypeScore / 100.0)
        typeWt = int(typeWt * typeRatio + 0.5)
    return typeWt

"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def extComparator(InExt, MatchExt):
    ext1 = InExt
    ext2 = MatchExt
    score = 0
    mfObj_MissFlag = ' '
    # Neither has extension
    if (ext1 == 0 and ext2 == 0):
        mfObj_MissFlag = 'B'
        mfObj_MissFlag_Dict['extComparator']='B'
        score = 2
        return score
    # Both extensions present
    if (ext1 > 0 and ext2 > 0):
        if (ext1 == ext2):
            score == 100
        else:
            score = 0
        return score
    # One extension present
    mfObj_MissFlag = 'M'
    mfObj_MissFlag_Dict['extComparator']='M'
    score = 1
    return score

"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def scoreExtension(extScore):
    if mfObj_MissFlag == 'M' or mfObj_MissFlag_Dict.get('extComparator', ' ') == 'M':
        extWt = extMW
        extScore = 1
    elif mfObj_MissFlag == 'B' or mfObj_MissFlag_Dict.get('extComparator', ' ') == 'B':
        extWt = extBW
        extScore = 2
    elif (extScore == 0):
        extWt = extDW
    else:
        extWt = extAW
    return extWt

"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def zipComparator(zip1, zip2):
    zip1 = str(zip1)
    zip2 = str(zip2)
    score = 0

    mfObj_MissFlag = ' '
    # Check if both zips have NULL values
    if zip1 is None and zip2 is None:
        score = 100
        mfObj_MissFlag = 'B'
        mfObj_MissFlag_Dict['zipComparator']='B'
        return score
    # Check if 1 zip has NULL values
    if zip1 is None or zip2 is None:
        score = 0
        mfObj_MissFlag = 'M'
        mfObj_MissFlag_Dict['zipComparator']='M'
        return score
    # Convert input strings to int
    intZip1 = int(zip1)
    intZip2 = int(zip2)
    # Check for both zips = 00000
    if (intZip1 == 0 and intZip2 == 0):
        score = 100
        mfObj_MissFlag = 'B'
        mfObj_MissFlag_Dict['zipComparator']='B'
        return score
    
    if zip1 == zip2:
        score = 100
        return score
    # Check for one zip = 00000
    if intZip1 == 0 or intZip2 == 0:
        score = 0
        mfObj_MissFlag = 'M'
        mfObj_MissFlag_Dict['zipComparator']='M'
        return score

    # Guard against substring errors if either zip < 5 in length   
    if len(str(zip1)) < 5 or len(str(zip2)) < 5:
        score = 0
        return score
    
    # Check 3-digit zip
    if zip1[:3] != zip2[:3]:
        score = 0
        return score
    
    # At this point we have a 3-digit match
    # Check for transposition of last 2 digits
    bufZip2 = zip2[3:5]
    #https://stackoverflow.com/questions/931092/reverse-a-string-in-python
    if zip1[3:5]== bufZip2[::-1]:
        score = 65
    # check first 4 digit match
    elif zip1[:4]==zip2[:4]:
        score = 65
    else:
        #score for a 3-digit match
        score = 50
    return score
    

"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def scoreZip(zipScore):
    # One zip missing
    if mfObj_MissFlag == 'M' or mfObj_MissFlag_Dict.get('zipComparator', ' ') == 'M':
        zipWt = zipMW
        zipScore = 1
    # Both zips missing
    elif mfObj_MissFlag == 'B' or mfObj_MissFlag_Dict.get('zipComparator', ' ') == 'B':
        zipWt = zipBW
        zipScore = 2
    elif (zipScore > zipCutoff):
        zipRatio = float(zipScore / 100.0)
        zipWt = int(zipDW + zipRatio * (zipAW - zipDW) + 0.5)
    else:
        zipWt = zipDW
        # Set funcVal flag to set overallScore to 0 for these conditions
        mfObj_FuncVal = -1
        mfObj_FuncVal_Dict['scoreZip']=-1
        
    return zipWt

def stringComparator(inString1, inString2):
    #just use a pre-built jaro-winkler string comparator from jellyfish
    #not really worth porting over something that complex when other versions e3xist
    #consider using febrl_methods.py as well...
    return jellyfish.jaro_winkler(inString1, inString2)
    
"""
mfObj_FuncVal = 0
mfObj_MissFlag = ' '
"""
def scoreName(compScore):
    nameRatio = compScore
    nameWt = int(nameDW + nameRatio * (nameAW - nameDW) + 0.5)
    nameScore = int((nameRatio * 10000.0) + 0.5)
    #Do not allow name scores less than .94
    if nameRatio < (minCompScore/100.0):
        mfObj_FuncVal = -1
        mfObj_FuncVal_Dict['scoreName']=-1
    return nameWt
    

def fidComparator(inName,matchName,inZip,matchZip,inPreType,matchPreType,inSufType,matchSufType,inExtType,matchExtType,inPreDir,matchPreDir,inSufDir,matchSufDir):
    overallScore = 0
    global mfObj_FuncVal
    mfObj_FuncVal = 0
    global mfObj_FuncVal_Dict
    mfObj_FuncVal_Dict = {}
    global mfObj_MissFlag
    mfObj_MissFlag = ' '
    global mfObj_MissFlag_Dict
    mfObj_MissFlag_Dict = {}
    #avoid overwriting function names, changed dirScore to inDirScore...
    inDirScore = dirComparator(inPreDir,matchPreDir,inSufDir,matchSufDir)
    dirWeight = scoreDirection(inDirScore)
    typeScore = typeComparator(inPreType,matchPreType,inSufType,matchSufType)
    typeWeight = scoreType(typeScore,inPreType,matchPreType)
    extScore = extComparator(inExtType, matchExtType)
    extWeight = scoreExtension(extScore)
    zipScore = zipComparator(inZip,matchZip)
    zipWeight = scoreZip(zipScore)
    compScore = stringComparator(inName,matchName)
    nameWeight = scoreName(compScore)
    
    if mfObj_FuncVal == -1 or -1 in mfObj_FuncVal_Dict.values():
        overallScore = 0
    else:
        overallScore = nameWeight + dirWeight + typeWeight + zipWeight + extWeight #consider "dumb fix" to prefent ext score overweighting..
    mfObj_FuncVal = 0
    return int(overallScore)

def replaceSpanishChar(sBuffer):
    sBuffer = str(sBuffer)
    chrMap = {}
    chrMap[chr(193)]='A'
    chrMap[chr(225)]='a'
    chrMap[chr(201)]='E'
    chrMap[chr(233)]='e'
    chrMap[chr(205)]='I'
    chrMap[chr(237)]='i'
    chrMap[chr(209)]='N'
    chrMap[chr(241)]='n'
    chrMap[chr(211)]='O'
    chrMap[chr(243)]='o'
    chrMap[chr(218)]='U'
    chrMap[chr(250)]='u'
    chrMap[chr(220)]='U'
    chrMap[chr(252)]='u'
    chrMap[chr(305)]='A'
    chrMap[chr(229)]='a'
    
    outStr = ''.join([chrMap[x] if x in chrMap.keys() else x for x in sBuffer])
    return outStr

#Consider doing this later, not sure its worth it yet...    
def hnScore(inHouseNumFrom, inHouseNumSepFrom, inHouseNumExtFrom, inHouseNumTo, inHouseNumSepTo, inHouseNumExtTo):
    #force inputs as strings
    inHouseNumFrom=str(inHouseNumFrom)
    inHouseNumSepFrom=str(inHouseNumSepFrom)
    inHouseNumExtFrom=str(inHouseNumExtFrom)
    inHouseNumTo=str(inHouseNumTo)
    inHouseNumSepTo=str(inHouseNumSepTo)
    inHouseNumExtTo=str(inHouseNumExtTo)
    
    retScore = 0
    hn1From = 0
    hn2From = 0
    hn1To = 0
    hn2To = 0
    wholeHnFrom = 0
    wholeHnTo = 0
    
    # Trim incoming data 
    houseNumFrom = inHouseNumFrom.strip().upper()
    houseNumTo = inHouseNumTo.strip().upper()
    houseNumSepFrom = inHouseNumSepFrom.strip().upper()
    houseNumSepTo = inHouseNumSepTo.strip().upper()
    houseNumExtFrom = inHouseNumExtFrom.strip().upper()
    houseNumExtTo = inHouseNumExtTo.strip().upper()

    # Separators must match or one should be a hyphen and the other null ??
    if (not(houseNumSepFrom == houseNumSepTo or (houseNumSepFrom == "-" and len(houseNumSepTo) == 0) or (houseNumSepTo == "-" and len(houseNumSepFrom) == 0))):
        return 0 #retScore

    # Alphanum comparison of HN and HN2: if match get out
    if houseNumFrom==houseNumTo:
        if houseNumExtFrom==houseNumExtTo:
            return 10

    # To continue HN1 must be integer for both, otherwise no match
    try:
        hn1From = int(houseNumFrom)
        hn1To = int(houseNumTo)
    except: 
        return retScore # no need to compare further
    
    # Alternative is to parse only if houseNumExt_from.matches("\\s*\\d+\\s*")
    # Parse HN2 as integers
    try:
        hn2From = int(houseNumExtFrom)
    except:
        # Remains 0 if failure
        pass
    
    try:
        hn2To = int(houseNumExtTo)
    except:
        # Remains 0 if failure
        pass

        
    # Integer equality of both HN1 and HN2
    if (hn1From == hn1To and hn2From == hn2To):
        retScore = 9
    else:
        # Integer equality of HN1 + HN2 as strings
        try:
            wholeHnFrom = houseNumFrom + houseNumExtFrom
            wholeHnTo = houseNumTo + houseNumExtTo
        except:
            pass

    if (hn2From > 0 and wholeHnFrom == hn1To) or (hn2To > 0 and wholeHnTo == hn1From):
        retScore = 8
    elif (hn2From != 0 and hn2To == 0 and houseNumFrom+houseNumExtFrom==hn1To) or (hn2To != 0 and hn2From == 0 and houseNumTo==houseNumExtTo == hn1From):
        retScore = 7
    elif hn1From == hn1To:
        retScore = 5
        

    return retScore
   
    
if __name__=='__main__':
    import ast 
    from itertools import chain
    #https://www.geeksforgeeks.org/python-convert-a-string-representation-of-list-into-list/
    #string literal
    #put address example here...
    iniList = "((2, 710599669379, None, '141', None, None, None, '141', 0, 263, 0, 4, 0, '2ND', ' ', 'W 2nd St', None, None, None, '57580', '57580', '141', ' '), (788, 710599670174, None, '141', None, None, None, '141', 0, 263, 0, 0, 0, 'ADAMS', ' ', 'Adams St', None, None, None, '57580', '57580', '141', ' '))"
    pair = ast.literal_eval(iniList)
    #merge up "pair" with unduplicationTesting.py logic...
    
    fidOrder = ['OSN','ZIP','SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    fidOrder = ['MSN','ZIP','SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    print('This function uses either MSN or OSN, must be changed manually for inputs...')
    print('\t',str(fidOrder),'\n\n')
    numConvert = ['SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    headerDict ={0: 'INPUTID',
                 'INPUTID': 0,
                 1: 'CUSTID',
                 'CUSTID': 1,
                 2: 'HNPRE',
                 'HNPRE': 2,
                 3: 'HN1',
                 'HN1': 3,
                 4: 'HNSEP',
                 'HNSEP': 4,
                 5: 'HN2',
                 'HN2': 5,
                 6: 'HNSUF',
                 'HNSUF': 6,
                 7: 'HN',
                 'HN': 7,
                 8: 'SNPTC',
                 'SNPTC': 8,
                 9: 'SNSTC',
                 'SNSTC': 9,
                 10: 'SNEC',
                 'SNEC': 10,
                 11: 'SNPDC',
                 'SNPDC': 11,
                 12: 'SNSDC',
                 'SNSDC': 12,
                 13: 'MSN',
                 'MSN': 13,
                 14: 'OSN',
                 'OSN': 14,
                 15: 'STREETNAME',
                 'STREETNAME': 15,
                 16: 'WSDESC1',
                 'WSDESC1': 16,
                 17: 'WSID1',
                 'WSID1': 17,
                 18: 'WS',
                 'WS': 18,
                 19: 'ZIP',
                 'ZIP': 19,
                 20: 'BLOCK1',
                 'BLOCK1': 20,
                 21: 'BLOCK2',
                 'BLOCK2': 21,
                 22: 'BLOCK3',
                 'BLOCK3': 22}
    
    fidDict = {}
    for e, i in enumerate(fidOrder):
        fidDict[i]=e
    
  
    
    adrA, adrB = pair
    
    hnA = adrA[2]
    hnB = adrB[2]
    
    idA = adrA[0]
    idB = adrB[0]
    
    compA = [adrA[headerDict[x]] for x in fidOrder]
    compB = [adrB[headerDict[x]] for x in fidOrder]
    #convert codes to integers...
    compA = [int(x) if ei>1 else x for ei, x in enumerate(compA)]
    compB = [int(x) if ei>1 else x for ei, x in enumerate(compB)]    
    
    fidList = list(chain.from_iterable(zip(compA,compB)))
    #fidScore = amgScore.fidComparator(*fidList)
    
    osn1,osn2,zip1,zip2,snptc1,snptc2,snstc1,snstc2,snec1,snec2,snpdc1,snpdc2,snsdc1,snsdc2 = fidList
    
    inDirScore = dirComparator(snpdc1,snpdc2,snsdc1,snsdc2)
    dirWeight = scoreDirection(inDirScore)
    
    t_TypeScore = typeComparator(snptc1,snptc2,snstc1,snstc2)
    typeWeight = scoreType(t_TypeScore,snptc1,snptc2)
    
    extScore = extComparator(snec1, snec2)
    extWeight = scoreExtension(extScore)
    
    zipScore = zipComparator(zip1,zip2)
    zipWeight = scoreZip(zipScore)
    
    compScore = stringComparator(osn1,osn2)
    nameWeight = scoreName(compScore)    
    
    print(' '.join([str(pyNvl(x,' ')) for x in adrA]))
    print(' '.join([str(pyNvl(x,' ')) for x in adrB]))
    print('')
    
    print('OVERALL', fidComparator(osn1,osn2,zip1,zip2,snptc1,snptc2,snstc1,snstc2,snec1,snec2,snpdc1,snpdc2,snsdc1,snsdc2))
    print('\tOSN1:',osn1)
    print('\tOSN1:',osn2)
    print('NAME_WT',nameWeight)
    print('TYPE_WT',typeWeight)
    print('DIR_WT',dirWeight)
    print('ZIP_WT',zipWeight)
    print('EXT_WT',extWeight)
    print('COMP_SCORE',compScore)
    print('TYPE_SCORE',t_TypeScore)
    print('DIR_SCORE',inDirScore)
    print('ZIP_SCORE',zipScore)
    print('EXT_SCORE',extScore)
    
#----------------------------------------------
#proposed/experiemntal enhancements....
    


    
#look into letter swaps, at some point...  also/or just spell checker functions?
   
"""
  private static final int [][] sp		= {
    {'A','E'},{'A','I'},{'A','O'},{'A','U'},{'B','V'},{'E','I'},{'E','O'},
    {'E','U'},{'I','O'},{'I','U'},{'O','U'},{'I','Y'},{'E','Y'},{'C','G'},
    {'E','F'},{'W','U'},{'W','V'},{'X','K'},{'S','Z'},{'X','S'},{'Q','C'},
    {'U','V'},{'M','N'},{'L','I'},{'Q','O'},{'P','R'},{'I','J'},{'2','Z'},
    {'5','S'},{'8','B'},{'1','I'},{'1','L'},{'0','O'},{'0','Q'},{'C','K'},
    {'G','J'},{'E',' '},{'Y',' '},{'S',' '}};
"""