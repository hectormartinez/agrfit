import gensim
import argparse
import numpy
from scipy.stats import entropy


def softmax(w):
    w = numpy.array(w)

    maxes = numpy.amax(w, axis=1)
    maxes = maxes.reshape(maxes.shape[0], 1)
    e = numpy.exp(w - maxes)
    dist = e / numpy.sum(e, axis=1)

    return dist


parser = argparse.ArgumentParser(description="")
parser.add_argument("infile",   metavar="FILE", help="name of the input file")

args = parser.parse_args()


for line in [x for x in open(args.infile).readlines()][1:]:
    a = line.strip().split(" ")
    key = a[0]
    v = [float(x) for x in a[1:]]
    print(a,entropy(softmax(v)))
