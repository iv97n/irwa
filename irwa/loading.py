import json

from .models.User import User
from .models.Tweet import Tweet
# Assuming Tweet and User classes are already defined as above


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


# Function to create a User object from JSON data
def create_user(user_data):
    return User(
        username=user_data['username'],
        displayname=user_data['displayname'],
        user_id=user_data['id'],
        description=user_data['description'],
        raw_description=user_data['rawDescription'],
        description_urls=user_data.get('descriptionUrls', []),
        verified=user_data['verified'],
        created=user_data['created'],
        followers_count=user_data['followersCount'],
        friends_count=user_data['friendsCount'],
        statuses_count=user_data['statusesCount'],
        favourites_count=user_data['favouritesCount'],
        listed_count=user_data['listedCount'],
        media_count=user_data['mediaCount'],
        location=user_data.get('location', ''),
        protected=user_data['protected'],
        link_url=user_data.get('linkUrl', ''),
        link_tco_url=user_data.get('linkTcourl', ''),
        profile_image_url=user_data['profileImageUrl'],
        profile_banner_url=user_data.get('profileBannerUrl', ''),
        url=user_data.get('url', '')
    )

# Function to create a Tweet object from JSON data
def create_tweet(tweet_data):
    # Create User object
    user = create_user(tweet_data['user']) if tweet_data.get('user') else None  # Handle missing user

    # Handle retweeted and quoted tweets if they exist
    retweeted_tweet = create_tweet(tweet_data['retweetedTweet']) if tweet_data.get('retweetedTweet') else None
    quoted_tweet = create_tweet(tweet_data['quotedTweet']) if tweet_data.get('quotedTweet') else None

    # Handle mentioned users, ensuring it's an empty list if None

    mentioned_users_data = tweet_data.get('mentionedUsers', [])
    if mentioned_users_data != None:
        mentioned_users = [create_user(user) for user in mentioned_users_data if user]  # Create User objects for mentioned users
    else:
        mentioned_users = None
    return Tweet(
        url=tweet_data.get('url', ''),
        date=tweet_data.get('date', ''),
        content=tweet_data.get('content', ''),
        rendered_content=tweet_data.get('renderedContent', ''),
        tweet_id=tweet_data.get('id', ''),
        user=user,  # Assign the User object
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
        mentioned_users=mentioned_users  # List of mentioned users
    )




# Function to load all tweets
def load_all_tweets(file_path):
    tweets_data = load_tweets_from_json(file_path)
    if tweets_data is None:
        print("No tweets loaded from the file.")
        return []
    return [create_tweet(tweet) for tweet in tweets_data]

