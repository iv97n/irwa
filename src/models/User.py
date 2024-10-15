class User:
    def __init__(self, username, displayname, user_id, description, raw_description, description_urls, verified, 
                 created, followers_count, friends_count, statuses_count, favourites_count, listed_count, 
                 media_count, location, protected, link_url, link_tco_url, profile_image_url, 
                 profile_banner_url, url):
        self._username = username
        self._displayname = displayname
        self._user_id = user_id
        self._description = description
        self._raw_description = raw_description
        self._description_urls = description_urls
        self._verified = verified
        self._created = created
        self._followers_count = followers_count
        self._friends_count = friends_count
        self._statuses_count = statuses_count
        self._favourites_count = favourites_count
        self._listed_count = listed_count
        self._media_count = media_count
        self._location = location
        self._protected = protected
        self._link_url = link_url
        self._link_tco_url = link_tco_url
        self._profile_image_url = profile_image_url
        self._profile_banner_url = profile_banner_url
        self._url = url

    # Getters
    def get_username(self):
        return self._username

    def get_displayname(self):
        return self._displayname

    def get_user_id(self):
        return self._user_id

    def get_description(self):
        return self._description

    def get_raw_description(self):
        return self._raw_description

    def get_description_urls(self):
        return self._description_urls

    def get_verified(self):
        return self._verified

    def get_created(self):
        return self._created

    def get_followers_count(self):
        return self._followers_count

    def get_friends_count(self):
        return self._friends_count

    def get_statuses_count(self):
        return self._statuses_count

    def get_favourites_count(self):
        return self._favourites_count

    def get_listed_count(self):
        return self._listed_count

    def get_media_count(self):
        return self._media_count

    def get_location(self):
        return self._location

    def get_protected(self):
        return self._protected

    def get_link_url(self):
        return self._link_url

    def get_link_tco_url(self):
        return self._link_tco_url

    def get_profile_image_url(self):
        return self._profile_image_url

    def get_profile_banner_url(self):
        return self._profile_banner_url

    def get_url(self):
        return self._url

    # Setters
    def set_username(self, username):
        self._username = username

    def set_displayname(self, displayname):
        self._displayname = displayname

    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_description(self, description):
        self._description = description

    def set_raw_description(self, raw_description):
        self._raw_description = raw_description

    def set_description_urls(self, description_urls):
        self._description_urls = description_urls

    def set_verified(self, verified):
        self._verified = verified

    def set_created(self, created):
        self._created = created

    def set_followers_count(self, followers_count):
        self._followers_count = followers_count

    def set_friends_count(self, friends_count):
        self._friends_count = friends_count

    def set_statuses_count(self, statuses_count):
        self._statuses_count = statuses_count

    def set_favourites_count(self, favourites_count):
        self._favourites_count = favourites_count

    def set_listed_count(self, listed_count):
        self._listed_count = listed_count

    def set_media_count(self, media_count):
        self._media_count = media_count

    def set_location(self, location):
        self._location = location

    def set_protected(self, protected):
        self._protected = protected

    def set_link_url(self, link_url):
        self._link_url = link_url

    def set_link_tco_url(self, link_tco_url):
        self._link_tco_url = link_tco_url

    def set_profile_image_url(self, profile_image_url):
        self._profile_image_url = profile_image_url

    def set_profile_banner_url(self, profile_banner_url):
        self._profile_banner_url = profile_banner_url

    def set_url(self, url):
        self._url = url
