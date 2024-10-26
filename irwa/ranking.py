from collections import defaultdict
import math
import irwa.preprocessing as ipp

def tf_idf(inverted_index, query, token_tweets):
    N = len(token_tweets)                               # Total number of documents
    scores = defaultdict(float)                         # Store scores for each document
    query = ipp.build_terms(query)
    # For each term in the query
    for term in query:
        if term in inverted_index:
            df = len(inverted_index[term])              # Document Frequency of the term --> en cuántos documentos aparece palabra de la query
            idf = math.log(N / (1+df))                      # Inverse Document Frequency --> modificación por razones matemáticas del df
            
            for doc_id in inverted_index[term]:         # Para todos los documentos en los que aparece la palabra de la query
                tf = token_tweets[doc_id].count(term)   # Term Frequency in the document --> contar cuantas veces aparece por documento
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
