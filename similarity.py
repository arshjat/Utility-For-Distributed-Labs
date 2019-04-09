
# IMPORT PACKAGES
import math
from collections import Counter

def counter_cosine_similarity(c1, c2):
    """
    This functions calculates Cosine similarity metric between two Counters.
    Input : 
        Argument 1 - Counter
        Argument 2 - Counter

    Output :         int
    Requirements :   None
    """

    terms = set(c1).union(c2)

    # DOT PRODUCT
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    
    # TO AVOID DIVISIBILITY BY ZERO CONDITION, WE DIVIDE BY 0.01
    if magA==0 or magB ==0 :
        return dotprod / 0.01
    else:
        return dotprod / (magA * magB)


def length_similarity(c1, c2):
    """
    This funtion calculates the Length similarity metric.
    Input :
        Argument 1 - Counter
        Argument 2 - Counter

    Output :         int
    Requirements :   None
    """
    lenc1 = sum(c1.values())
    lenc2 = sum(c2.values())
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))

def similarity_score(l1, l2):
    """
    This function returns the similarity score metric which is calculated by multiplying the cosine_similarity
    and length similarity metrics.
    Input :    
        Argument 1 - List
        Argument 2 - List

    Output :         int
    Requirements :   Calculations by cosine_similarity and length _similarity functions.
    """

    # LISTS ARE CONVERTED TO COUNTERS TO GIVE TO ABOVE FUNCTIONS.
    c1, c2 = Counter(l1), Counter(l2)
    return length_similarity(c1, c2) * counter_cosine_similarity(c1, c2)

