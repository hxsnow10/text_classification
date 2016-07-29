import cPickle
import numpy
import theano
import random

def random_init(dims, good_initial=False):
    high, low = 1, -1
    if good_initial:
        high = 4.0 * numpy.sqrt( 6.0 / sum(dims) )
        low = -high

    w = numpy.zeros(dims, dtype=theano.config.floatX)
    randomize(w, dims, low=low, high=high)
    return theano.shared(value=w, borrow=True)

def random_pick(vec):
    idx = int(math.floor(random.uniform(0, len(vec))))
    return vec[idx]
    
def randomize(w, dims, low=-1, high=1):
    if len(dims)==1:
        for i in range(dims[0]):
            w[i] = random.uniform(low,high)
    else:
        for i in range(dims[0]):
            randomize(w[i], dims[1:], low, high)

