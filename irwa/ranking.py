from collections import defaultdict
import math

def tf_idf(inverted_index, query, token_tweets):
    N = len(token_tweets)                               # Total number of documents
    scores = defaultdict(float)                         # Store scores for each document

    # For each term in the query
    for term in query:
        if term in inverted_index:
            df = len(inverted_index[term])              # Document Frequency of the term
            idf = math.log(N / df)                      # Inverse Document Frequency
            for doc_id in inverted_index[term]:
                tf = token_tweets[doc_id].count(term)   # Term Frequency in the document
                scores[doc_id] += tf * idf              # Calculate and accumulate tf-idf score

    return dict(scores)

def sort_scores_tf_idf(scores, n=10):
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    # Display the top n results
    print(f"Top {n} Results:")
    for doc_id, score in sorted_scores[:n]:
        print(f"Document {doc_id}: {score}")