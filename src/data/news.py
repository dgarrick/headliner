import json
from timeit import default_timer as timer
import feedparser
from nltk.corpus import stopwords
from multiprocessing.dummy import Pool

from utilities import strip_punctuation


class News:

    def __init__(self):
        self.articles = []
        self.stopwords = stopwords.words("english")

    def get_feed(self, feed):
        start = timer()
        parsed_feed = feedparser.parse(feed['url'])
        end = timer()
        print(str(len(parsed_feed.entries)) + " Articles from '" + feed['name'] +
              "' in " + str((end - start)) + " seconds")
        for ent in parsed_feed.entries:
            sanitized_title = strip_punctuation(ent.title)
            cleaned_title = [word for word in sanitized_title.split() if word not in self.stopwords]
            if len(cleaned_title) == 0:
                print "Found entry whose title is all stopwords: "+ent.title+" from: "+feed['name']
                return
            """python lists are threadsafe. Their data is not. We are only adding to the list,
            not accessing or changing data, so this op is safe"""
            self.articles.append({'raw_title': ent.title,
                                  'cleaned_title': ' '.join(cleaned_title),
                                  'source': feed['name'],
                                  'link': ent.link})

    def get_articles(self):
        with open('src/resources/feeds.json') as feeds_file:
            feeds = json.load(feeds_file)
        for feed in feeds['feeds']:
            self.get_feed(feed)
        return self.articles
