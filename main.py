from w2v import W2V
from news import News
from pprint import pprint

print("Main")
w2vobj = W2V()
news = News()
articles = news.get_articles()
pprint(articles)
w2vobj.train()
article_vecs = [w2vobj.get_sentence_vector(article['cleaned_title']) for article in articles]
pprint(article_vecs)
# Demo stuff here
# w2vobj.about()

