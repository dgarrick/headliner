import json
from timeit import default_timer as timer
import feedparser
from nltk.corpus import stopwords

from utilities import strip_punctuation


class News:

    def __init__(self):
        self.articles = []
        self.stopwords = stopwords.words("english")

    def get_articles(self):
        with open('resources/feeds.json') as feeds_file:
            feeds = json.load(feeds_file)

        for feed in feeds['feeds']:
            start = timer()
            parsed_feed = feedparser.parse(feed['url'])
            end = timer()
            print(str(len(parsed_feed.entries)) + " Articles from '" + feed['name'] +
                  "' in " + str((end-start)) + " seconds")
            for ent in parsed_feed.entries:
                sanitized_title = strip_punctuation(ent.title)
                self.articles.append({'raw_title': ent.title,
                                      'cleaned_title': ' '.join(
                                          [word for word in sanitized_title.split() if word not in self.stopwords]),
                                      'source': feed['name'],
                                      'link': ent.link})
        return self.articles
