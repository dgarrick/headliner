import numpy as np
import json
import re

def json_kmeans_clusters(clustering, articles, should_prune, limit):
    clustering.cluster(prune_clusters=should_prune, limit=limit)
    clustered_vecs = clustering.cluster_to_vec_index
    json_output = {}
    json_clusters = {}
    for i in xrange(len(clustered_vecs)):
        if i in clustered_vecs:
            json_cluster = {}
            cluster = clustered_vecs[i]
            for index in cluster:
                json_article = {}
                json_article['raw'] = articles[index]['raw_title']
                json_article['source'] = articles[index]['source']
                json_article['link'] = articles[index]['link']
                json_cluster[str(index)] = json_article
            json_clusters[str(i)] = json_cluster
    json_output['clusters'] = json_clusters
    with open('src/resources/clusters.json', 'w') as outfile:
        json.dump(json_output, outfile)



def print_ann_clusters(clustering, articles):
    zeroes_closest_indices = clustering.get_neighbors_vector(article_vecs[0])
    print("The ten closest articles to: '" + articles[0]['raw_title'] + "' are...")
    for index, distance in zip(zeroes_closest_indices[0], zeroes_closest_indices[1]):
        print articles[index]['raw_title'] + "\n\tNews Source: " + articles[index]['source'] \
              + "\n\theadline cleaned: " + articles[index]['cleaned_title'] + "\n\tDistance: " + str(distance) + "\n"

def print_random_kmeans_cluster(clustering, articles, should_prune, limit):
  clustering.cluster(prune_clusters=should_prune, limit=limit)
  clustered_vecs = clustering.cluster_to_vec_index
  i = random.randint(0, len(clustered_vecs))
  if i in clustered_vecs:
      cluster = clustered_vecs[i]
      print(cluster)
      print("Cluster " + str(i))
      for index in cluster:
          print articles[index]['raw_title'] + "\n\tNews Source: " + articles[index]['source'] \
                + "\n\theadline cleaned: " + articles[index]['cleaned_title']


def average_vector(vecs, k):
    num_vecs = len(vecs)
    if num_vecs == 0:
        return np.zeros(k, dtype=np.float)
    vec_length = len(vecs[0])
    avg_vec = np.zeros(vec_length, dtype=np.float)
    # Sum all components
    for vec in vecs:
        for index, value in enumerate(vec):
            avg_vec[index] += vec[index]
    # Divide by number of vecs seen
    for index in range(0, len(avg_vec)):
        avg_vec[index] /= num_vecs
    return avg_vec


def strip_punctuation(sentence):
    return re.sub(r'([^\s\w]|_)+', '', sentence).lower()
