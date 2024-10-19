import json
import pandas as pd
import nltk
import re
try:
    nltk.data.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from .models import Tweet


# Function to load the JSON file
def load_tweets_from_json(file_path):
    tweets = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                tweet = json.loads(line.strip())  # Load each line as a JSON object
                tweets.append(tweet)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e} - Line: {line.strip()}")
    return tweets


# Function to create a Tweet object from JSON data
def create_tweet(tweet_data):
    
    # Handle retweeted and quoted tweets if they exist
    retweeted_tweet = create_tweet(tweet_data['retweetedTweet']) if tweet_data.get('retweetedTweet') else None
    quoted_tweet = create_tweet(tweet_data['quotedTweet']) if tweet_data.get('quotedTweet') else None

    return Tweet(
        url=tweet_data.get('url', ''),
        date=tweet_data.get('date', ''),
        content=tweet_data.get('content', ''),
        rendered_content=tweet_data.get('renderedContent', ''),
        tweet_id=tweet_data.get('id', ''),
        user=tweet_data.get('user', ''),
        outlinks=tweet_data.get('outlinks', []),
        tcooutlinks=tweet_data.get('tcooutlinks', []),
        reply_count=tweet_data.get('replyCount', 0),
        retweet_count=tweet_data.get('retweetCount', 0),
        like_count=tweet_data.get('likeCount', 0),
        quote_count=tweet_data.get('quoteCount', 0),
        conversation_id=tweet_data.get('conversationId', ''),
        lang=tweet_data.get('lang', ''),
        source=tweet_data.get('source', ''),
        source_url=tweet_data.get('sourceUrl', ''),
        source_label=tweet_data.get('sourceLabel', ''),
        media=tweet_data.get('media', []),
        retweeted_tweet=retweeted_tweet,  # Assign retweeted tweet object (if any)
        quoted_tweet=quoted_tweet,  # Assign quoted tweet object (if any)
        mentioned_users=tweet_data.get('mentionedUsers', ''),
    )


# Function to load all tweets
def load_all_tweets(file_path):
    tweets_data = load_tweets_from_json(file_path)
    if tweets_data is None:
        print("No tweets loaded from the file.")
        return []
    return [create_tweet(tweet) for tweet in tweets_data]


# Auxiliary function that does text preprocessing
def build_terms(line): 
    """
    Argument:
    line -- string (tweet text) to be preprocessed

    Returns:
    A list of tokens corresponding to the input text after preprocessing.
    """
    
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


# Function to preprocesses tweets and maps them to a doc_id
def create_tokenized_dictionary(tweets, csv_file_path):
    """    
    Create a dictionary that maps document IDs to the tokenized content of tweets.
    
    This function processes a list of tweet objects and a CSV file containing 
    mappings of document IDs to tweet IDs. It tokenizes the content of tweets 
    based on the provided mapping and stores the results in a dictionary.
    
    Arguments:
    tweets -- a list of tweet objects, where each tweet object has '_tweet_id' and '_content' attributes
    csv_file_path -- path to the CSV file containing 'docId' and 'id' columns, where 'id' corresponds to tweet_id

    Returns:
    tokenized_dict -- a dictionary with doc_ids as keys and tokenized tweet content as values
    """
    # Load the mapping of doc_id to tweet_id from the CSV file
    tweet_mapping = pd.read_csv(csv_file_path)

    # Create tokenized dictionary with doc_id as key
    tokenized_dict = {}
    for _, row in tweet_mapping.iterrows():
        doc_id = row['docId']
        tweet_id = row['id']
        
        # Find the corresponding tweet by tweet_id
        for tweet in tweets:
            if tweet._tweet_id == tweet_id:
                tokenized_dict[doc_id] = build_terms(tweet._content)
                break  # Stop searching after finding the tweet

    return tokenized_dict