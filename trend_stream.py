from pytz import timezone
from dateutil import parser
# from datetime import datetime
from twitter import Twitter, TwitterStream, OAuth
from _thread import get_ident
from threading import Timer

import os
from os.path import join, dirname
from dotenv import load_dotenv
from ElastincsearchProvider import ElastincsearchProvider

# 環境変数の読み込み
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OAUTH_INFO = dict(
    token=os.environ.get("ACCESS_TOKEN"),
    token_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
    consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET")
)

STREAM_INFO = dict(
    timeout=600,
    block=False,
    heartbeat_timeout=600
)

JST = timezone('Asia/Tokyo')
WOEID_JP = 23424856


class TwitterTrendStream():
    def __init__(self):
        self.__current_trend_ident = None
        self.__oauth = OAuth(**OAUTH_INFO)
        self.__es = ElastincsearchProvider()

    def __fetch_trends(self, twitter):
        response = twitter.trends.place(_id=WOEID_JP)
        return [trend["name"] for trend in response[0]["trends"]]

    def __fetch_filter_stream(self, twitter_stream, track_list):
        track = ",".join(track_list)
        return twitter_stream.statuses.filter(track=track)

    def run(self):
        print('run...')
        self.__current_trend_ident = get_ident()  # 今動作しているスレッドIDをセット
        Timer(300, self.run).start()

        twitter = Twitter(auth=self.__oauth)
        twitter_stream = TwitterStream(auth=self.__oauth, **STREAM_INFO)

        trend_lsit = self.__fetch_trends(twitter)
        tweet_iter = self.__fetch_filter_stream(twitter_stream, trend_lsit)

        for tweet in tweet_iter:
            if "limit" in tweet:
                continue

            if self.__current_trend_ident != get_ident():
                return True

            for trend in trend_lsit:
                if trend in tweet['text']:
                    doc = {
                        'track': trend,
                        'text': tweet['text'],
                        'created_at': str(parser.parse(tweet['created_at']).astimezone(JST).isoformat())
                    }
                    self.__es.set(body=doc)


if __name__ == '__main__':
    TwitterTrendStream().run()
