from annoy import AnnoyIndex
import numpy
import bisect

class Clustering:

    def __init__(self, vecs):
        self.vec_length = len(vecs[0])
        self.vecs = vecs
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

    def rank_vectors(self, num_ranks):
        """Finds the top N vectors which have the most dense clustering to other vectors.
           Returns a list of vectors zipped with their respective density score"""
        dists = numpy.zeros(num_ranks)
        labels = [None] * num_ranks
        for vec in self.vecs:
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
