import nltk
nltk.download('stopwords')
from collections import defaultdict
from array import array
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords




def build_terms(line):
    """
    Argument:
    line -- string (tweet text) to be preprocessed

    Returns:
    A list of tokens corresponding to the input text after preprocessing.
    """
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    line = line.lower()  # Transform to lowercase
    line = line.split()  # Tokenize the text
    line = [word for word in line if word not in stop_words]  # Remove stopwords
    line = [stemmer.stem(word) for word in line]  # Perform stemming
    return line


def create_index(tweets):
    """
    Create an inverted index for the collection of Tweet objects.

    Argument:
    tweets -- list of Tweet objects

    Returns:
    index - inverted index (implemented through a Python dictionary) containing terms as keys
    and the corresponding list of tweet IDs where these keys appear (with positions).
    tweet_index - dictionary mapping tweet IDs to tweet content (for reference).
    """
    index = defaultdict(list)  # Inverted index
    tweet_index = {}  # Dictionary to map tweet IDs to tweet content

    for tweet in tweets:  # Loop through each Tweet object
        tweet_id = tweet._tweet_id  # Extract tweet ID
        content = tweet._content  # Get the tweet content
        terms = build_terms(content)  # Get preprocessed terms from tweet content
        tweet_index[tweet_id] = content  # Store tweet content in tweet_index

        # ===============================================================
        # Create the index for the current tweet
        # ===============================================================
        current_tweet_index = {}

        for position, term in enumerate(terms):  # Loop through all terms in the tweet
            try:
                # If the term is already in the index for the current tweet, append the position
                current_tweet_index[term][1].append(position)
            except:
                # Add the new term as a key, initialize the array of positions and add the position
                current_tweet_index[term] = [tweet_id, array('I', [position])]

        # Merge the current tweet index with the main index
        for term, posting in current_tweet_index.items():
            index[term].append(posting)  # Append the posting list for each term to the main index

    return index, tweet_index
"""
def create_index(tweets, tweet_document_ids_map):
    
    Argument:
    tweets -- list of Tweet objects
    tweet_document_ids_map -- dictionary mapping document IDs (e.g., doc_0) to tweet IDs

    Returns:
    index - inverted index (implemented through a Python dictionary) containing terms as keys
    and the corresponding list of document IDs where these keys appear (with positions).
    tweet_index - dictionary mapping document IDs to tweet content (for reference).
    


    index = defaultdict(list)  # Inverted index
    tweet_index = {}  # Dictionary to map document IDs to tweet content

    for doc_id, tweet_id in tweet_document_ids_map.items():
        # Find the tweet by its ID
        tweet = next((t for t in tweets if str(t._tweet_id) == str(tweet_id)), None)
        if not tweet:
            continue  # Skip if tweet is not found

        content = tweet._content  # Get the tweet content
        terms = build_terms(content)  # Get preprocessed terms from tweet content
        tweet_index[doc_id] = content  # Store tweet content in tweet_index using doc_id

        # ===============================================================
        # Create the index for the current tweet
        # ===============================================================
        current_tweet_index = {}

        for position, term in enumerate(terms):  # Loop through all terms in the tweet
            try:
                # If the term is already in the index for the current document, append the position
                current_tweet_index[term][1].append(position)
            except:
                # Add the new term as a key, initialize the array of positions and add the position
                current_tweet_index[term] = [doc_id, array('I', [position])]

        # Merge the current tweet index with the main index
        for term, posting in current_tweet_index.items():
            index[term].append(posting)  # Append the posting list for each term to the main index

    return index, tweet_index
    """

