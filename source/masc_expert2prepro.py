import argparse
from collections import defaultdict
from utils import *

from nltk.corpus import wordnet as wn


#The ritter data have Petrov tags, we kind of circumvent the issue


def main():
    parser = argparse.ArgumentParser(description=")")
    parser.add_argument("infilesentences",   metavar="FILE", help="name of the input file")
    parser.add_argument("infileannotations",   metavar="FILE", help="name of the input file")
    parser.add_argument("querylemma")
    parser.add_argument("queryforms",help="comma-separated possible forms to trigger sense annotation, like 'know,knows,known'")

    #parser.add_argument("infilesenses",   metavar="FILE", help="name of the input file")

    args = parser.parse_args()


    fout = open(args.infilesentences+".topos","w")
    foutannotations = open(args.infilesentences+".annotations","w")
    queryforms = args.queryforms.split(",")

    lemma, pos = args.querylemma.split("-")

    if pos == "j":
        pos = "a"


    sentencewiseannotatedlabels = [x.strip().replace("\t",",").replace("9999","0").replace("999","0") for x in open(args.infileannotations).readlines()[1:]]

    for sentenceid,line in enumerate(open(args.infilesentences).readlines()[:len(sentencewiseannotatedlabels)]):
        line = line.strip()
        tokenized = tokenizestring(line)
        foundtargetword = -1
        for idxt,t in enumerate(tokenized):
            if t.lower() in queryforms:
                foundtargetword = idxt
        if foundtargetword == -1:
            print(queryforms, "not in", tokenized)
            continue
        currentline = tokenized+[SENTENCEBOUNDARY]
        currentanno = ["_\t_\t_"] * len(currentline)
        nlabels = len(wn.synsets(lemma,pos=pos))
        instanceidentifier= str(sentenceid)+"_"+str(foundtargetword)+"_"+args.querylemma
        annotatedlabels = sentencewiseannotatedlabels[sentenceid]
        currentanno[foundtargetword] = "\t".join([instanceidentifier,annotatedlabels,"nlabels:"+str(nlabels)])
        currentanno[-1]=""
        for line in currentline:
            fout.write(line+"\n")
        for line in currentanno:
            foutannotations.write(line+"\n")

    fout.close()
    foutannotations.close()


if __name__ == "__main__":
    main()
