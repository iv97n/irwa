import json

class Tweet:
    def __init__(self, url, date, content, rendered_content, tweet_id, user, outlinks, tcooutlinks, reply_count, 
                 retweet_count, like_count, quote_count, conversation_id, lang, source, source_url, 
                 source_label, media, retweeted_tweet=None, quoted_tweet=None, mentioned_users=None):
        self._url = url
        self._date = date
        self._content = content
        self._rendered_content = rendered_content
        self._tweet_id = tweet_id
        self._user = user  # In the future can be implemented as a user object
        self._outlinks = outlinks
        self._tcooutlinks = tcooutlinks
        self._reply_count = reply_count
        self._retweet_count = retweet_count
        self._like_count = like_count
        self._quote_count = quote_count
        self._conversation_id = conversation_id
        self._lang = lang
        self._source = source
        self._source_url = source_url
        self._source_label = source_label
        self._media = media
        self._retweeted_tweet = retweeted_tweet  # Another Tweet object if this is a retweet
        self._quoted_tweet = quoted_tweet  # Another Tweet object if this is a quote
        self._mentioned_users = mentioned_users if mentioned_users else []  # In the future can be implemented as a list of User objects

    @classmethod
    def dict_tweet(cls, tweet_dict):
        """Alternative constructor for creating Tweet instances from a tweet dictionary

        Args:
            tweet_dict (Dict): Dictionary containing the tweet information

        Returns:
            Tweet: Tweet instance
        """
        # Handle retweeted and quoted tweets if they exist
        retweeted_tweet = cls.dict_tweet(tweet_dict['retweetedTweet']) if tweet_dict.get('retweetedTweet') else None
        quoted_tweet = cls.dict_tweet(tweet_dict['quotedTweet']) if tweet_dict.get('quotedTweet') else None

        return cls(
            url=tweet_dict.get('url', ''),
            date=tweet_dict.get('date', ''),
            content=tweet_dict.get('content', ''),
            rendered_content=tweet_dict.get('renderedContent', ''),
            tweet_id=tweet_dict.get('id', ''),
            user=tweet_dict.get('user', ''),
            outlinks=tweet_dict.get('outlinks', []),
            tcooutlinks=tweet_dict.get('tcooutlinks', []),
            reply_count=tweet_dict.get('replyCount', 0),
            retweet_count=tweet_dict.get('retweetCount', 0),
            like_count=tweet_dict.get('likeCount', 0),
            quote_count=tweet_dict.get('quoteCount', 0),
            conversation_id=tweet_dict.get('conversationId', ''),
            lang=tweet_dict.get('lang', ''),
            source=tweet_dict.get('source', ''),
            source_url=tweet_dict.get('sourceUrl', ''),
            source_label=tweet_dict.get('sourceLabel', ''),
            media=tweet_dict.get('media', []),
            retweeted_tweet=retweeted_tweet,
            quoted_tweet=quoted_tweet,
            mentioned_users=tweet_dict.get('mentionedUsers', ''),
        )

    def get_content(self):
        return self._content

