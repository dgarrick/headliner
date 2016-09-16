from annoy import AnnoyIndex
import numpy
import bisect

class Clustering:

    def __init__(self, vecs):
        self.vec_length = len(vecs[0])
        self.vecs = vecs
        self.ranks = 10
        self.dists = numpy.zeros(self.ranks)
        self.labels = []
        self.annoy = AnnoyIndex(self.vec_length, metric='euclidean')
        for i, vec in enumerate(self.vecs):
            self.annoy.add_item(i, vec)
        print("Built an index with " + str(self.annoy.get_n_items()) + " headlines")
        self.annoy.build(10)
        self.rank_headlines()

    def get_neighbors_vector(self, vec):
        return self.annoy.get_nns_by_vector(vec, 10, include_distances=True)

    def rank_headlines(self):
        for vec in self.vecs:
            total = 0
            closest_arr = self.get_neighbors_vector(vec)[1]
            for dist in closest_arr:
                total += dist * 10
            #shits not working
            index = numpy.searchsorted(self.dists, total)
            print(index)
            if index < self.ranks:
                self.dists = numpy.insert(self.dists, index, total)
                print(self.dists[index])
            self.labels.insert(index, vec)
