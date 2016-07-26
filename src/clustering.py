from annoy import AnnoyIndex


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
