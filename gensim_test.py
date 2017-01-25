import gensim
import os
import numpy as np

class MySentences(object):
    def __init__(self, fname):
        self.fname = fname

    def __iter__(self):
        for line in open(self.fname):
            yield line.split()


def get_sentence_vector_avg(w2v, sentence):
    # Get vectors for each word in the sentence that appears in our training data, average them together and return
    return average_vector([w2v[word] for word in sentence.split() if word in w2v], int(70))

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

sentences = MySentences('/home/dgarrick/git/headliner/src/resources/fourMonths') # a memory-friendly iterator
model = gensim.models.Word2Vec.load_word2vec_format('/home/dgarrick/git/headliner/src/resources/output70', binary=True)

vecs = []
vecs.append(get_sentence_vector_avg(model, "CES 2017: Razer gaming laptop has not one but three screens"))
vecs.append(get_sentence_vector_avg(model, "CES 2017: The jacket that lets you stash 42 gadgets"))
vecs.append(get_sentence_vector_avg(model, "CES 2017: Sony chief pledges to detangle confusing TV tech"))
vec = average_vector(vecs, 70)

print(model.similar_by_vector(vec))
