import feedparser
import json
from nltk.corpus import stopwords
from utilities import strip_punctuation


class News:

    def __init__(self):
        self.articles = []
        self.stopwords = stopwords.words("english")

    def get_articles(self):
        with open('feeds.json') as feeds_file:
            feeds = json.load(feeds_file)

        for feed in feeds['feeds']:
            parsed_feed = feedparser.parse(feed['url'])

            for ent in parsed_feed.entries:
                sanitized_title = strip_punctuation(ent.title)
                self.articles.append({'raw_title': ent.title,
                                      'cleaned_title': ' '.join(
                                          [word for word in sanitized_title.split() if word not in self.stopwords]),
                                      'link': ent.link})
        return self.articles
