import pandas as pd
import nltk
import re
try:
    nltk.data.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


def build_terms(line):
    """Prepocessing and tokenization of the tweets

    Args:
        line (str): tweet content

    Returns:
        List[str]: tokenized tweet content list
    """
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    symbols_to_remove = '!"$%&\'()*+,-/:;<=>?@[\\]^_`{|}~.'  # Does not include hashtag for future purposes
    url_pattern = re.compile(r'http\S+|www\S+')

    line = line.lower()  # Convert letters to lowercase
    
    urls = url_pattern.findall(line) # Find urls, save for latter and substitute with nothing
    line = url_pattern.sub('', line)

    line = line.translate(str.maketrans("", "", symbols_to_remove))  # Remove desired punctuation symbols
    line = line.split()  # Tokenize the text
    line = [word for word in line if word not in stop_words]  # Remove stopwords
    line = [stemmer.stem(word) for word in line]  # Perform stemming
    
    line.extend(urls)  # Add all found urls at the end
    
    return line


def create_tokenized_dictionary(tweets, csv_file_path):
    """Function to preprocesses tweets and maps them to a doc_id

    Args:
        tweets (Dict[id, Tweet]): dicitonary containing the mapping between tweet ids and tweet objects
        csv_file_path (str): path to the mapping csv

    Returns:
        Dict[str, List[str]]: dicitonary mapping from document id to the tokenized tweet content
    """
    # Load the mapping of doc_id to tweet_id from the CSV file
    tweet_mapping = pd.read_csv(csv_file_path)

    # Create tokenized dictionary with doc_id as key
    tokenized_dict = {}
    docid_to_tweetid = {}

    for _, row in tweet_mapping.iterrows():
        doc_id = row['docId']
        tweet_id = row['id']
        if tweet_id in tweets:
            tokenized_dict[doc_id] = build_terms(tweets[tweet_id].get_content())
            docid_to_tweetid[doc_id] = tweet_id

    return docid_to_tweetid, tokenized_dict
