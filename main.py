from w2v import W2V
from news import News
from clustering import Clustering
from pprint import pprint

print("Main")
w2vobj = W2V()
news = News()
articles = news.get_articles()
w2vobj.train()
article_vecs = [w2vobj.get_sentence_vector(article['cleaned_title']) for article in articles]
clustering = Clustering(article_vecs)
zeroes_closest_indices = clustering.get_neighbors_vector(article_vecs[0])
print("The ten closest articles to: '" + articles[0]['raw_title'] + "' are...")
for index, distance in zip(zeroes_closest_indices[0], zeroes_closest_indices[1]):
    print articles[index]['raw_title'] + "\n\tNews Source: " + articles[index]['source'] \
          + "\n\theadline cleaned: " + articles[index]['cleaned_title'] + "\n\tDistance: " + str(distance) + "\n"
# Demo stuff here
# w2vobj.about()
