from w2v import W2V
from news import News
from clustering import Clustering
import sys


def get_args():
    flags_defs = {
        '-i': '../resources/bigsample',
        '-t': '../resources/output30',
        '-k': '30'
    }
    if len(sys.argv) == 1:
        print('no flags found, continuing with defaults')
        print('use -i to specify input data, -t to specify output, and -k to specify a number of dimensions')
        return flags_defs
    for i, arg in enumerate(sys.argv):
        if arg in flags_defs:
            if i+1 >= len(sys.argv):
                print("missing argument following flag: "+arg)
            else:
                flags_defs[arg] = sys.argv[i+1]
    return flags_defs

print("Main")
args = get_args()
w2vobj = W2V(args['-i'], args['-t'], args['-k'])
news = News()
articles = news.get_articles()
w2vobj.train()
article_vecs = [w2vobj.get_sentence_vector(article['cleaned_title']) for article in articles]

clustering = Clustering(article_vecs,10)
ranked_vecs = clustering.kmeans_cluster()
print("The top trending articles are: ")
for vec, score in ranked_vecs:
    index = clustering.get_vector_index(vec)[0]
    print articles[index]['raw_title'] + "\n\tNews Source: " + articles[index]['source'] \
          + "\n\theadline cleaned: " + articles[index]['cleaned_title']

"""vec, dist = ranked_vecs[0]
zeroes_closest_indices = clustering.get_neighbors_vector(vec)
index = zeroes_closest_indices[0][0]
print("The ten closest articles to: '" + articles[index]['raw_title'] + "' are...")
for index, distance in zip(zeroes_closest_indices[0], zeroes_closest_indices[1]):
    print articles[index]['raw_title'] + "\n\tNews Source: " + articles[index]['source'] \
          + "\n\theadline cleaned: " + articles[index]['cleaned_title'] + "\n\tDistance: " + str(distance) + "\n"
# Demo stuff here
# w2vobj.about()
"""

