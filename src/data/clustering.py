from annoy import AnnoyIndex
from sklearn.cluster import KMeans
import utilities
import numpy

class Clustering:

    def __init__(self, vecs, w2v):
        self.vec_length = len(vecs[0])
        self.vecs = vecs
        self.num_clusters = int(len(vecs)*.5)
        self.cluster_to_vec_index = {}
        self.labels = []
        self.w2v = w2v
        #self.cluster_func = AgglomerativeClustering(n_clusters=self.num_clusters, affinity="manhattan", linkage="complete")
        self.cluster_func = KMeans(n_clusters=self.num_clusters)
        self.annoy = AnnoyIndex(self.vec_length, metric='euclidean')
        for i, vec in enumerate(self.vecs):
            if vec is not None:
                self.annoy.add_item(i, vec)
        print("Built an index with " + str(self.annoy.get_n_items()) + " headlines")
        self.annoy_vocab = AnnoyIndex(self.vec_length, metric='angular')
        for i, word in enumerate(self.w2v.model.vectors):
            if word is not None:
                self.annoy_vocab.add_item(i, word)
        self.annoy.build(10)
        self.annoy_vocab.build(5)

    def get_neighbors_vector(self, vec):
        return self.annoy.get_nns_by_vector(vec, 10, include_distances=True)

    def get_cluster_label_idx(self, vec):
        return self.annoy_vocab.get_nns_by_vector(vec, 5, include_distances=False)

    def prune_clusters(self, limit):
        """Iterates through all clusters, deleting those that have few vectors"""
        for i in xrange(self.num_clusters):
            if len(self.cluster_to_vec_index[i]) < limit:
                del self.cluster_to_vec_index[i]

    def label_clusters(self, articles):
        cluster_index_to_label = {}
        for j in xrange(0, self.num_clusters):
            clust_vecs = []
            if j in self.cluster_to_vec_index:
                for k in self.cluster_to_vec_index[j]:
                    clust_vecs.append(self.vecs[k])
                    print(articles[k]["raw_title"])
                cluster_vec = utilities.average_vector(clust_vecs, self.vec_length)
                label_idx = self.get_cluster_label_idx(cluster_vec)
                print(label_idx)
                for idx in range(0,len(label_idx)):
                    print(self.w2v.model.vocab[label_idx[idx]])
                print("\n")
                #print(self.w2v.model.analogy(label, []))
                cluster_index_to_label[j] = label_idx[0]
        return cluster_index_to_label

    def cluster(self, limit=2, prune_clusters=False):
        vec_index_to_cluster = self.cluster_func.fit_predict(self.vecs)
        vec_indices = range(0, len(self.vecs))
        for j in xrange(0, self.num_clusters):
            self.cluster_to_vec_index[j] = []
        for i in xrange(0, len(vec_indices)):
            self.cluster_to_vec_index[vec_index_to_cluster[i]].append(vec_indices[i])
        if prune_clusters:
            self.prune_clusters(limit)
