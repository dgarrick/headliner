from w2v import W2V
from news import News
from clustering import Clustering
import utilities
import sys

def get_args():
    flags_defs = {
        '-i': '../resources/bigsample',
        '-t': '',
        '-k': '30',
        '-c': 'kmeans',
        '-p': 'false',
        '-l': '20'
    }
    if len(sys.argv) == 1:
        print('no flags found, continuing with defaults')
        print('use -i to specify input data, -t to specify output, -c for clustering method (\'kmeans\' or \'ann\'),  \
               -k to specify a number of dimensions, -p followed by \'true\' to prune clusters and -l to specify \
                a cluster threshold (e.g., 20)')
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
if args['-t'] == '':
    args['-t'] = 'src/resources/output' + args['-k']
w2vobj = W2V(args['-i'], args['-t'], args['-k'])
news = News()
articles = news.get_articles()
w2vobj.train()
article_vecs = [w2vobj.get_sentence_vector(article['cleaned_title']) for article in articles]
cluster_obj = Clustering(article_vecs)
if args['-c'] == 'kmeans':
    if args['-p'] == 'true' or args['-p'] == 'True':
        utilities.json_kmeans_clusters(cluster_obj, articles, True, int(args['-l']))
        print("json dump complete")
    else:
        utilities.json_kmeans_clusters(cluster_obj, articles, False, int(args['-l']))
        print("json dump complete")
else:
    #TODO save appropriate json
    utilties.print_ann_clusters(cluster_obj, articles)

# Demo stuff here
# w2vobj.about()
