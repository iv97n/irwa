from collections import defaultdict, Counter
import math
import numpy as np
from numpy import linalg as la
import irwa.preprocessing as ipp
import irwa.indexing as ind


def display_scores_tf_idf(scores, docid_to_tweetid,tweets, n=10):
    """
    Displays the top-ranked documents based on their TF-IDF similarity scores.

    Args:
        scores (list): A list of tuples containing document IDs and their similarity scores, sorted in descending order
        by score.
        docid_to_tweetid (dict): A dictionary mapping document IDs to tweet IDs.
        tweets (dict): A dictionary where keys are tweet IDs and values are tweet objects. Each tweet object should have
        an attribute `_content` representing the original tweet content.
        n (int, optional): The number of top results to display. Defaults to 10.

    Returns:
        None: The function prints the top `n` results, including document ID, similarity score, and original tweet
        content.
    """
    aux = 1
    print(f"Top {n} Results:\n------------------------------------------------------------")
    for doc_id, score in scores[:n]:
        tweet_id = docid_to_tweetid[doc_id]
        original_tweet_content = tweets[tweet_id].get_content()
        print("RESULT", aux)
        print(f"Document {doc_id}: {score}")
        print(f"Content: {original_tweet_content}")
        print("------------------------------------------------------------")
        aux += 1


def conjunctive_filtering(query, documents):
    """
    Function for filtering the documents based on an input cojunctive query

    Args:
        query (string): _description_
        documents (_type_): _description_
        
    Returns:
        Set containing the document ids of the documents that contain all the words of the query
    """

    # Set for storing the document id of the documents that contain all the words in the query
    valid_documents = set()

    for document_id, document_terms in documents.items():
        if all(query_term in document_terms for query_term in query):
            valid_documents.add(document_id)

    return valid_documents


def rank_documents(query, documents, inverted_index, tf, idf, document_filtering=None):
    """
    Function for ranking the documents based on an input query and using the tf-idf as the similarity metric  

    Args:
        query (list): A list of terms representing the input query.
        documents (dict): A dictionary with document IDs as keys and lists of terms as values.
        inverted_index (defaultdict(set)): An inverted index with terms as keys and sets of document IDs where those
        terms appear.
        tf (defaultdict(defaultdict(int))): Term frequency dictionary mapping document IDs to another dictionary that
        maps terms to their frequency in that document.
        idf (defaultdict(float)): Inverse document frequency dictionary mapping terms to their IDF values.
        document_filtering: (function, optional): A function to filter documents before ranking. Defaults to None.

    Returns:
        list: A list of tuples where each tuple contains a document ID and its similarity score to the query, sorted by
        score in descending order.
    """

    # Filter the documents if any filtered method specified
    candidate_docs = document_filtering(query, documents) if document_filtering is not None else set(doc_id for doc_id
                                                                                                     in documents.keys())

    # Dictionary mapping from doc_id to the vectorized document (only containing as many dimensions as words specified
    # in the query)
    vectorized_docs = defaultdict(lambda: [0] * len(query))
    
    # Array containing the vectorized query
    vectorized_query = [0] * len(query)

    # Counter with terms of the query and their respective counts
    query_terms_count = Counter(query)
    query_norm = la.norm(list(query_terms_count.values()))

    # Iterate over each term of the query, without repeating terms (i.e for each distinct element of the query)
    for index, term in enumerate(query):
        
        vectorized_query[index] = query_terms_count[term] / query_norm * idf[term] 
        
        # For a document to be considered it has to be a candidate document and have the corresponding term.
        # If the term does not exist in the vocabulary it is not considered
        for doc in (candidate_docs & inverted_index.get(term, set())):
            doc_norm = la.norm(list(tf[doc].values())) 
            vectorized_docs[doc][index] = tf[doc][term] / doc_norm * idf[term]

    # Compute the cosine similar between each document and the input query.
    doc_scores = [(doc, np.dot(vectorized_doc, vectorized_query)) for doc, vectorized_doc in vectorized_docs.items()]

    # Sort the documents by score
    doc_scores.sort(reverse=True, key=lambda doc_score:doc_score[1])

    return doc_scores
