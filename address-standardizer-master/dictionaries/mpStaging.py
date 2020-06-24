# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 08:47:58 2020

This is a data staging script meant to be run for each ZIP 3, prior to running MAFPLUS_match_merge

@author: watso330
"""

import csv, string, amgScore
from itertools import chain
from collections import OrderedDict
from copy import deepcopy

#pre-staged data
dsfDataDir = r'C:\A_LocalWork\DataStore\Frames\RawDataLocal\UNUSED_DSF'
lehdDataDir = r'C:\A_LocalWork\DataStore\Frames\RawDataLocal\{T.B.D.}'

wsTerms = set()
puntTerms = set()

hnTerms = set()
hnPuntTerms = set()


fidOrder = ['OSN','ZIP','SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
hnSimple = ['HN']
wsSimple = ['WS']
#HNPRE|HN1|HNSEP|HN2|HNSUF|HN
hnAmgOrder = ['HN1','HNSEP','HN2']

hnFull = ['HN1', 'HNSEP', 'HN2']
hnFull2 = ['HNPRE', 'HN1', 'HNSEP', 'HN2', 'HNSUF']
wsFull = ['WSDESC1', 'WSID1']
numConvert = ['SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
headerIndex = {0: 'INPUTID',
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

#def matchOrigCheck(inOsn, inMsn, cutOff=0):
def matchOrigCheck(inOsn, inMsn, cutOff=0):
    """
    f idOrder = ['OSN','ZIP','SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    f idOrder = ['OSN','ZIP','SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    
    compScore = stringComparator(osn1,osn2)
    nameWeight = scoreName(compScore) 
scoreName(compScore)    
    """
    #amgScore.stringComparator(inString1, inString2)
    #nameList = ['OSN','MSN']
    
    inOsn = inOsn.strip()
    inMsn = inMsn.strip()
    

    
    
    if inOsn == 'None':
        inOsn = ''
    if inMsn == 'None':
        inMsn = ''
    
    if len(inOsn)==0 and len(inMsn)>0:
        goodCol = 'MSN'
    elif len(inOsn)>0 and len(inMsn)==0:
        goodCol = 'OSN'
    elif inOsn==inMsn:
        goodCol = 'OSN'
    elif inOsn!=inMsn:
        compScore = amgScore.stringComparator(inOsn, inMsn)
        nameScore = amgScore.scoreName(compScore)
        lenMsn = len(inMsn)
        lenOsn = len(inOsn)
        if nameScore> cutOff:
            if lenMsn>lenOsn:
                goodCol = 'MSN'
            else:
                goodCol = 'OSN'
        else:
            goodCol = 'OSN'
    else:
        #when all other logic fails...
        goodCol = 'OSN'
    
    lFidOrder = [goodCol,'ZIP','SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    return lFidOrder
        
    
    
    


#common functions 

##figure out stancode lookups...
#import os, json
#metaDir = r'V:\Data\metadata'
#stanCodePath = os.path.join(metaDir,'mafdata_StanCode.csv')
#cenPreTypPath = os.path.join(metaDir, 'cenPreTyp.json')
#cenDirectionPath = os.path.join(metaDir, 'uspsDirections.json')
#cenStrSufPath = os.path.join(metaDir, 'uspsStrSufAbbr.json')
#
#
#with open() as temp:
#    pass

#https://stackoverflow.com/questions/4368423/symmetric-dictionary-where-dab-dba


def loadPipeCsv(inPath, filterCol = None, filterValue = None):
    csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
    print('loading CSV data: {}'.format(inPath))
    localData = []
    with open(inPath, "r") as csvfile:
        for row in csv.DictReader(csvfile, dialect='piper'):
            if 'lclHeader' not in locals():
                lclHeader = [x for x in row.keys()]
            if not filterCol and not filterValue:
                #if both values are default, None, then logic returned == True, execute following:
                localData.append([x.strip() for x in row.values()])
            else:
                #else, it is assumed that a valid column and value exist...
                if row[filterCol]==filterValue:
                    localData.append([x.strip() for x in row.values()])
                else:
                    pass
                
    try:
        return lclHeader, localData
    except:
        return [],[]
    
##common functions 
#def loadPipeCsv_ByteForm(inPath, filterCol = None, filterValue = None):
#    csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
#    print('loading CSV data: {}'.format(inPath))
#    localData = []
#    with open(inPath, "rb") as csvfile:
#        for row in csv.DictReader(csvfile, dialect='piper'):
#            if 'lclHeader' not in locals():
#                lclHeader = [x for x in row.keys()]
#            if not filterCol and not filterValue:
#                #if both values are default, None, then logic returned == True, execute following:
#                localData.append([x.strip() for x in row.values()])
#            else:
#                #else, it is assumed that a valid column and value exist...
#                if row[filterCol]==filterValue:
#                    localData.append([x.strip() for x in row.values()])
#                else:
#                    pass
#                
#    try:
#        return lclHeader, localData
#    except:
#        return [],[]    

def pyNvl(var, val):
  if var is None:
    return val
  return var

#basic matching function

def amgHnMatch(adrA,adrB):
    hnA = [pyNvl(adrA[headerIndex[x]], ' ') for x in hnFull] # [pyNvl(x,' ') for x in hnFull]
    hnB = [pyNvl(adrB[headerIndex[x]], ' ') for x in hnFull]
    hnArgs = []
    hnArgs.extend(hnA)
    hnArgs.extend(hnB)
    hnMatch = amgScore.hnScore(*hnArgs)
    return hnMatch

def amgFidCompare(adrA, adrB, cutOff=800):
    #def matchOrigCheck(inOsn, inMsn, cutOff=0):
    #adrA[headerIndex['OSN']] adrA[headerIndex['MSN']]
    locFidOrderA = matchOrigCheck(adrA[headerIndex['OSN']], adrA[headerIndex['MSN']], cutOff=0)
    locFidOrderB = matchOrigCheck(adrB[headerIndex['OSN']], adrB[headerIndex['MSN']], cutOff=0)
    compA = [adrA[headerIndex[x]] for x in locFidOrderA]
    compB = [adrB[headerIndex[x]] for x in locFidOrderB]
    #convert codes to integers...
    compA = [int(x) if ei>1 else x for ei, x in enumerate(compA)]
    compB = [int(x) if ei>1 else x for ei, x in enumerate(compB)]
    #STREET NAME MATCHING
    if compA == compB:
        #print('exact match, moving on...')
        nameMatch = True
        exactMatch = True
        fidList = list(chain.from_iterable(zip(compA,compB)))
        fidScore = amgScore.fidComparator(*fidList)
    else:
        fidList = list(chain.from_iterable(zip(compA,compB)))
        fidScore = amgScore.fidComparator(*fidList)
        if fidScore >= cutOff:
            nameMatch = True
            exactMatch = False        
    if not nameMatch:
        #exit iteration early
        return (False, False, fidScore)   

    if nameMatch:
        return (True, exactMatch, fidScore)
    else:
        print('unexpected matching criteria met, failing gracelessly')
        raise('this is a debug error, check your standard-out')

simpleAdr = ['HN','STREETNAME','WS','ZIP']

def renderAddress(inData, inVal, inVar='INPUTID', stringForm = False):
    outRow = []
    for row in inData:
        if str(row[headerIndex[inVar]])==str(inVal):
            #print('found it!')
            for adrPart in simpleAdr:
                outRow.append(pyNvl(row[headerIndex[adrPart]],' '))
            break
    if stringForm:
        return ' '.join(outRow)
    else:
        return outRow
    

def multiMatch1(adrA, adrB):
    adrA = [pyNvl(x, ' ') for x in adrA]
    adrB = [pyNvl(x, ' ') for x in adrB]
    hnMatchSimple = False
    nameMatchFid = False
    wsMatchSimple = False
    
    hnMatchAmg = False
    hnPreMatch = False
    hnSufMatch = False
    
    hnPreMatch = False
    hnSufMatch = False
    hnExactMatch = False
    
    hnSufwsMatch = False
    wsid1Match = False
    
    #compund Matches
    bsaMatch = False
    fullExactMatch = False
    fullEquivMatch = False


    #determine HN exact matches
    hnAfull = [adrA[headerIndex[x]] for x in hnFull2 ]
    hnBfull = [adrB[headerIndex[x]] for x in hnFull2 ]
    
    if hnAfull == hnBfull:
        hnExactMatch = True

    #determine simple/simpleMatch HN match:
    hnA = [adrA[headerIndex[x]] for x in hnSimple]
    hnB = [adrB[headerIndex[x]] for x in hnSimple]    
    if hnA == hnB:
        hnMatchSimple = True

    #determine simple/simpleMatch WS match:
    wsA = [pyNvl(adrA[headerIndex[x]], ' ') for x in wsSimple][0].split()
    wsB = [pyNvl(adrB[headerIndex[x]], ' ') for x in wsSimple][0].split()
    #simple extract of last number...
    if len(wsA)>0:
        wsA = wsA[-1]
    else:
        wsA = ''

    if len(wsB)>0:
        wsB = wsB[-1]
    else:
        wsB = '' 
    if wsA == wsB:
        wsMatchSimple = True    
       
    #determine classic/Fid name match
    #STREET NAME MATCHING
    locFidOrderA = matchOrigCheck(adrA[headerIndex['OSN']], adrA[headerIndex['MSN']], cutOff=0)
    locFidOrderB = matchOrigCheck(adrB[headerIndex['OSN']], adrB[headerIndex['MSN']], cutOff=0)
    
    compA = [adrA[headerIndex[x]] for x in locFidOrderA]
    compB = [adrB[headerIndex[x]] for x in locFidOrderB]
    #convert codes to integers...
    compA = [int(x) if ei>1 else x for ei, x in enumerate(compA)]
    compB = [int(x) if ei>1 else x for ei, x in enumerate(compB)]
    
    if compA == compB:
        #print('exact match, moving on...')
        nameMatchFid = True
        exactMatch = True
        fidList = list(chain.from_iterable(zip(compA,compB)))
        fidScore = amgScore.fidComparator(*fidList)
    else:
        fidList = list(chain.from_iterable(zip(compA,compB)))
        fidScore = amgScore.fidComparator(*fidList)
        if fidScore >= 800:
            nameMatchFid = True
        exactMatch = False
    
    #determine hn amg match
    hnAmgA = [adrA[headerIndex[x]] for x in hnAmgOrder]
    hnAmgB = [adrB[headerIndex[x]] for x in hnAmgOrder]
    hnAmgList = deepcopy(hnAmgA)
    hnAmgList.extend(hnAmgB)
    hnAmgResult = amgScore.hnScore(*hnAmgList)
    if hnAmgResult> 0:
        hnMatchAmg = True

    #Determine straight WSID1 match:
    if str(adrA[headerIndex['WSID1']]).upper() == str(adrB[headerIndex['WSID1']]).upper():
        wsid1Match = True
        
    #Determine pre/suf matches 
    if len(adrA[headerIndex['HNPRE']].strip())>0 and len(adrB[headerIndex['HNPRE']].strip()):
        if str(adrA[headerIndex['HNPRE']]).upper() == str(adrB[headerIndex['HNPRE']]).upper():
            hnPreMatch = True
        if str(adrA[headerIndex['HNSUF']]).upper() == str(adrB[headerIndex['HNSUF']]).upper():
            hnSufMatch = True
    
#    print('A HNSUF',adrA[headerIndex['HNSUF']])
#    print('B HNSUF',adrB[headerIndex['HNSUF']])
#    print('A WSID1',adrA[headerIndex['WSID1']])
#    print('B WSID1',adrB[headerIndex['WSID1']])
    #determine is hn suf = WSID1
    #if (len(adrA[headerIndex['HNSUF']].strip())>0  and len(adrB[headerIndex['WSID1']].strip())>0 ) or (len(adrB[headerIndex['HNSUF']].strip())>0  and len(adrA[headerIndex['WSID1']].strip())>0 ):
    if len(adrA[headerIndex['HNSUF']].strip())>0  and len(adrB[headerIndex['WSID1']].strip())>0  and \
        str(adrA[headerIndex['HNSUF']]).upper() == str(adrB[headerIndex['WSID1']]).upper():
            hnSufwsMatch = True
    elif len(adrB[headerIndex['HNSUF']].strip())>0  and len(adrA[headerIndex['WSID1']].strip())>0 and \
        str(adrA[headerIndex['WSID1']]).upper() == str(adrB[headerIndex['HNSUF']]).upper():
            hnSufwsMatch = True
        
#        or (str(adrA[headerIndex['WSID1']]).upper() == str(adrB[headerIndex['HNSUF']]).upper()):
#            hnSufwsMatch = True
    
    #derived and compund match types...
    
#    print('hnMatchSimple',hnMatchSimple)
#    print('nameMatchFid',nameMatchFid)
#    print('wsMatchSimple',wsMatchSimple)
    
    #"simple" match logic, because why not?
    simpleMatchResult = False
    if all([hnMatchSimple, nameMatchFid, wsMatchSimple]):
        simpleMatchResult = True
    
    #Full exact match first, should be easy...
    if all([hnExactMatch, exactMatch, wsid1Match]):
        fullExactMatch = True
    
    #Full equivocated Match... gets trickier...
    if any([hnMatchAmg, hnMatchSimple]) and any([nameMatchFid, exactMatch]) and any([wsMatchSimple, hnSufwsMatch, wsid1Match]):
        fullEquivMatch = True
    
    #BSA match, any
    if any([hnMatchAmg, hnMatchSimple]) and any([nameMatchFid, exactMatch]):
        bsaMatch = True
        
    #return row info:
    # fullEquivMatch, fullExactMatch, fidScore, bsaMatch, hnAmgResult, hnSufwsMatch, simpleMatchResult
    return (fullEquivMatch, fullExactMatch, fidScore, bsaMatch, hnAmgResult, hnSufwsMatch, simpleMatchResult)
        
        
    
    #street name
    
    #wsid
    
    #return order - original: #return (equivMatch, exactMatch, fidScore)
    

#-----------------------------------------------------------------------------        
def simpleMatch(adrA, adrB):
    pass
    hnMatch = False
    nameMatch = False
    wsMatch = False

    """
    fidOrder = ['OSN','ZIP','SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    hnSimple = ['HN']
    wsSimple = ['WS']
    
    hnFull = ['HNPRE', 'HN1', 'HNSEP', 'HN2']
    wsFull = ['WSDESC1', 'WSID1']
    numConvert = ['SNPTC','SNSTC','SNEC','SNPDC','SNSDC']
    """
    #adrA[headerIndex[x]]
    hnA = [adrA[headerIndex[x]] for x in hnSimple] #adrA[2]
    hnB = [adrB[headerIndex[x]] for x in hnSimple] #adrA[2]
    
    #wsA = adrA[4].split()
    #wsB = adrB[4].split()
    wsA = [pyNvl(adrA[headerIndex[x]], ' ') for x in wsSimple][0].split() #adrA[2]
    wsB = [pyNvl(adrB[headerIndex[x]], ' ') for x in wsSimple][0].split() #adrA[2]
    #simple extract of last number...
    if len(wsA)>0:
        wsA = wsA[-1]
    else:
        wsA = ''

    if len(wsB)>0:
        wsB = wsB[-1]
    else:
        wsB = ''        
    locFidOrderA = matchOrigCheck(adrA[headerIndex['OSN']], adrA[headerIndex['MSN']], cutOff=0)
    locFidOrderB = matchOrigCheck(adrB[headerIndex['OSN']], adrB[headerIndex['MSN']], cutOff=0)
    
    compA = [adrA[headerIndex[x]] for x in locFidOrderA]
    compB = [adrB[headerIndex[x]] for x in locFidOrderB]
    #convert codes to integers...
    compA = [int(x) if ei>1 else x for ei, x in enumerate(compA)]
    compB = [int(x) if ei>1 else x for ei, x in enumerate(compB)]
    
    
    #HOUSE NUMBER MATCHING
    if hnA == hnB:
        hnMatch = True
    else:
        try:
            #explore how badly you need to handle WSID variations...
            charListA = [x for x in hnA if x in string.ascii_letters]
            charListB = [x for x in hnB if x in string.ascii_letters]
            
            puntListA = [x for x in hnA if x in string.punctuation]
            puntListB = [x for x in hnB if x in string.punctuation]
            
            if len(charListA)==len(charListB) and len(puntListA)==len(puntListB) and len(charListA)+len(charListB)+len(puntListA)+len(puntListB)> 2:
                global hnTerms, hnPuntTerms
                hnTerms.add(''.join(charListA))
                hnTerms.add(''.join(charListB))
                hnPuntTerms.add(''.join(puntListA))
                hnPuntTerms.add(''.join(puntListB))
        except:
            pass

    
    if not hnMatch:
        #exit iteration early
        return (False, False, 0)


    #WS ID Matching
    if wsA == wsB:
        wsMatch = True
    else:
        #explore how badly you need to handle WSID variations...
        charListA = [x for x in wsA if x in string.ascii_letters]
        charListB = [x for x in wsB if x in string.ascii_letters]
        
        puntListA = [x for x in wsA if x in string.punctuation]
        puntListB = [x for x in wsB if x in string.punctuation]
        
        if len(charListA)==len(charListB) and len(puntListA)==len(puntListB) and len(charListA)+len(charListB)+len(puntListA)+len(puntListB)> 2:
            global wsTerms, puntTerms
            wsTerms.add(''.join(charListA))
            wsTerms.add(''.join(charListB))
            puntTerms.add(''.join(puntListA))
            puntTerms.add(''.join(puntListB))

    if not wsMatch:
        return (False, False, 0)      

    
    #STREET NAME MATCHING
    if compA == compB:
        #print('exact match, moving on...')
        nameMatch = True
        exactMatch = True
        fidList = list(chain.from_iterable(zip(compA,compB)))
        fidScore = amgScore.fidComparator(*fidList)
    else:
        fidList = list(chain.from_iterable(zip(compA,compB)))
        fidScore = amgScore.fidComparator(*fidList)
        if fidScore >= 800:
            nameMatch = True
            exactMatch = False        
    if not nameMatch:
        #exit iteration early
        return (False, False, 0)   

    if nameMatch and wsMatch and hnMatch:
        return (True, exactMatch, fidScore)
    else:
        print('unexpected matching criteria met, failing gracelessly')
        raise('this is a debug error, check your standard-out')

    #--- End of simpleMatch function...            
        
def bsaLinkages(rootPath, zip5):
    """
    This is a (primary block?) level handler meant to derive BSA linkages from a combination
    of both multimatch results and deduplication links.  this may be a work in progress...
    """
    from os.path import join
    
    linksPath = join(rootPath,r'Linkages\MPlinks_{zip5}.csv'.format(zip5=zip5))
    
    
    pass

#for standard fields:
headerDict = OrderedDict({'INPUTID': 0,
             'CUSTID': 1,
             'HN': 2,
             'STREETNAME': 3,
             'WS': 4,
             'ZIP': 5,
             'MSN': 6,
             'OSN': 7,
             'SNPTC': 8,
             'SNSTC': 9,
             'SNEC': 10,
             'SNPDC': 11,
             'SNSDC': 12,
             'BLOCK1': 13,
             'BLOCK2': 14,
             'BLOCK3': 15})
    





dsfSql = """
select rownum INPUTID,
x.dsf_delp_id custid, 
HNPRE,
HN1,
HNSEP,
HN2,
HNSUF,
HN,
PRETYP snptc,
SUFTYP snstc,
SUFQUAL snec,
PREDIR snpdc,
SUFDIR snsdc,
MATCHNAME MSN,
ORIGNAME OSN,
street streetname,
WSDESC WSDESC1,
wsid wsid1,
WS,
ZIP,
nvl(x.zip, ' ') BLOCK1, nvl(x.hn1, ' ') BLOCK2, nvl(x.wsid, ' ') BLOCK3 

from mafdata.dsf_super x
where x.zip3='{zip3}'
and x.zip = '{zip5}'
and x.dsf_record_type in ('S', 'F', 'H')
and x.rejectflag is not null
and x.hn is not null and x.street is not null
"""

dsfSql_BAD = """

"""

lehdSql = """
select 
INPUTID,
nvl(RAW_INPUTID, ' ') CUSTID,
nvl(LOCLOWHNPRE, ' ') HNPRE,
nvl(LOCLOWHN1, ' ') HN1,
nvl(LOCLOWHNSEP, ' ') HNSEP,
nvl(LOCLOWHN2, ' ') HN2,
nvl(LOCHNSUF, ' ') HNSUF,
nvl(LOCHN, ' ') HN,
nvl(LOCPRETYP, 0) SNPTC,
nvl(LOCSUFTYP, 0) SNSTC,
nvl(LOCSUFQUAL, 0) SNEC,
nvl(LOCPREDIR, 0) SNPDC,
nvl(LOCSUFDIR, 0) SNSDC,
nvl(LOCMATCHNAME, ' ') MSN,
nvl(LOCORIGNAME, ' ') OSN,
nvl(LOCNAME, ' ') STREETNAME,
nvl(LOCWSDESC, ' ') WSDEC1,
nvl(LOCWSID1, ' ') WSID1,
nvl(LOCWSID, ' ') WS,
nvl(LOCZIP, ' ') ZIP,
nvl(x.loczip, ' ') BLOCK1, 
nvl(x.LOCLOWHN1, ' ') BLOCK2, 
nvl(LOCWSID1, ' ') BLOCK3 
from mafdata.lehd_gssmg_vw_eval x
where x.loczip = '{zip5}'
and x.lochn is not null and x.locname is not null
"""


adminRecAllSql = """
select 
INPUTID,
'57_'||nvl(RAW_INPUTID, INPUTID) CUSTID,
nvl(LOCLOWHNPRE, ' ') HNPRE,
nvl(LOCLOWHN1, ' ') HN1,
nvl(LOCLOWHNSEP, ' ') HNSEP,
nvl(LOCLOWHN2, ' ') HN2,
nvl(LOCHNSUF, ' ') HNSUF,
nvl(LOCHN, ' ') HN,
nvl(LOCPRETYP, 0) SNPTC,
nvl(LOCSUFTYP, 0) SNSTC,
nvl(LOCSUFQUAL, 0) SNEC,
nvl(LOCPREDIR, 0) SNPDC,
nvl(LOCSUFDIR, 0) SNSDC,
nvl(LOCMATCHNAME, ' ') MSN,
nvl(LOCORIGNAME, ' ') OSN,
nvl(LOCNAME, ' ') STREETNAME,
nvl(LOCWSDESC, ' ') WSDEC1,
nvl(LOCWSID1, ' ') WSID1,
nvl(LOCWSID, ' ') WS,
nvl(LOCZIP, ' ') ZIP,
nvl(x.loczip, ' ') BLOCK1, 
nvl(x.LOCLOWHN1, ' ') BLOCK2, 
nvl(LOCWSID1, ' ') BLOCK3 
--Edit line here
from mafdata.GSSMG_{adminSrcZip}_EVAL x
--Edit line here
where x.loczip = '{zip5}'
and x.lochn is not null and x.locname is not null
and mafid_m is null and dup_flag is null
"""


blknSql = """
select 
INPUTID,
nvl(CUSTID, INPUTID) CUSTID,
nvl(HNPRE, ' ') HNPRE,
nvl(HN1, ' ') HN1,
nvl(HNSEP, ' ') HNSEP,
nvl(HN2, ' ') HN2,
nvl(HNSUF, ' ') HNSUF,
nvl(HN, ' ') HN,
nvl(SNPTC, 0) SNPTC,
nvl(SNSTC, 0) SNSTC,
nvl(SNEC, 0) SNEC,
nvl(SNPDC, 0) SNPDC,
nvl(SNSDC, 0) SNSDC,
nvl(MSN, ' ') MSN,
nvl(OSN, ' ') OSN,
nvl(STREETNAME, ' ') STREETNAME,
' ' WSDEC1,
nvl(WSID1, ' ') WSID1,
nvl(WS, ' ') WS,
nvl(ZIP, ' ') ZIP,
nvl(zip, ' ') BLOCK1, 
nvl(HN1, ' ') BLOCK2, 
nvl(WSID1, ' ') BLOCK3 
from BKDATA_STAN x
where x.zip = '{zip5}'
and x.hn is not null and x.streetname is not null
"""

gmafSql = """
select 
INPUTID,
nvl(RAW_INPUTID, INPUTID) CUSTID,
nvl(LOCLOWHNPRE, ' ') HNPRE,
nvl(LOCLOWHN1, ' ') HN1,
nvl(LOCLOWHNSEP, ' ') HNSEP,
nvl(LOCLOWHN2, ' ') HN2,
nvl(LOCHNSUF, ' ') HNSUF,
nvl(LOCHN, ' ') HN,
nvl(LOCPRETYP, 0) SNPTC,
nvl(LOCSUFTYP, 0) SNSTC,
nvl(LOCSUFQUAL, 0) SNEC,
nvl(LOCPREDIR, 0) SNPDC,
nvl(LOCSUFDIR, 0) SNSDC,
nvl(LOCMATCHNAME, ' ') MSN,
nvl(LOCORIGNAME, ' ') OSN,
nvl(LOCNAME, ' ') STREETNAME,
nvl(LOCWSDESC, ' ') WSDEC1,
nvl(LOCWSID1, ' ') WSID1,
nvl(LOCWSID, ' ') WS,
nvl(LOCZIP, ' ') ZIP,
nvl(x.loczip, ' ') BLOCK1, 
nvl(x.LOCLOWHN1, ' ') BLOCK2, 
nvl(LOCWSID1, ' ') BLOCK3 
from mafdata.gmaf_gssmg_vw_eval x
where x.loczip = '{zip5}'
and x.lochn is not null and x.locname is not null
"""

gppSql = """
select 
INPUTID,
nvl(RAW_INPUTID, ' ') CUSTID,
nvl(LOCLOWHNPRE, ' ') HNPRE,
nvl(LOCLOWHN1, ' ') HN1,
nvl(LOCLOWHNSEP, ' ') HNSEP,
nvl(LOCLOWHN2, ' ') HN2,
nvl(LOCHNSUF, ' ') HNSUF,
nvl(LOCHN, ' ') HN,
nvl(LOCPRETYP, 0) SNPTC,
nvl(LOCSUFTYP, 0) SNSTC,
nvl(LOCSUFQUAL, 0) SNEC,
nvl(LOCPREDIR, 0) SNPDC,
nvl(LOCSUFDIR, 0) SNSDC,
nvl(LOCMATCHNAME, ' ') MSN,
nvl(LOCORIGNAME, ' ') OSN,
nvl(LOCNAME, ' ') STREETNAME,
nvl(LOCWSDESC, ' ') WSDEC1,
nvl(LOCWSID1, ' ') WSID1,
nvl(LOCWSID, ' ') WS,
nvl(LOCZIP, ' ') ZIP,
nvl(x.loczip, ' ') BLOCK1, 
nvl(x.LOCLOWHN1, ' ') BLOCK2, 
nvl(LOCWSID1, ' ') BLOCK3 
from mafdata.gpp_gssmg_vw_eval x
where x.loczip = '{zip5}'
and x.lochn is not null and x.locname is not null
"""

br13Sql = """
select 
INPUTID,
nvl(RAW_INPUTID, ' ') CUSTID,
nvl(LOCLOWHNPRE, ' ') HNPRE,
nvl(LOCLOWHN1, ' ') HN1,
nvl(LOCLOWHNSEP, ' ') HNSEP,
nvl(LOCLOWHN2, ' ') HN2,
nvl(LOCHNSUF, ' ') HNSUF,
nvl(LOCHN, ' ') HN,
nvl(LOCPRETYP, 0) SNPTC,
nvl(LOCSUFTYP, 0) SNSTC,
nvl(LOCSUFQUAL, 0) SNEC,
nvl(LOCPREDIR, 0) SNPDC,
nvl(LOCSUFDIR, 0) SNSDC,
nvl(LOCMATCHNAME, ' ') MSN,
nvl(LOCORIGNAME, ' ') OSN,
nvl(LOCNAME, ' ') STREETNAME,
nvl(LOCWSDESC, ' ') WSDEC1,
nvl(LOCWSID1, ' ') WSID1,
nvl(LOCWSID, ' ') WS,
nvl(LOCZIP, ' ') ZIP,
nvl(x.loczip, ' ') BLOCK1, 
nvl(x.LOCLOWHN1, ' ') BLOCK2, 
nvl(LOCWSID1, ' ') BLOCK3 
from mafdata.br13_gssmg_vw_eval x
where x.loczip = '{zip5}'
and x.lochn is not null and x.locname is not null
"""


mafxFilterSql = """
"""

#{benchSchema} 
#and a.zip = '{zip5}'
mafxFullSql = """
select 
rownum INPUTID, xa.*,
nvl(xa.zip, ' ') BLOCK1, nvl(xa.hn1, ' ') BLOCK2, nvl(xa.wsid1, ' ') BLOCK3  
from (
select
CUSTID,
max(HNPRE) keep (dense_rank last order by TOTAL asc) HNPRE,
max(HN1) keep (dense_rank last order by TOTAL asc) HN1,
max(HNSEP) keep (dense_rank last order by TOTAL asc) HNSEP,
max(HN2) keep (dense_rank last order by TOTAL asc) HN2,
max(HNSUF) keep (dense_rank last order by TOTAL asc) HNSUF,
max(HN) keep (dense_rank last order by TOTAL asc) HN,
max(SNPTC) keep (dense_rank last order by TOTAL asc) SNPTC,
max(SNSTC) keep (dense_rank last order by TOTAL asc) SNSTC,
max(SNEC) keep (dense_rank last order by TOTAL asc) SNEC,
max(SNPDC) keep (dense_rank last order by TOTAL asc) SNPDC,
max(SNSDC) keep (dense_rank last order by TOTAL asc) SNSDC,
max(MSN) keep (dense_rank last order by TOTAL asc) MSN,
max(OSN) keep (dense_rank last order by TOTAL asc) OSN,
max(STREETNAME) keep (dense_rank last order by TOTAL asc) STREETNAME,
max(WSDESC1) keep (dense_rank last order by TOTAL asc) WSDESC1,
max(WSID1) keep (dense_rank last order by TOTAL asc) WSID1,
max(WS) keep (dense_rank last order by TOTAL asc) WS,
max(ZIP) keep (dense_rank last order by TOTAL asc) ZIP

from (
select ad.oid custid,
ad.hnpre hnpre,
ad.hn1 hn1,
ad.hnsep hnsep,
ad.hn2 hn2,
ad.hnsuf hnsuf,
trim(REGEXP_REPLACE(ad.hnpre||' '||ad.hn1||' '||ad.hnsep||' '||ad.hn2||' '||ad.hnsuf, '\s{{2,}}', ' ')) HN,
nvl(mn.pretyp, 0) snptc,
nvl(mn.suftyp, 0) snstc,
nvl(mn.sufqual, 0) snec,
nvl(mn.predir, 0) snpdc,
nvl(mn.sufdir, 0) snsdc,
nvl(mn.msn, ' ') MSN,
nvl(mn.osn, ' ') OSN,
fn.displayname streetname,
sc1.descr wsdesc1,
ad.wsid1,
trim(REGEXP_REPLACE(sc1.descr||' '||ad.wsid1, '\s{{2,}}', ' ')) WS,
ad.zip zip,
count(*) TOTAL

from {benchSchema}.matchname mn join {benchSchema}.unstanname un on un.oidmn = mn.oid
join {benchSchema}.featurename fn on fn.oid = un.oidfn
join {benchSchema}.address ad on ad.oidfn = fn.oid or ad.oidbn = fn.oid
left join mafdata.stancode sc1 on sc1.code = ad.wsdesc1
where ad.zip = '{zip5}'
and ad.mtfcc='E1000'
and (sc1.category = 'WS'  or sc1.category is null )  

group by ad.oid,
ad.hnpre,
ad.hn1,
ad.hnsep,
ad.hn2,
ad.hnsuf,
nvl(mn.pretyp, 0),
nvl(mn.suftyp, 0),
nvl(mn.sufqual, 0),
nvl(mn.predir, 0),
nvl(mn.sufdir, 0),
nvl(mn.msn, ' '),
nvl(mn.osn, ' '),
fn.displayname,
ad.zip,
sc1.descr,
ad.wsid1
) x
group by custid
) xa

"""



mafxFullSql_all_MTFCC = """
select 
rownum INPUTID, xa.*,
nvl(xa.zip, ' ') BLOCK1, nvl(xa.hn1, ' ') BLOCK2, nvl(xa.wsid1, ' ') BLOCK3  
from (
select
CUSTID,
max(HNPRE) keep (dense_rank last order by TOTAL asc) HNPRE,
max(HN1) keep (dense_rank last order by TOTAL asc) HN1,
max(HNSEP) keep (dense_rank last order by TOTAL asc) HNSEP,
max(HN2) keep (dense_rank last order by TOTAL asc) HN2,
max(HNSUF) keep (dense_rank last order by TOTAL asc) HNSUF,
max(HN) keep (dense_rank last order by TOTAL asc) HN,
max(SNPTC) keep (dense_rank last order by TOTAL asc) SNPTC,
max(SNSTC) keep (dense_rank last order by TOTAL asc) SNSTC,
max(SNEC) keep (dense_rank last order by TOTAL asc) SNEC,
max(SNPDC) keep (dense_rank last order by TOTAL asc) SNPDC,
max(SNSDC) keep (dense_rank last order by TOTAL asc) SNSDC,
max(MSN) keep (dense_rank last order by TOTAL asc) MSN,
max(OSN) keep (dense_rank last order by TOTAL asc) OSN,
max(STREETNAME) keep (dense_rank last order by TOTAL asc) STREETNAME,
max(WSDESC1) keep (dense_rank last order by TOTAL asc) WSDESC1,
max(WSID1) keep (dense_rank last order by TOTAL asc) WSID1,
max(WS) keep (dense_rank last order by TOTAL asc) WS,
max(ZIP) keep (dense_rank last order by TOTAL asc) ZIP

from (
select ad.oid custid,
ad.hnpre hnpre,
ad.hn1 hn1,
ad.hnsep hnsep,
ad.hn2 hn2,
ad.hnsuf hnsuf,
trim(REGEXP_REPLACE(ad.hnpre||' '||ad.hn1||' '||ad.hnsep||' '||ad.hn2||' '||ad.hnsuf, '\s{{2,}}', ' ')) HN,
nvl(mn.pretyp, 0) snptc,
nvl(mn.suftyp, 0) snstc,
nvl(mn.sufqual, 0) snec,
nvl(mn.predir, 0) snpdc,
nvl(mn.sufdir, 0) snsdc,
nvl(mn.msn, ' ') MSN,
nvl(mn.osn, ' ') OSN,
fn.displayname streetname,
sc1.descr wsdesc1,
ad.wsid1,
trim(REGEXP_REPLACE(sc1.descr||' '||ad.wsid1, '\s{{2,}}', ' ')) WS,
ad.zip zip,
count(*) TOTAL

from {benchSchema}.matchname mn join {benchSchema}.unstanname un on un.oidmn = mn.oid
join {benchSchema}.featurename fn on fn.oid = un.oidfn
join {benchSchema}.address ad on ad.oidfn = fn.oid or ad.oidbn = fn.oid
left join mafdata.stancode sc1 on sc1.code = ad.wsdesc1
where ad.zip = '{zip5}'
and (sc1.category = 'WS'  or sc1.category is null )  

group by ad.oid,
ad.hnpre,
ad.hn1,
ad.hnsep,
ad.hn2,
ad.hnsuf,
nvl(mn.pretyp, 0),
nvl(mn.suftyp, 0),
nvl(mn.sufqual, 0),
nvl(mn.predir, 0),
nvl(mn.sufdir, 0),
nvl(mn.msn, ' '),
nvl(mn.osn, ' '),
fn.displayname,
ad.zip,
sc1.descr,
ad.wsid1
) x
group by custid
) xa

"""


print('__________________________________________________________________________________')
print("Don't forget to come back to AMG SCORE and work on equivocating Unit A == Apt 1!!!")
print('__________________________________________________________________________________')
    
from string import ascii_uppercase
stringDict = {}
for e, letter in enumerate(ascii_uppercase):
    stringDict[letter]=e
    stringDict[e]=letter

def wsidAlphaNumMatch(adrA, adrB):
    """
hnSimple = ['HN']
wsSimple = ['WS']
#HNPRE|HN1|HNSEP|HN2|HNSUF|HN
hnAmgOrder = ['HN1','HNSEP','HN2']

hnFull = ['HN1', 'HNSEP', 'HN2']
hnFull2 = ['HNPRE', 'HN1', 'HNSEP', 'HN2', 'HNSUF']
wsFull = ['WSDESC1', 'WSID1']    
    """
    
    
    pass



if __name__=='__main__':
    import ast 
    from itertools import chain
    tHeader, tData = loadPipeCsv('linksPair.csv')
    
    adrA = tData[0]
    adrB = tData[1]
    print(adrA)
    print(adrB)
    print("(fullEquivMatch, fullExactMatch, fidScore, bsaMatch, hnAmgResult, hnSufwsMatch, simpleMatchResult)")
    print(multiMatch1(adrA, adrB))
    
        
