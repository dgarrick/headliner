import feedparser
import json
from utilities import strip_punctuation


class News:

    def __init__(self):
        self.articles = []

    def get_articles(self):
        with open('feeds.json') as feeds_file:
            feeds = json.load(feeds_file)

        for feed in feeds['feeds']:
            parsed_feed = feedparser.parse(feed['url'])

            for ent in parsed_feed.entries:
                self.articles.append({'raw_title': ent.title,
                                      'sanitized_title': strip_punctuation(ent.title),
                                      'link': ent.link})
        # TODO remove "stop words" (blacklist) before sending back
        return self.articles
