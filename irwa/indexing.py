from collections import defaultdict

def create_inverted_index(token_tweets):
    
    inverted_index = defaultdict(set)
    
    # Iterate over each document
    for doc_id, tokens in token_tweets.items():
        # For each token in the document
        for token in tokens:
            # Append the document ID to the token's set
            inverted_index[token].add(doc_id)
    
    return inverted_index