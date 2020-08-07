# address-standardizer
***Overall Summary***: A package for the parsing, normalization, and probabilistic matching of address data based on USPS and Census Bureau standards completed by Aishani Dutta and Evan Dong as part of the Summer 2020 [Civic Digital Fellowship](https://www.codingitforward.com/fellowship). The components of our work are as follows:

***Parsing + Standardization***: 
We expanded the capabilities of the [usaddress parser](https://github.com/datamade/usaddress) and the reference dictionaries in the [scourgify](https://github.com/GreenBuildingRegistry/usaddress-scourgify) standardizer to build an accurate, working standardization system. Our standardizer will separate an input address into labeled parts and abbreviate components according to USPS conventions when appropriate. 
In addition, the script in comparator.py will convert a standardized address into the input list for the fidCompare function in amgScore.py 

***Data Edits***: 

- *Number Processing* 

    - Converts numbers back and forth between numerical text, as well as adding or removing ordinal endings (e.g. “1023” <-> “one thousand twenty three”, “fifth” <-> “5th”), with intuitive handling of non-standard formats for numerical text – cases like “fourteen ninety two" -> “1492”, which break simpler tools 

- *Spell Checking*

    - Takes in two files of address records: one, a corpus of data, which is used to correct given components (e.g. street names) of the records in the second file. 
Corrections are scored by the frequency of terms in the first corpus and their edit distance (optionally with some cutoff; may improve speed in large datasets) from the corrected term  

- *Phonetic Matching*

    - Given two sets of  addresses, this script will output a file indicating the phonetic similarity between each pair of entries using the NYSIIS Algorithm 
The similarity score between two addresses is determined by assigning a phonetic encoding to each syllable within each address and calculating the Levenshtein distance between the encoded entries 

***Optimized Matching System***: Created with blocking and optimization features in the pandas library

- *Graphs/Network Deduplication*

    - Given a score from fidComparator, or other kind of “similarity score” weight for matching, we can represent clusters of matches as graph networks. We experimented with applying Affinity Propagation clustering to isolate exemplars for deduplication.

```
from tools.matching import keyMatch

## Create two dataframes from pipe delimited test files comparisonData.csv and testData.csv
frameA = keyMatch.csv_to_frame("comparisonData.csv", "CUSTID", "ADDRESS", delimiter='|')
frameB = keyMatch.csv_to_frame("testData.csv", "CUSTID", "ADDRESS", delimiter='|')

## Print a dataframe demonstrating all plausible matches
print(keyMatch.records_to_matches(frameA, frameB, show_errors=False))

## Print a dataframe showing all plausible duplicates within a single file
print(keyMatch.records_to_matches(frameA, show_errors=False))
```
