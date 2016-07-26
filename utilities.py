import numpy as np
import re


def average_vector(vecs):
    num_vecs = len(vecs)
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


def strip_punctuation(sentence):
    return re.sub(r'([^\s\w]|_)+', '', sentence).lower()

