import argparse
import numpy as np
from utils import *
from wordannotatedsentence import *
from collections import defaultdict
import math





def InverseLogRank(form,sortedvocab):
    if form  in sortedvocab:
        return 1/math.log(sortedvocab.index(form)+2) #+2 = +1 to adjust to the real rank, +1 to avoid divisions by zero
    return 1/math.log(len(sortedvocab))

def f_targetFreq(s,sortedvocab):
    form = s.forms[s.headwordindex]
    return InverseLogRank(form.lower(),sortedvocab)


def f_head_of_targetFreq(s,sortedvocab):

    head_of_target = head_of(s.parsetree,s.headwordindex)
    if head_of_target != 0:
        form = s.forms[head_of_target]
        return InverseLogRank(form.lower(),sortedvocab)
    return 0.0

def f_posbigram(s,left=True):
    if left:
        array = s.postags[s.headwordindex-2:s.headwordindex]
    else:
        array = s.postags[s.headwordindex+1:s.headwordindex+3]
    if len(array) == 0:
        array = ["none"]
    return "_".join(array)


def main():
    parser = argparse.ArgumentParser(description="Rewrite Semafor input to annotation format")
    parser.add_argument("infilecommon",  metavar="FILE", help="name of the framenet-parsed file file")
    parser.add_argument("sortedvocab",  metavar="FILE", help="name of the framenet-parsed file file")

    args = parser.parse_args()

    sortedvocab = []
    for l in open(args.sortedvocab):
        try:
            freq,word = l.strip().split(" ")
            sortedvocab.append(word)
        except:
            print("ERROR",l)



    #sortedvocab = [x.strip().split(" ")[1] for x in open(args.sortedvocab,encoding="utf-8").readlines()]

    #Load common file into a list of WordAnnotatedSentence
    instances = readsentences(args.infilecommon)
    for s in instances:
        feats = defaultdict(list)

        feats["a_targetwordfreq_n"] = f_targetFreq(s,sortedvocab)
        feats["a_headoftargetfreq_n"] = f_head_of_targetFreq(s,sortedvocab)
        feats["b_targetpos_s"] =  s.postags[s.headwordindex]
        feats["b_head_of_targetpos_s"] = s.postags[head_of(s.parsetree,s.headwordindex)]
        feats["c_posbigram_left"] = f_posbigram(s)
        feats["c_posbigram_right"] = f_posbigram(s,left=False)
        feats["X_slength_n"] = len(s.postags[1:])
        feats["X_content_proportion_n"] = len([x for x in s.postags[1:] if x in CONTENTTAGS]) / len(s.postags[1:])
        print(s.id_,s.headwordindex,s.forms,s.postags,feats)



if __name__ == "__main__":
    main()