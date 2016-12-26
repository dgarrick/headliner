from w2v import W2V
from news import News
from clustering import Clustering
import json
import utilities
import sys
import redis
import os
import tsne
import numpy

def get_config():
    with open('src/resources/config.json') as config:
        return json.load(config)

def get_args():
    flags_defs = {
        '-input': '../resources/rsstraining',
        '-train': '',
        '-k': '30',
        '-cluster': 'agg',
        '-prune': 'true',
        '-limit': '3'
    }
    if len(sys.argv) == 1:
        print('no flags found, continuing with properties from resources/config.json')
        print('use -input to specify input data, -train to specify training data, -cluster for clustering method (\'agg\' or \'ann\'),  \
               -k to specify a number of dimensions, -prune followed by \'true\' to prune clusters and -limit to specify \
                a cluster threshold (e.g., 2)')
        return get_config()
    for i, arg in enumerate(sys.argv):
        if arg in flags_defs:
            if i+1 >= len(sys.argv):
                print("missing argument following flag: "+arg)
            else:
                print(sys.argv[i+1])
                flags_defs[arg] = sys.argv[i+1]
    return flags_defs

def dump_clusters():

    args = get_args()
    if args['-train'] == '':
        args['-train'] = 'src/resources/output' + args['-k']
    w2vobj = W2V(args['-input'], args['-train'], args['-k'])

    news = News()
    articles = news.get_articles()
    w2vobj.train()
    #article_vecs = [w2vobj.get_sentence_vector_avg(article['cleaned_title']) for article in articles]
    article_vecs = [w2vobj.get_sentence_vector_newtonian(article['cleaned_title']) for article in articles]
    cluster_obj = Clustering(article_vecs)
    r_conn = redis.from_url(os.getenv('REDIS_URL',"redis://localhost:6379/"))

    if args['-cluster'] == 'agg':
        if args['-prune'] == 'true' or args['-prune'] == 'True':
            utilities.redis_kmeans_clusters(cluster_obj, articles, True, int(args['-limit']), r_conn)
            print("redis dump complete")
        else:
            utilities.redis_kmeans_clusters(cluster_obj, articles, False, int(args['-limit']), r_conn)
            print("redis dump complete")
    else:
        #TODO dump to redis
        utilties.print_ann_clusters(cluster_obj, articles)

dump_clusters()
