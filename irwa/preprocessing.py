import pandas as pd
import nltk
import re
try:
    nltk.data.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


# Auxiliary function that does text preprocessing
def build_terms(line): 
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    symbols_to_remove = '!"$%&\'()*+,-/:;<=>?@[\\]^_`{|}~.' #Does not include hashtag for future purposes
    url_pattern = re.compile(r'http\S+|www\S+')


    line = line.lower()  # Convert letters to lowercase
    
    urls = url_pattern.findall(line) # Find urls, save for latter and substitute with nothing
    line = url_pattern.sub('', line)

    line = line.translate(str.maketrans("", "", symbols_to_remove)) #Remove desired punctuation symbols
    line = line.split()  # Tokenize the text
    line = [word for word in line if word not in stop_words]  # Remove stopwords
    line = [stemmer.stem(word) for word in line]  # Perform stemming
    
    line.extend(urls) #Add all found urls at the end
    
    return line


def create_tokenized_dictionary(tweets, csv_file_path):
    """Function to preprocesses tweets and maps them to a doc_id

    Args:
        tweets (_type_): _description_
        csv_file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Load the mapping of doc_id to tweet_id from the CSV file
    tweet_mapping = pd.read_csv(csv_file_path)

    # Create tokenized dictionary with doc_id as key
    tokenized_dict = {}
    for _, row in tweet_mapping.iterrows():
        doc_id = row['docId']
        tweet_id = row['id']
        if tweet_id in tweets:
            tokenized_dict[doc_id] = build_terms(tweets[tweet_id]._content)

    return tokenized_dict