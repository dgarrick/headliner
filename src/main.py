from w2v import W2V
from news import News
from clustering import Clustering
import sys


def print_kmeans_clusters(clustering):
    clustering.kmeans_cluster(rank_clusters=True)
    clustered_vecs = clustering.cluster_to_vec_index
    for i in xrange(clustering.num_clusters):
        cluster = clustered_vecs[i]
        print(cluster)
        print("Cluster " + str(i))
        for index in cluster:
            print articles[index]['raw_title'] + "\n\tNews Source: " + articles[index]['source'] \
                  + "\n\theadline cleaned: " + articles[index]['cleaned_title']


def print_ann_clusters(clustering):
    zeroes_closest_indices = clustering.get_neighbors_vector(article_vecs[0])
    print("The ten closest articles to: '" + articles[0]['raw_title'] + "' are...")
    for index, distance in zip(zeroes_closest_indices[0], zeroes_closest_indices[1]):
        print articles[index]['raw_title'] + "\n\tNews Source: " + articles[index]['source'] \
              + "\n\theadline cleaned: " + articles[index]['cleaned_title'] + "\n\tDistance: " + str(distance) + "\n"


def get_args():
    flags_defs = {
        '-i': '../resources/bigsample',
        '-t': '../resources/output30',
        '-k': '30',
        '-c': 'kmeans'
    }
    if len(sys.argv) == 1:
        print('no flags found, continuing with defaults')
        print('use -i to specify input data, -t to specify output, -c for clustering method (\'kmeans\' or \'ann\')  \
               and -k to specify a number of dimensions')
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
cluster_obj = Clustering(article_vecs)
if args['-c'] == 'kmeans':
    print_kmeans_clusters(cluster_obj)
else:
    print_ann_clusters(cluster_obj)

# Demo stuff here
# w2vobj.about()


