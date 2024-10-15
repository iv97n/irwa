class Tweet:
    def __init__(self, url, date, content, rendered_content, tweet_id, user, outlinks, tcooutlinks, reply_count, 
                 retweet_count, like_count, quote_count, conversation_id, lang, source, source_url, 
                 source_label, media, retweeted_tweet=None, quoted_tweet=None, mentioned_users=None):
        self._url = url
        self._date = date
        self._content = content
        self._rendered_content = rendered_content
        self._tweet_id = tweet_id
        self._user = user  # User object
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
        self._mentioned_users = mentioned_users if mentioned_users else []  # List of User objects

    # Getters
    def get_url(self):
        return self._url

    def get_date(self):
        return self._date

    def get_content(self):
        return self._content

    def get_rendered_content(self):
        return self._rendered_content

    def get_tweet_id(self):
        return self._tweet_id

    def get_user(self):
        return self._user

    def get_outlinks(self):
        return self._outlinks

    def get_tcooutlinks(self):
        return self._tcooutlinks

    def get_reply_count(self):
        return self._reply_count

    def get_retweet_count(self):
        return self._retweet_count

    def get_like_count(self):
        return self._like_count

    def get_quote_count(self):
        return self._quote_count

    def get_conversation_id(self):
        return self._conversation_id

    def get_lang(self):
        return self._lang

    def get_source(self):
        return self._source

    def get_source_url(self):
        return self._source_url

    def get_source_label(self):
        return self._source_label

    def get_media(self):
        return self._media

    def get_retweeted_tweet(self):
        return self._retweeted_tweet

    def get_quoted_tweet(self):
        return self._quoted_tweet

    def get_mentioned_users(self):
        return self._mentioned_users

    # Setters
    def set_url(self, url):
        self._url = url

    def set_date(self, date):
        self._date = date

    def set_content(self, content):
        self._content = content

    def set_rendered_content(self, rendered_content):
        self._rendered_content = rendered_content

    def set_tweet_id(self, tweet_id):
        self._tweet_id = tweet_id

    def set_user(self, user):
        self._user = user

    def set_outlinks(self, outlinks):
        self._outlinks = outlinks

    def set_tcooutlinks(self, tcooutlinks):
        self._tcooutlinks = tcooutlinks

    def set_reply_count(self, reply_count):
        self._reply_count = reply_count

    def set_retweet_count(self, retweet_count):
        self._retweet_count = retweet_count

    def set_like_count(self, like_count):
        self._like_count = like_count

    def set_quote_count(self, quote_count):
        self._quote_count = quote_count

    def set_conversation_id(self, conversation_id):
        self._conversation_id = conversation_id

    def set_lang(self, lang):
        self._lang = lang

    def set_source(self, source):
        self._source = source

    def set_source_url(self, source_url):
        self._source_url = source_url

    def set_source_label(self, source_label):
        self._source_label = source_label

    def set_media(self, media):
        self._media = media

    def set_retweeted_tweet(self, retweeted_tweet):
        self._retweeted_tweet = retweeted_tweet

    def set_quoted_tweet(self, quoted_tweet):
        self._quoted_tweet = quoted_tweet

    def set_mentioned_users(self, mentioned_users):
        self._mentioned_users = mentioned_users

    # Add a mentioned user
    def add_mentioned_user(self, user):
        self._mentioned_users.append(user)
