## Suggestions for improvement
### Standardizer

#### Flaw: usaddress parsing 

usaddress *can* have errors in parsing; using tag() can lead to RepeatedLabelError, which is a result of the parser identifying two separate pieces of the address as the same label. More generally, it's not a perfect tool, and it can also just plain mislabel things.
The crosswalk we have between usaddress categories and the Census’s categories is slightly incomplete (SNE, OccupancyType, etc. are noted challenges); this leads to errors were you to try and update data records, as some address components do not exist in the rules of one tool or the other 

We suggest, as a more long-term and stable solution, ultimately retraining and/or partially rewriting usaddress using the underlying parserator and crfsuite packages - a general purpose package for using conditional random fields. The actual address-specific implementation code in usaddress is only ~300 lines long; changing the built-in categories into the census’s address schema should be possible.

#### Suggestion: training data

We aren't completely sure of how to get ground truth training data; one possibility is to look toward preexisting MAF/address data that we trust to be properly parsed as a starting point. However, this might break down when we get to obtaining a wide spread of correctly labeled “unusual” data – those with the less common bits, like Within Structure IDs, if the legacy parser also fails here. Overall, though, conditional random fields require relatively little amounts of data; this might be relatively feasible.

#### Improvement: more standardizations 

You can add customized functions to parse address components as necessary; there's a function dictionary in standardizer.py that maps address components to standardization/processing functions. 

In addition, we have a few suggestions:
* add more substitutions – common abbreviations, for example, for street names 
* Extra rules & capabilities for phrases of multiple words; more generally, n-gram phrases (most relevant for street names)
* add any missing standardization codes for some street/building/etc. types


### Matching 

#### Flaw: Comparator 

FidComparator alone can lead to too many false positives – it doesn’t account for house numbers, within structure identifiers, place names, and other address characteristics. Because of this, we also filter on exact matches of HN/WS/occupancy code. This is somewhat unwieldy or inflexible, and sometimes too restrictive, especially given usaddress’s above-mentioned challenges in parsing WS & occupancy codes. 
As OccupancyType and OccupancyIdentifier don’t quite exist in the Census address framework, an alternative will be necessary in the long run. Moreover, the setup for how exactly comparisons should be would ideally be modular and customizeable; this implementation is slightly hardcoded, and could do with changing.

#### Improvement: Build a new comparator function(s) 

This started to step too far outside the scope of our goals and knowledge of addresses; however, someone with more geography and address experience might be able to create a unified function that also accounts for these other fields (HN/WS/etc.)
A few suggeestions for what this comparator would include: 
* optional levels or varieties of input might be useful 
* e.g. scoring on just street characteristics, or street + house number, or street + WS + HN, etc. 

Some more sophisticated suggestions... 
##### Ideas from ‘A deep learning architecture for semantic address matching' 

https://www.tandfonline.com/doi/full/10.1080/13658816.2019.1681431 
Intended to work in the absence of a strong standardization system, I think that this model could be used to find matches amongst a lot of the unique/out of the ordinary cases (Puerto Rican addresses potentially?) 

* Summary – Tokenized word vectors are created using word2vec (see below) and a inferential learning model identifies matches between vectors 
* Benefits – This system was originally developed around the inconsistencies that have emerged in the structure/conventions of writing addresses 
* Requirements – A ground truth set of address matches and fails which would serve as training data for the model 

The code implementation of this paper is here, all that is additionally needed to use this repo is a ground truth training dataset: https://github.com/linyuehzzz/semantic_address_matching 

##### Using word2vec - paraphrased from "Machine learning innovations in address matching" 

Similar to TF-IDF, the goal is to create comparison vectors that can distinguish matches from non-matches. TF-IDF relies on the term frequencies to create vectorized representations, but word2vec utilizes the syntactic and semantic structure of the corpus to create tokenized representations – this could create more precise or nuanced ways of finding matches. We can use a cosine similarity score to compare the two vectors and find a match.

 
#### Runtime 

While Pandas has some optimized structures that we have taken advantage of, there are notable improvements possible. A few disclaimers:

* This code has not been parallelized or multithreaded 
  * We are unsure how this would work with pandas; neither of us know extensively about the underlying C to Python interface.
* This code also has not been optimized for running on servers or clusters; applying additional techniques would make it more compatible for large-scale computing 

### Network Deduplication 

#### Flaw: Lack of evaluability 

It’s difficult to tell how accurate Affinity Propagation, and clustering in general, is. This was very much an experimental approach toward deduplication, with little precedent. Almost by definition, we don’t have ground-truth answers available, and the efficacy of this tool may be as dependent on amgScore.py's comparator functions as it is on the machine learning. It may be worthwhile to look at how non-machine learning algorithms would handle this, and decide what best fits your needs.  

#### Improvement: Create a testing framework to assess effectiveness 

We’re not actually sure if there’s a standard way to do this. Neither of us authors are machine learning experts, and did not research how unsupervised learning is assessed (aside from with our own eyeballs and in comparison to other algorithms.) 
* One suggestion we might have: try a testing file of known duplicate records, and a “correct” file of how the duplicates would ideally be reduced

#### Idea: Accuracy 

As mentioned above, it might be feasible to compare Affinity Propagation to other network clustering algorithms. Some require more parameters, or multiple seeded iterations, and not all are easily available through sklearn - which is why we used this algorithm to start. There's probably also a lot of math that would help make informed decisions to improve this; we don't know that math.
* Tentative suggestion: similar to a random forest, we could run multiple different algorithms and weight outputs into a combined decisions 
This will likely be *quite* slow, however, and we're unsure if this will be more effective. Try any preliminary attempts *after* establishing some testing tools.

 

### Spellchecking 

#### Flaw: Runtime
Essentially the same problems and suggestions as with matching; see above.

#### Flaw: Scoring 

The scoring formula is mostly arbitrary; while it doesn't seem to be terribly unbalanced, calibrating it more rigorously or coming up with a better formula, or at least extensively testing it on your data needs, is highly suggested.
* The current formula is log(count) * 10^(1-distance), with a minimum score of 1 to replace the base word.

#### Idea: Experiment with n-grams 

The current system splits addresses based on the parser; it might be worthwhile to consider... 
1. split by word within a component category (I.e. by every word in a street name (“Yellow” “Brick”), as opposed to full street name chunks (“Yellow Brick”), or some combination of both (in other words, both 1- and 2-grams) 
2. check key combinations of categories (I.e. instead of correcting street name and street post type separately, looking at n-pairs of them (“Yellow” “Brick”), as opposed to full street name chunks (“Yellow Brick”), or some combination of both (in other words, both 1- and 2-grams 


### Number Processing 

#### Improvement: Implement functionality for fractions 

Fractional house numbers are a known element of addresses; there may be street names or other situations with fractions as well. This would also require being less judicial about removing punctuation and slashes in standardizer.
