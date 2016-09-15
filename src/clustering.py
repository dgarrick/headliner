from annoy import AnnoyIndex
import bisect

class Clustering:

    def __init__(self, vecs):
        self.vec_length = len(vecs[0])
        self.vecs = vecs
        self.headlines = []
        self.annoy = AnnoyIndex(self.vec_length, metric='euclidean')
        for i, vec in enumerate(self.vecs):
            self.annoy.add_item(i, vec)
        print("Built an index with " + str(self.annoy.get_n_items()) + " headlines")
        self.annoy.build(10)
        #self.rank_headlines()

    def get_neighbors_vector(self, vec):
        return self.annoy.get_nns_by_vector(vec, 10, include_distances=True)

    """def rank_headlines(self):
        for vec in self.vecs:
            if len(self.headlines) > 0:
                bisect.insort_right(self.headlines,(vec,self.get_neighbors_vector(vec)),0,len(self.headlines))
            else:
                self.headlines.append((vec,self.get_neighbors_vector(vec)))   """ 
