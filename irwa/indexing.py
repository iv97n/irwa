from collections import defaultdict

import numpy as np


def create_inverted_index(token_tweets):

    inverted_index = defaultdict(set)
    
    # Iterate over each document
    for doc_id, tokens in token_tweets.items():
        # For each token in the document
        for token in tokens:
            # Append the document ID to the token's set
            inverted_index[token].add(doc_id)
    
    return inverted_index


# ------------TO BE REVIEWED-------------------


def create_inverted_index_tf_idf(documents):

    # Create inverted index
    inverted_index = create_inverted_index(documents)

    num_documents = len(documents)
    # Dictionaty containing as keys the doc_id and as values a dictionary containing as key the term and as value the frequency of the term in the dictionary
    tf = defaultdict(lambda: defaultdict(int))
    # Dicitionary containing as keys the terms and as values the document frequency of such terms
    df = defaultdict(int)
    # Dictionary containing as keys the terms and as values the inverse document frequency of such terms
    idf = defaultdict(float)

    for doc_id, content in documents.items():
        for term in content:
            tf[doc_id][term] += 1

    for term, values in inverted_index.items():
        # The document frequency of a term is the lenght of the set value in the inverted index
        df[term] = len(values)
        # Compute the idf as the logarithm of the division between the number of documents and the document frequency
        idf[term] = np.round(np.log(float(num_documents / df[term])), 4)
    
    

    return  inverted_index, tf, idf

            