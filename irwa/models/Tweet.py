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
    def parse_json_tweet(cls, json_tweet_data):
        # Handle retweeted and quoted tweets if they exist
        retweeted_tweet = cls.parse_tweet(json_tweet_data['retweetedTweet']) if json_tweet_data.get('retweetedTweet') else None
        quoted_tweet = cls.parse_tweet(json_tweet_data['quotedTweet']) if json_tweet_data.get('quotedTweet') else None

        return cls(
            url=json_tweet_data.get('url', ''),
            date=json_tweet_data.get('date', ''),
            content=json_tweet_data.get('content', ''),
            rendered_content=json_tweet_data.get('renderedContent', ''),
            tweet_id=json_tweet_data.get('id', ''),
            user=json_tweet_data.get('user', ''),
            outlinks=json_tweet_data.get('outlinks', []),
            tcooutlinks=json_tweet_data.get('tcooutlinks', []),
            reply_count=json_tweet_data.get('replyCount', 0),
            retweet_count=json_tweet_data.get('retweetCount', 0),
            like_count=json_tweet_data.get('likeCount', 0),
            quote_count=json_tweet_data.get('quoteCount', 0),
            conversation_id=json_tweet_data.get('conversationId', ''),
            lang=json_tweet_data.get('lang', ''),
            source=json_tweet_data.get('source', ''),
            source_url=json_tweet_data.get('sourceUrl', ''),
            source_label=json_tweet_data.get('sourceLabel', ''),
            media=json_tweet_data.get('media', []),
            retweeted_tweet=retweeted_tweet,
            quoted_tweet=quoted_tweet,
            mentioned_users=json_tweet_data.get('mentionedUsers', ''),
        )
