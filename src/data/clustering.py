from annoy import AnnoyIndex
from sklearn.cluster import AgglomerativeClustering
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
        self.cluster_func = AgglomerativeClustering(n_clusters=self.num_clusters, affinity="manhattan", linkage="complete")
        self.annoy = AnnoyIndex(self.vec_length, metric='euclidean')
        for i, vec in enumerate(self.vecs):
            if vec is not None:
                self.annoy.add_item(i, vec)
        print("Built an index with " + str(self.annoy.get_n_items()) + " headlines")
        self.annoy.build(10)

    def get_neighbors_vector(self, vec):
        return self.annoy.get_nns_by_vector(vec, 10, include_distances=True)

    def get_cluster_label_idx(self, vec):
        return self.annoy_vocab.get_nns_by_vector(vec, 5, include_distances=False)

    def prune_clusters(self, limit):
        """Iterates through all clusters, deleting those that have few vectors"""
        for i in xrange(self.num_clusters):
            if len(self.cluster_to_vec_index[i]) < limit:
                del self.cluster_to_vec_index[i]

    def get_most_freq_word(self, headline_vocab, headline_vocab_dict, label_idx):
        most_freq_word = headline_vocab[label_idx[0]]
        freq = headline_vocab_dict[most_freq_word]
        for idx in label_idx:
            if headline_vocab_dict[headline_vocab[idx]] > freq:
                most_freq_word = headline_vocab[idx]
                freq = headline_vocab_dict[headline_vocab[idx]]
        return most_freq_word

    def label_clusters(self, articles):
        cluster_index_to_label = {}
        for c in range(self.num_clusters):
            annoy_headline_vocab = AnnoyIndex(self.vec_length, metric='angular')
            headline_vocab = []
            headline_vocab_dict = {}
            clust_vecs = []
            if c in self.cluster_to_vec_index:
                for index in self.cluster_to_vec_index[c]:
                    headline = articles[index]["cleaned_title"]
                    clust_vecs.append(self.vecs[index])
                    for word in headline.split(' '):
                        if word in self.w2v.model:
                            if word in headline_vocab_dict:
                                headline_vocab_dict[word] = headline_vocab_dict[word] + 1
                            else:
                                headline_vocab_dict[word] = 1
                            headline_vocab.append(word)
                            annoy_headline_vocab.add_item(len(headline_vocab)-1, self.w2v.model[word])
                annoy_headline_vocab.build(5)
                cluster_vec = utilities.average_vector(clust_vecs, self.vec_length)
                label_idx = annoy_headline_vocab.get_nns_by_vector(cluster_vec, 5, include_distances=False)
                cluster_index_to_label[c] = self.get_most_freq_word(headline_vocab, headline_vocab_dict, label_idx)
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
