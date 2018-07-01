from annoy import AnnoyIndex
from sklearn.cluster import AgglomerativeClustering
import utilities
import numpy
from utilities import lemmatize_word

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
        """this should probably not be called directly: use
        label_and_merge_clusters instead"""
        cluster_index_to_label = {}
        for c in self.cluster_to_vec_index.keys():
            annoy_headline_vocab = AnnoyIndex(self.vec_length, metric='angular')
            headline_vocab = []
            headline_vocab_dict = {}
            clust_vecs = []
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
            cluster_index_to_label[c] = lemmatize_word(self.get_most_freq_word(headline_vocab, headline_vocab_dict, label_idx))
        return cluster_index_to_label

    def label_and_merge_clusters(self, articles):
        """merges all clusters with similar labels"""
        cluster_index_to_label = self.label_clusters(articles)
        label_to_cluster_index = {}
        for c_idx in cluster_index_to_label.keys():
            label = cluster_index_to_label[c_idx]
            if label in label_to_cluster_index:
                label_to_cluster_index[label].append(c_idx)
            else:
                label_to_cluster_index[label] = [c_idx]
        for label, clust_list in label_to_cluster_index.iteritems():
            if len(clust_list) > 1:
                merge_clust = clust_list[0]
                for i in xrange(1, len(clust_list)):
                    cur_clust = clust_list[i]
                    cur_vecs = self.cluster_to_vec_index[cur_clust]
                    self.cluster_to_vec_index[merge_clust].extend(cur_vecs)
                    del self.cluster_to_vec_index[cur_clust]
                    del cluster_index_to_label[cur_clust]
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
