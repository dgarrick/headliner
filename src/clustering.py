from annoy import AnnoyIndex
from sklearn.cluster import KMeans
import numpy
import bisect

class Clustering:

    def __init__(self, vecs):
        self.vec_length = len(vecs[0])
        self.vecs = vecs
        self.num_clusters = int(len(vecs) * 0.20)
        self.threshold = 0.25
        self.cluster_to_vec_index = {}
        self.labels = []
        self.kmeans = KMeans(n_clusters=self.num_clusters)
        self.annoy = AnnoyIndex(self.vec_length, metric='euclidean')
        for i, vec in enumerate(self.vecs):
            self.annoy.add_item(i, vec)
        print("Built an index with " + str(self.annoy.get_n_items()) + " headlines")
        self.annoy.build(10)

    def get_neighbors_vector(self, vec):
        return self.annoy.get_nns_by_vector(vec, 10, include_distances=True)

    @staticmethod
    def find_sorted_index(dists, total):
        """Returns None if no index can be found"""
        for i, dist in enumerate(dists):
            if total > dist:
                return i

    def rank_clusters(self):
        """Finds the top N vectors which have the most dense clustering to other vectors.
           Returns a list of vectors zipped with their respective density score"""
        for i in xrange(self.num_clusters):
            cluster_vec_indices = self.cluster_to_vec_index[i]
            num_elems = len(cluster_vec_indices)
            dists = numpy.zeros(num_elems)
            for j in cluster_vec_indices:
                vec = self.vecs[j]
                total = 0
                closest_arr = self.get_neighbors_vector(vec)[1]
                for dist in closest_arr:
                    if dist > 0:
                        total += 1.0 / dist
                index = 0
                cur_idx = j
                while index is not None:
                    index = self.find_sorted_index(dists, total)
                    if index is not None:
                        tmp_total = dists[index]
                        tmp_idx = cluster_vec_indices[index]
                        numpy.put(dists, index, total)
                        cluster_vec_indices[index] = cur_idx
                        total = tmp_total
                        cur_idx = tmp_idx
            self.cluster_to_vec_index[i] = cluster_vec_indices

    def kmeans_cluster(self, rank_clusters=False):
        vec_index_to_cluster = self.kmeans.fit_predict(self.vecs)
        vec_indices = range(0, len(self.vecs))
        for j in xrange(0, self.num_clusters):
            self.cluster_to_vec_index[j] = []
        for i in xrange(0, len(vec_indices)):
            self.cluster_to_vec_index[vec_index_to_cluster[i]].append(vec_indices[i])
        if rank_clusters:
            self.rank_clusters()
