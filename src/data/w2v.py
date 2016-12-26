# Required packages: word2vec (which requires numpy and cython)
import os.path
import random

import word2vec
import numpy
import math

import utilities


class W2V:
    def __init__(self, input_fname, trained_fname, num_dims):
        self.input_fname = input_fname
        # If no file exists with this name, we will train and store the trained date here.
        self.trained_fname = trained_fname
        # 30 dims seems to be a good value
        self.train_dimensions = num_dims
        self.model = None

    def train(self):
        if not os.path.isfile(self.trained_fname):
            print("Previous training '" + self.trained_fname + "' not found. Begin training on input '" +
                  self.input_fname + "' into " + str(self.train_dimensions) + " dimensions ...")
            word2vec.word2vec(self.input_fname, self.trained_fname, size=self.train_dimensions)
        else:
            print("Trained data seems to exist at '" + self.trained_fname + "'")
        print("Loading training results...")
        self.model = word2vec.load(self.trained_fname, kind='bin')

    def about(self):
        words, dims = self.model.vectors.shape
        print("\nShape: " + str(words) + " words")
        print("\nDimensions: " + str(dims) + " dimensions")
        print("\nVocab sample: " + str(self.model.vocab))
        print("\nVectors: " + str(self.model.vectors))
        # Sanity check: similar words to 'rocks'
        self.print_similar_words_to('rocks')
        # Grab a random index from within the range of the vocabulary
        random_word = self.get_random_word(words)
        print("\nVectors corresponnding to '" + random_word + "': " + str(self.model[random_word]))
        self.print_similar_words_to(random_word)
        random_sentence = [self.model[self.get_random_word(words)] for i in range(0, 3)]
        utilities.average_vector(random_sentence, dims)

    def get_random_word(self, words):
        random_index = random.randint(0, words - 1)
        return self.model.vocab[random_index]

    def get_random_word_and_vector(self):
        index = random.randint(0, len(self.model.vocab) - 1)
        return self.model.vocab[index], self.model.vectors[index]

    def print_similar_words_to(self, word):
        indices, metrics = self.model.cosine(word)
        print("\nSimilar words to '" + str(word) + "'")
        for index, metric in zip(indices, metrics):
            print("\tword: '" + str(self.model.vocab[index]) + "'\tvalue: " + str(metric))

    def get_vector(self, word):
        if word in self.model:
            return self.model[word]

    def get_sentence_vector_newtonian(self, sentence):
        word_vecs = []
        words = []
        for word in sentence.split(" "):
            word = word.lower()
            if word in self.model:
                word_vecs.append(self.model[word])
                words.append(word)

        # Had a 1-word article once...
        if len(word_vecs) == 1:
            return word_vecs[0]

        # bit hacky.
        dimensions = word_vecs[0].shape[0]
        # array of 1's with length of dimensions
        sentence_vec = [1] * dimensions
        for vec in word_vecs:
            force = self._get_force(vec, word_vecs)
            # One way of doing it is to avegage the forces.. there are others.
            avg_force = sum(force) / len(force)
            for i, dimensional_scalar in enumerate(vec):
                sentence_vec[i] += avg_force * dimensional_scalar

        assert(len(sentence_vec) == len(word_vecs[0]))
        return self._normalize_vector(numpy.asarray(sentence_vec))

    # Just returns the length of the vector. Nothing special.
    def _get_vector_length(self, vector):
        distance_sum = 0
        for dimension in range(0, vector.shape[0]):
            distance_sum += vector[dimension] * vector[dimension]
        return math.sqrt(distance_sum)

    def _normalize_vector(self, vector):
        vec_length = self._get_vector_length(vector)
        for i in xrange(len(vector)):
            vector[i] /= vec_length
        return vector

    def _get_force(self, vector, other_vectors):
        dimensions = vector.shape[0]
        forces = []
        for i, other in enumerate(other_vectors):
            # Don't want to consider forces to our own vector for fear of dividing by zero.
            if not numpy.array_equal(other, vector):
                distance = self._get_distance_euclidian(vector, other)
                # Modified version of Newton's Gravitational Formula. Log base is adjustment value!
                forces.append(1.0 / (math.pow(distance, math.log10(dimensions))))
        return forces

    def _get_distance_euclidian(self, vector, other):
        dimensions = vector.shape[0]
        # Calculate distances.
        distance_sums = 0
        for dimension in range(0, dimensions):
            this_dist = other[dimension] - vector[dimension]
            distance_sums += this_dist * this_dist
        distance = math.sqrt(distance_sums)
        return distance

    def get_sentence_vector_avg(self, sentence):
        # Get vectors for each word in the sentence that appears in our training data, average them together and return
        return utilities.average_vector([self.model[word] for word in sentence.split() if word in self.model], int(self.train_dimensions))
