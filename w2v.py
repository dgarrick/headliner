# Required packages: word2vec (which requires numpy and cython)
import word2vec
import os.path
import random


class W2V:
    def __init__(self):
        self.input_fname = 'bigsample'
        # If no file exists with this name, we will train and store the trained date here.
        self.trained_fname = 'output30'
        # 30 dims seems to be a good value
        self.train_dimensions = 30
        self.model = None

    def train(self):
        if not os.path.isfile(self.trained_fname):
            print("Previous training '" + self.trained_fname + "' not found. Begin training on input '" +
                  self.input_fname + "' into " + str(self.train_dimensions) + " dimensions ...")
            word2vec.word2vec(self.input_fname, self.trained_fname, size=self.train_dimensions)
        else:
            print("Trained data seems to exist at '" + self.trained_fname + "'")

    def about(self):
        print("Loading training results...")
        self.model = word2vec.load(self.trained_fname, kind='bin')
        words, dims = self.model.vectors.shape
        print("\nShape: " + str(words) + " words")
        print("\nDimensions: " + str(dims) + " dimensions")
        print("\nVocab sample: " + str(self.model.vocab))
        print("\nVectors: " + str(self.model.vectors))
        # Sanity check: similar words to 'rocks'
        self.print_similar_words_to('rocks')
        # Grab a random index from within the range of the vocabulary
        random_index = random.randint(0, words-1)
        random_word = self.model.vocab[random_index]
        print("\nA random word (index " + str(random_index) + ") from this set... '" + random_word + "'")
        print("\nVectors corresponnding to '" + random_word + "': " + str(self.model[random_word]))
        self.print_similar_words_to(random_word)

    def print_similar_words_to(self, word):
        indices, metrics = self.model.cosine(word)
        print("\nSimilar words to '" + str(word) + "'")
        for index, metric in zip(indices, metrics):
            print("\tword: '" + str(self.model.vocab[index]) + "'\tvalue: " + str(metric))
