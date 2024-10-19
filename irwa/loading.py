import json
from .models import Tweet


# Function to load the JSON file
def load_tweets_from_json(file_path):
    """Function to load the tweets from the json file into a dictionary of key: tweet id, value: tweet object

    Args:
        file_path (string): Path to the json file

    Returns:
        Dict[int, Tweet]: Dictionary mapping tweet ids to tweet objects. It allows fast retrieval of tweets when indexing by id.
    """
    tweets = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # Load the json string into a dictionary
                dict_tweet = json.loads(line.strip()) 
                # Create a new instance of the Tweet class and add it to the dictionary of tweets
                tweets[dict_tweet['id']] = Tweet.dict_tweet(dict_tweet)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON format: {e} - Line: {line.strip()}")
    return tweets
