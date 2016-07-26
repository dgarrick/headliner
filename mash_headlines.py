import feedparser
import json
import uuid
from nltk.corpus import stopwords
from src.utilities import strip_punctuation

# Standalone script that grabs all our headlines and puts the cleaned headlines into a space-separated file

output_fname = str(uuid.uuid4()) + ".txt"
articles = []
stopword = stopwords.words("english")

with open("resources/feeds.json") as feeds_file:
    feeds = json.load(feeds_file)

target = open(output_fname, 'w')
for feed in feeds['feeds']:
    parsed_feed = feedparser.parse(feed['url'])
    for ent in parsed_feed.entries:
        sanitized_title = strip_punctuation(ent.title)
        cleaned_title = ' '.join([word for word in sanitized_title.split() if word not in stopword])
        target.write(cleaned_title)
        target.write(" ")
    print feed['name'] + " is done"

print("Done, your data is at " + output_fname)
target.close()