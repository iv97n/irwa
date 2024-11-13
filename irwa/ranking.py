from collections import defaultdict, Counter
import math
import numpy as np
from numpy import linalg as la
import irwa.preprocessing as ipp
import irwa.indexing as ind



def conjunctive_filtering(query, documents):
    """
    Function for filtering the documents based on an input cojunctive query

    Args:
        query (list): A list of terms representing the input query.
        documents (_type_): A dictionary with document IDs as keys and lists of terms as values.
        
    Returns:
        Set containing the document ids of the documents that contain all the words of the query
    """

    # Set for storing the document id of the documents that contain all the words in the query
    valid_documents = set()

    for document_id, document_terms in documents.items():
        if all(query_term in document_terms for query_term in query):
            valid_documents.add(document_id)

    return valid_documents


# Tf-idf functions


def display_scores_tf_idf(scores, docid_to_tweetid, tweets, n=10):
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

def rank_documents_tf_idf(query, documents, inverted_index, tf, idf, document_filtering=None):
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

    # Iterate over each term of the query, without repeating terms (i.e. for each distinct element of the query)
    for index, term in enumerate(query):
        
        vectorized_query[index] = query_terms_count[term] / query_norm * idf[term] 
        
        # For a document to be considered it has to be a candidate document and have the corresponding term.
        # If the term does not exist in the vocabulary it is not considered.
        for doc in (candidate_docs & inverted_index.get(term, set())):
            doc_norm = la.norm(list(tf[doc].values())) 
            vectorized_docs[doc][index] = tf[doc][term] / doc_norm * idf[term]

    # Compute the cosine similar between each document and the input query.
    doc_scores = [(doc, np.dot(vectorized_doc, vectorized_query)) for doc, vectorized_doc in vectorized_docs.items()]

    # Sort the documents by score
    doc_scores.sort(reverse=True, key=lambda doc_score: doc_score[1])

    return doc_scores

# Our score functions

def rank_documents_our_score(tweets, docid_to_tweetid, doc_scores, alpha=0.5, k0 =1, k1=1, k2=1, k3=1):
    """
    Rank tweets based on TF-IDF similarity with a query and an engagement score.

    Parameters:
    - tweets: Dictionary of Tweet objects.
    - docid_to_tweetid: Dictionary mapping document IDs to tweet IDs.
    - doc_scores: document ID and its similarity score to the query.
    - alpha: Weight for TF-IDF and engagement score in the final score.
    - k0, k1, k2, k3: Scaling factors for retweet and quote counts.
    
    Returns:
    - Ranked list of (Tweet, score) tuples.
    """

    # Initialize list for ranking
    ranked_tweets = []
    
    # Process scores and compute final score
    for doc_id, similarity_score in doc_scores:
        tweet_id = docid_to_tweetid[doc_id]

        # Calculate engagement score
        tweet = tweets[tweet_id]
        engagement_score = k0 * tweet._like_count + k1 * tweet._retweet_count + k2 * tweet._quote_count + k3 * tweet._reply_count

        
        # Final score
        final_score = alpha * similarity_score + (1-alpha) * engagement_score
        ranked_tweets.append((doc_id, final_score))

     # Extract scores for normalization
    scores = [score for _, score in ranked_tweets]
    min_score = min(scores)
    max_score = max(scores)

    # Apply Min-Max normalization
    if max_score > min_score:  # Prevent division by zero
        normalized_ranked_tweets = [
            (doc_id, (final_score - min_score) / (max_score - min_score))
            for doc_id, final_score in ranked_tweets
        ]
    else:
        # If all scores are the same, normalize to 0.5
        normalized_ranked_tweets = [
            (doc_id, 0.5)  # Arbitrary middle value
            for doc_id, _ in ranked_tweets
        ]

    # Sort tweets by normalized score in descending order
    normalized_ranked_tweets.sort(key=lambda x: x[1], reverse=True)
    
    return normalized_ranked_tweets


def calculate_avgdl(documents):
    """
    Calculate the average document length (avgdl) for a collection of documents.

    Args:
        documents (dict): A dictionary of documents, where each key is a document 
                          ID (e.g., a string or integer) and each value is a list of 
                          terms in the document.

    Returns:
        float: The average document length, or 0 if there are no documents.
    """
    total_length = sum(len(doc) for doc in documents.values())
    return total_length / len(documents) if documents else 0



def rank_documents_bm25(query, documents, inverted_index, tf, idf, k1=1.2, b=0.75):
    """
    Rank documents using the BM25 score based on the query and document statistics.

    Args:
        query : tokenized input query.
        documents (dict): A dictionary with document IDs as keys and lists of terms as values.
        inverted_index (defaultdict(set)): An inverted index with terms as keys and sets of document IDs where those terms appear.
        tf (defaultdict(defaultdict(int))): Term frequency dictionary mapping document IDs to another dictionary that maps terms to their frequency in that document.
        idf (defaultdict(float)): Inverse document frequency dictionary mapping terms to their IDF values.
        k1 (float): BM25 parameter for term frequency scaling.
        b (float): BM25 parameter for document length normalization.

    Returns:
        list: A list of tuples where each tuple contains a document ID and its BM25 score, sorted by score in descending order.
    """
    
    # Calculate the average document length across all documents
    avgdl = calculate_avgdl(documents)
    
    # Dictionary to store the BM25 score for each document
    doc_scores = defaultdict(float)
    
    for index, term in enumerate(query):
        if term not in inverted_index:
            continue

        # Get the inverse document frequency for the term
        term_idf = idf[term]

        for doc_id in inverted_index[term]:
            # Term frequency of the term in the document
            term_freq = tf[doc_id][term]
            
            # Document length
            doc_length = len(documents[doc_id])
            
            # BM25 score calculation
            score = term_idf * ((term_freq * (k1 + 1)) / (k1 * ((1 - b) + b * (doc_length / avgdl)) + term_freq))
            
            # Accumulate the score for the document
            doc_scores[doc_id] += score

    # Sort documents by their BM25 score in descending order
    ranked_docs = sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)
    
    return ranked_docs

def create_tweet2vec(token_tweets, model):
    """
    Converts each tweet into a unique vector representation by averaging the vectors 
    of the words it contains, using a trained Word2Vec model.

    Parameters:
    token_tweets (dict): Dictionary where keys are document IDs and values are lists of tokenized words in each tweet.
    model (gensim.models.Word2Vec): Trained Word2Vec model used to generate word vectors.

    Returns:
    dict: A dictionary where keys are document IDs and values are the averaged word vectors representing each tweet.
    """
    
    tweet2vec = dict()
    for doc_id in token_tweets:
        tweet_vectors = [model.wv[word] for word in token_tweets[doc_id] if word in model.wv]
        if len(tweet_vectors)!=0:
            tweet2vec[doc_id] = sum(tweet_vectors) / len(tweet_vectors)
    return tweet2vec


def tweet2vec_cossim(tweet2vec, model, query):
    """
    Calculates the cosine similarity between a given query and each tweet vector 
    in a collection, returning sorted similarity scores.

    Parameters:
    tweet2vec (dict): Dictionary where keys are document IDs and values are vector representations of each tweet.
    model (gensim.models.Word2Vec): Trained Word2Vec model used to generate word vectors.
    query (list of str): List of words representing the query.

    Returns:
    list of tuples: A sorted list of tuples, where each tuple contains a document ID 
                    and the cosine similarity score between the query and the tweet.
                    Sorted in descending order of similarity.
    """
    
    # Vectorize the query
    query_vectors = [model.wv[word] for word in query if word in model.wv]
    if len(query_vectors)==0: 
        print("THE QUERY CANNOT BE VECTORIZED WITH THE CURRENT MODEL")
        return 0
    query_vect = sum(query_vectors) / len(query_vectors)
    query_norm = la.norm(query_vect)

    # Compute the cosine similarity between each document and the input query.    
    doc_scores = [(doc, np.dot(vectorized_doc/la.norm(vectorized_doc), query_vect/query_norm)) for doc, vectorized_doc in tweet2vec.items()]

    # Sort the documents by score
    doc_scores.sort(reverse=True, key=lambda doc_score: doc_score[1])

    return doc_scores
