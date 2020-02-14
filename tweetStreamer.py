import tweepy
import datetime as dt
from HealthTwitterAnalytics import credentials
import json



def clean(absolute_path, history_depth):
    'Function cleans master id list. New list only contains the last /history_depth/ runs.'
    with open(absolute_path, "r") as file:
        data = json.load(file)
        clean_list = data[-history_depth:]
    return clean_list


def get_recent_ids(absolute_path, history_depth):
    'Function returns list of recent ids to prevent duplicates.'
    'History depth determines how many runs back is relevant for duplicates'
    ids = []
    with open(absolute_path, "r") as file:
        data = json.load(file)
        list_of_id_lists = []
        if len(data) < history_depth:
            list_of_id_lists = data
        else:
            list_of_id_lists = data[-history_depth:]
        for id_list in list_of_id_lists:
            for id in id_list:
                ids.append(id)
    return ids


class TweetCollector:
    def __init__(self, word, tweet_amount):
        self.api = tweepy.API(authentication, wait_on_rate_limit=True)
        self.base_word = word
        self.search_word = word + " -filter:retweets"
        self.tweet_amount = tweet_amount

    def get_file_name(self):
        formatted_time = dt.datetime.now().strftime("%m-%d-%Y_%I-%M-%S_")
        return formatted_time + self.base_word.replace(" ", "") + ".json"

    def fetch(self):
        tweets = tweepy.Cursor(self.api.search, q=self.search_word,
                               tweet_mode="extended", lang="en", result_type="recent").items(self.tweet_amount)
        return tweets

    def update_id_list(self, id_list):
        with open(path_to_ids, "r") as file:
            data = json.load(file)
        data.append(id_list)
        with open(path_to_ids, "w") as output:
            json.dump(data, output, indent=4)

    def parse(self, tweets, file_name):
        tweet_list = {}
        ids = []
        for tweet in tweets:
            if tweet.id in recent_ids:
                continue
            ids.append(tweet.id)
            tweet_list[tweet.id] = tweet.full_text
        with open(file_name, "w+") as file:
            json.dump(tweet_list, file, indent=4)
        self.update_id_list(ids)

    def cache_tweets(self):
        file_name = self.get_file_name()
        tweets = self.fetch()
        self.parse(tweets, file_name)


if __name__ == "__main__":
    authentication = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_KEY_SECRET)
    authentication.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    path_to_ids = "list_of_ids.json"
    recent_ids = get_recent_ids(path_to_ids, 5)
    test = TweetCollector("sad", 100)
    test.cache_tweets()



