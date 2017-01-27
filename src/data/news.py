import json
from timeit import default_timer as timer
import feedparser
from nltk.corpus import stopwords
from multiprocessing.dummy import Pool
import re

from utilities import strip_punctuation


class News:

    def __init__(self):
        self.articles = []
        self.title_links = set()
        self.stopwords = stopwords.words("english")

    def get_feed(self, feed):
        start = timer()
        parsed_feed = feedparser.parse(feed['url'])
        end = timer()
        print(str(len(parsed_feed.entries)) + " Articles from '" + feed['name'] +
              "' in " + str((end - start)) + " seconds")
        duplicates_count = 0
        for ent in parsed_feed.entries:
            sanitized_title = strip_punctuation(ent.title)
            cleaned_title = [word.lower() for word in re.split(" | - ", sanitized_title) if word not in self.stopwords]
            if len(cleaned_title) == 0:
                print "Found entry whose title is all stopwords: "+ent.title+" from: "+feed['name']
                return
            if (ent.title, ent.link) not in self.title_links:
                self.title_links.add((ent.title, ent.link))
                self.articles.append({'raw_title': ent.title,
                                      'cleaned_title': ' '.join(cleaned_title),
                                      'source': feed['name'],
                                      'link': ent.link})
            else:
                duplicates_count += 1
        if duplicates_count > 0:
            print "Filtered out " + str(duplicates_count) + " duplicate articles"

    def get_articles(self):
        with open('src/resources/feeds.json') as feeds_file:
            feeds = json.load(feeds_file)
        for feed in feeds['feeds']:
            self.get_feed(feed)
        return self.articles
