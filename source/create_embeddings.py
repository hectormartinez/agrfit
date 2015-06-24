import gensim
import argparse

parser = argparse.ArgumentParser(description="Code snippet to get started with gensim. It generates an embeddings space from the input corpus and prints the vector for the word 'although'")
parser.add_argument("infile",   metavar="FILE", help="name of the input file")
args = parser.parse_args()

sentences = []
for line in open(args.infile).readlines():
    sentences.append(line.lower().strip().split(" "))

print("Generating embeddings, it might take a while")
embeddings = gensim.models.Word2Vec(sentences, size=100, window=5,min_count=5,sg=2,negative=10)
embeddings.save_word2vec_format(args.infile+".embeds",binary=False)
