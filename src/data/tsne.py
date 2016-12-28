#
#
# Implementation of t-SNE in Python. The implementation was tested on Python 2.7.10, and it requires a working
# installation of NumPy. The implementation comes with an example on the MNIST dataset. In order to plot the
# results of this example, a working installation of matplotlib is required.
#
# The example can be run by executing: `ipython tsne.py`
#
#
#  Created by Laurens van der Maaten on 20-12-08.
#  Copyright (c) 2008 Tilburg University. All rights reserved.

import numpy as math
from matplotlib import pyplot

def h_beta(d=math.array([]), beta=1.0):
    """Compute the perplexity and the P-row for a specific value of the precision of a Gaussian distribution."""
    # Compute P-row and corresponding perplexity
    p = math.exp(-d.copy() * beta)
    sum_p = sum(p)
    h = math.log(sum_p) + beta * math.sum(d * p) / sum_p
    p = p / sum_p
    return h, p


def x2p(x=math.array([]), tol=1e-5, perplexity=30.0):
    """Performs a binary search to get P-values in such a way that each conditional Gaussian has the same perplexity."""
    # Initialize some variables
    print "Computing pairwise distances..."
    (n, d) = x.shape
    sum_x = math.sum(math.square(x), 1)
    d = math.add(math.add(-2 * math.dot(x, x.T), sum_x).T, sum_x)
    p = math.zeros((n, n))
    beta = math.ones((n, 1))
    log_u = math.log(perplexity)

    # Loop over all datapoints
    for i in range(n):

        # Print progress
        if i % 500 == 0:
            print "Computing P-values for point ", i, " of ", n, "..."

        # Compute the Gaussian kernel and entropy for the current precision
        betamin = -math.inf
        betamax = math.inf
        d_i = d[i, math.concatenate((math.r_[0:i], math.r_[i + 1:n]))]
        (h, this_p) = h_beta(d_i, beta[i])

        # Evaluate whether the perplexity is within tolerance
        h_diff = h - log_u
        tries = 0
        while math.abs(h_diff) > tol and tries < 50:
            # If not, increase or decrease precision
            if h_diff > 0:
                betamin = beta[i].copy()
                if betamax == math.inf or betamax == -math.inf:
                    beta[i] *= 2
                else:
                    beta[i] = (beta[i] + betamax) / 2
            else:
                betamax = beta[i].copy()
                if betamin == math.inf or betamin == -math.inf:
                    beta[i] /= 2
                else:
                    beta[i] = (beta[i] + betamin) / 2

            # Recompute the values
            (h, this_p) = h_beta(d_i, beta[i])
            h_diff = h - log_u
            tries += 1

        # Set the final row of P
        p[i, math.concatenate((math.r_[0:i], math.r_[i + 1:n]))] = this_p

    # Return final P-matrix
    print "Mean value of sigma: ", math.mean(math.sqrt(1 / beta))
    return p


def pca(x=math.array([]), dimensions=50):
    """Runs PCA on the NxD array X in order to reduce its dimensionality to no_dims dimensions."""

    print "Preprocessing the data using PCA..."
    (n, d) = x.shape
    x = x - math.tile(math.mean(x, 0), (n, 1))
    (l, m) = math.linalg.eig(math.dot(x.T, x))
    return math.dot(x, m[:, 0:dimensions])


def tsne(x=math.array([]), dimensions=2, initial_dimensions=50, perplexity=30.0):
    """Runs t-SNE on the dataset in the NxD array X to reduce its dimensionality to no_dims dimensions.
    The syntaxis of the function is y = tsne.tsne(X, no_dims, perplexity), where X is an NxD NumPy array."""

    # Check inputs
    if isinstance(dimensions, float):
        print "Error: array X should have type float."
        return -1
    if round(dimensions) != dimensions:
        print "Error: number of dimensions should be an integer."
        return -1

    # Initialize variables
    x = pca(x, initial_dimensions).real
    (n, d) = x.shape
    max_iter = 1000
    initial_momentum = 0.5
    final_momentum = 0.8
    eta = 500
    min_gain = 0.01
    y = math.random.randn(n, dimensions)
    d_y = math.zeros((int(n), dimensions))
    i_y = math.zeros((n, dimensions))
    gains = math.ones((n, dimensions))

    # Compute p-values
    p = x2p(x, 1e-5, perplexity)
    p = p + math.transpose(p)
    p = p / math.sum(p)
    p *= 4
    p = math.maximum(p, 1e-12)

    # Run iterations
    for i in range(max_iter):

        # Compute pairwise affinities
        sum_y = math.sum(math.square(y), 1)
        num = 1 / (1 + math.add(math.add(-2 * math.dot(y, y.T), sum_y).T, sum_y))
        num[range(n), range(n)] = 0
        q = num / math.sum(num)
        q = math.maximum(q, 1e-12)

        # Compute gradient
        pq = p - q
        for j in range(n):
            d_y[j,:] = math.sum(math.tile(pq[:, j] * num[:, j], (dimensions, 1)).T * (y[j, :] - y), 0)

        # Perform the update
        if i < 20:
            momentum = initial_momentum
        else:
            momentum = final_momentum
        gains = (gains + 0.2) * ((d_y > 0) != (i_y > 0)) + (gains * 0.8) * ((d_y > 0) == (i_y > 0))
        gains[gains < min_gain] = min_gain
        i_y = momentum * i_y - eta * (gains * d_y)
        y += i_y
        y = y - math.tile(math.mean(y, 0), (n, 1))

        # Compute current value of cost function
        if (i + 1) % 10 == 0:
            c = math.sum(p * math.log(p / q))
            print "Iteration ", (i + 1), ": error is ", c

        # Stop lying about p-values
        if i == 100:
            p /= 4

    # Return solution
    return y


def plot(labels=None, sizes=None, vecs=math.array([])):
    if labels is None:
        labels = []
    coords = tsne(vecs, initial_dimensions=vecs.shape[0])
    pyplot.scatter(coords[:, 0], coords[:, 1], sizes[:])

    for label, x, y in zip(labels, coords[:, 0], coords[:, 1]):
        pyplot.annotate(label, xy=(x, y))
    pyplot.show()


def plot_simple(vecs=math.array([])):

    coords = tsne(vecs, initial_dimensions=vecs.shape[0])
    pyplot.scatter(coords[:, 0], coords[:, 1], 30)
    pyplot.show()
