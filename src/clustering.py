from annoy import AnnoyIndex
from sklearn.cluster import KMeans
import numpy
import bisect

class Clustering:

    def __init__(self, vecs, per_cluster_avg):
        self.vec_length = len(vecs[0])
        self.vecs = vecs
        self.num_clusters = self.vec_length / per_cluster_avg
        self.cluster_to_vec = {}
        self.labels = []
        self.kmeans = KMeans(n_clusters = self.num_clusters)
        self.annoy = AnnoyIndex(self.vec_length, metric='euclidean')
        for i, vec in enumerate(self.vecs):
            self.annoy.add_item(i, vec)
        print("Built an index with " + str(self.annoy.get_n_items()) + " headlines")
        self.annoy.build(10)

    def get_neighbors_vector(self, vec):
        return self.annoy.get_nns_by_vector(vec, 10, include_distances=True)

    def get_vector_index(self, vec):
        return self.annoy.get_nns_by_vector(vec, 1, include_distances=False)

    @staticmethod
    def find_sorted_index(dists, total):
        """Returns None if no index can be found"""
        for i, dist in enumerate(dists):
            if total > dist:
                return i

    def label_clusters(self):
        """Finds the top N vectors which have the most dense clustering to other vectors.
           Returns a list of vectors zipped with their respective density score"""
        for i in xrange(self.num_clusters):
            cluster_vecs = self.cluster_to_vec.get(i)
            num_elems = len(cluster_vecs)
            dists = numpy.zeros(num_elems)
            labels = [None] * num_elems
            for vec in cluster_vecs:
                total = 0
                closest_arr = self.get_neighbors_vector(vec)[1]
                for dist in closest_arr:
                    if dist > 0:
                        total += 1.0 / dist
                index = 0
                local_vec = vec
                while index is not None:
                    index = self.find_sorted_index(dists, total)
                    if index is not None:
                        tmp_total = dists[index]
                        tmp_vec = labels[index]
                        numpy.put(dists, index, total)
                        labels[index] = local_vec
                        total = tmp_total
                        local_vec = tmp_vec
            return zip(labels, dists)

    def kmeans_cluster(self):
        clusters = self.kmeans.fit_predict(self.vecs)
        self.cluster_to_vec = dict(zip(self.vecs, clusters))
        self.labels = self.label_clusters() 
