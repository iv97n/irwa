from collections import defaultdict, Counter
import math

import numpy as np
from numpy import linalg as la

import irwa.preprocessing as ipp
import irwa.indexing as ind

def tf_idf(inverted_index, query, token_tweets):
    N = len(token_tweets)                               # Total number of documents
    scores = defaultdict(float)                         # Store scores for each document
    tokenized_query = ipp.build_terms(query)
    # For each term in the query
    for term in tokenized_query:
        if term in inverted_index:
            df = len(inverted_index[term])              # Document Frequency of the term --> en cuántos documentos aparece palabra de la query
            idf = math.log(N / (df))                      # Inverse Document Frequency --> modificación por razones matemáticas del df
            
            for doc_id in inverted_index[term]:         # Para todos los documentos en los que aparece la palabra de la query
                tf = token_tweets[doc_id].count(term)   # Term Frequency in the document --> contar cuantas veces aparece por documento
                if (tf!=0):
                    tf = 1 + math.log(tf)
                scores[doc_id] += tf * idf              # Calculate and accumulate tf-idf score --> tf (numero de apariciones en documento) * idf (valor igual para todos los documentos)
                                                        # Al repetir el proceso para mas palabras, acumulamos el score total del documento es decir sum_todas_palabras_query(tf*idf de cada palabra)
    return dict(scores)

def sort_scores_tf_idf(scores, docid_to_tweetid,tweets, n=10):
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    # Display the top n results
    print(f"Top {n} Results:")
    for doc_id, score in sorted_scores[:n]:
        tweet_id = docid_to_tweetid[doc_id]
        original_tweet_content = tweets[tweet_id]._content
        print(f"Document {doc_id}: {score}")
        print(f"Content: {original_tweet_content}")


# --------------------- TO BE REVIEWED ---------------------

def conjunctive_filtering(query, documents):
    """Function for filtering the documents based on an input cojunctive query

    Args:
        query (string): _description_
        token_tweets (_type_): _description_
    Returns:
        Set containing the document ids of the documents that contain all the words of the query
    """

    # Set for storing the document id of the documents that contain all the words in the query
    valid_documents = set()

    for document_id, document_terms in documents.items():
        if all(query_term in document_terms for query_term in query):
            valid_documents.add(document_id)

    return valid_documents


def rank_documents(query, documents, inverted_index, tf, idf, filter=None):
    """Function for ranking the documents based on an input query and using the the tf-idf as simmilarity metric  

    Args:
        query (_type_): _description_
        token_tweets (_type_): _description_
        inverted_index (_type_, optional): _description_. Defaults to None.
    """

    # Filter the documents if any filtered method specified
    candidate_docs = filter(query, documents) if filter is not None else set(doc_id for doc_id in documents.keys())

    # Dictionary mapping from doc_id to the vectorized document (only containing the dimensions related to the words specified in the query)
    vectorized_docs = defaultdict(lambda: [0] * len(query))
    # Array containing the vectorized query
    vectorized_query = [0] * len(query)

    
    query_terms_count = Counter(query)

    # TAKE INTO ACCOUNT THAT THE TERM MIGHT NOT EXIST IN THE INDEX
    # Iterate over each term of the query, without repeating terms (i.e for each distinct element of the query)
    for index, term in enumerate(query):
        vectorized_query[index] = query_terms_count[term] / len(query) * idf[term] 
        
        # For a document to be considered it has to be a candidate document and have the corresponding term
        for doc in (candidate_docs & inverted_index[term]):
            doc_norm = la.norm(list(Counter(documents[doc]).values())) 
            vectorized_docs[doc][index] = tf[doc][term] / len(documents[doc]) * idf[term] 


    # Compute the cosine simmilary between each document and the input query.
    doc_scores = [(doc, np.dot(vectorized_doc, vectorized_query)) for doc, vectorized_doc in vectorized_docs.items()]

    # Sort the documents by score
    doc_scores.sort(reverse=True, key=lambda doc_score:doc_score[1])

    return doc_scores