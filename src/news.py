import json
from timeit import default_timer as timer
import feedparser
from nltk.corpus import stopwords
import Queue
import threading

from utilities import strip_punctuation


class News:

    def __init__(self):
        self.articles = []
        self.article_queue = Queue.Queue()
        self.stopwords = stopwords.words("english")

    def get_feed(self, feed):
        print feed

    def get_articles(self):
        with open('resources/feeds.json') as feeds_file:
            feeds = json.load(feeds_file)

        for feed in feeds['feeds']:
            print feed
            t = threading.Thread(target=self.get_feed, args="hi")
            t.daemon = True
            t.start()

        while self.article_queue.not_empty:
            self.articles.append(self.article_queue.get())
        return self.articles
