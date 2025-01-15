import csv
from collections import Counter
from itertools import chain
import pandas as pd


def save_scores_to_csv(doc_scores, filename):
    """
    Save document scores to a CSV file.

    Args:
        doc_scores (list): A list of tuples where each tuple contains a document ID and its score.
        filename (str): The name of the CSV file to save the results to.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(["Document ID", "Score"])
        
        # Write document scores
        for doc_id, score in doc_scores:
            writer.writerow([doc_id, score])

    print(f"Results saved to {filename}")



def word_count(tweets, top_words, count_type='all'):
    """
    Counts the most common words in a collection of tokenized tweets.

    Parameters:
    tweets (dict): A dictionary where keys are tweet identifiers and values are lists of words in the tweets.
    top_words (int): The number of top most common words to retrieve.
    count_type (str): An optional parameter to filter the type of words to count. It can take the values 'all' (default), 'hashtags', or 'no_hashtags'.

    Returns:
    word_counts (Counter): A Counter object containing the word counts.
    most_common_words (list): A list of tuples representing the most common words and their counts.
    """
    all_words = list(chain.from_iterable(tweets.values()))

    if count_type == "hashtags":
        words_to_count = [word for word in all_words if word.startswith('#')]  
    elif count_type == "no_hashtags":
        words_to_count = [word for word in all_words if not word.startswith('#')] 
    else:
        words_to_count = all_words  

    word_counts= Counter(words_to_count)
    most_common_words = word_counts.most_common(top_words)
    return word_counts, most_common_words


def top_retweeted_tweets(tweets, csv_file_path, n=10):
    """
    Finds the top n most retweeted tweets.

    Parameters:
    tweets (dict): A dictionary where keys are tweet identifiers and values are tweet objects containing tweet details.
    n (int): The number of top retweeted tweets to retrieve. Default is 10.

    Returns:
    list: A list of tuples containing tweet IDs, retweet counts, and tweet content of the top retweeted tweets.
    """

    # Load the mapping of doc_id to tweet_id from the CSV file
    tweet_mapping = pd.read_csv(csv_file_path)

    # Create tokenized dictionary with doc_id as key
    tokenized_lst = []
    for _, row in tweet_mapping.iterrows():
        doc_id = row['docId']
        tweet_id = row['id']
        if tweet_id in tweets:
            tweet = tweets[tweet_id]
            tokenized_lst.append((tweet_id,tweet._retweet_count, tweet._content))

    ranked_tweets = sorted(tokenized_lst, key=lambda x: x[1], reverse=True)[:n]
    '''
    tweets = [tweet for _, tweet in tokenized_dict.items()]
    ranked_tweets = sorted(tweets, key=lambda tweet: tweet._retweet_count, reverse=True)
    top_retweets = [(tweet._tweet_id, tweet._retweet_count, tweet._content) for tweet in ranked_tweets[:n]]'''
    return ranked_tweets
