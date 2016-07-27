import json
from timeit import default_timer as timer
import feedparser
from nltk.corpus import stopwords
import Queue
from multiprocessing.dummy import Pool

from utilities import strip_punctuation


class News:

    def __init__(self):
        self.articles = []
        self.article_queue = Queue.Queue()
        self.stopwords = stopwords.words("english")

    def get_feed(self, feed):
        start = timer()
        parsed_feed = feedparser.parse(feed['url'])
        end = timer()
        print(str(len(parsed_feed.entries)) + " Articles from '" + feed['name'] +
              "' in " + str((end - start)) + " seconds")
        for ent in parsed_feed.entries:
            sanitized_title = strip_punctuation(ent.title)
            self.article_queue.put({'raw_title': ent.title,
                                  'cleaned_title': ' '.join(
                                      [word for word in sanitized_title.split() if word not in self.stopwords]),
                                  'source': feed['name'],
                                  'link': ent.link})

    def get_articles(self):
        with open('../resources/feeds.json') as feeds_file:
            feeds = json.load(feeds_file)
        pool = Pool(len(feeds))
        pool.map(self.get_feed, feeds['feeds'])

        while not self.article_queue.empty:
            self.articles.append(self.article_queue.get())
        return self.articles
