import argparse
import numpy as np
from utils import *
from wordannotatedsentence import *
from collections import defaultdict
import math
import itertools


LOW=1/3
HIGH=2/3

HEADINGCOLUMNS=["i_id","y_Ao_n","y_Class_s"]

def header_in_order(feats):
    h = []
    for c in HEADINGCOLUMNS:
        h.append(c)
    for k in sorted(feats.keys()):
        if k not in HEADINGCOLUMNS:
            h.append(k)
    return h


def outfeats(feats):
    out = []
    header = header_in_order(feats)
    for h in header:
        out.append(str(feats[h]))
    return "\t".join(out)


def f_nsenses(s):
    return s.extra["nlabels"]

def f_distance_to_root(s,wordindex):
    return 0

def f_contextbagofwords(s):
    o = []
    for w in s.forms[:s.headwordindex]+s.forms[s.headwordindex+1:]:
        o.append(w.lower())
    return " ".join(sorted(set(o)))

def f_ndeps(s,wordindex):
    c=0
    for head, dependent in s.parsetree.edges():
        if head == wordindex:
            c+=1
    return c
def f_bag_of_dependent_labels(s,wordindex):
    c=[]
    for head, dependent in s.parsetree.edges():
        if head == wordindex:
            c.append(s.parsetree[head][dependent]["deprel"])
    if c == []:
        c = ["none"]
    return " ".join(c)
def y_Ao(annotations):
    total = 0.0
    pairings = [x for x in itertools.combinations(annotations,2)]
    for a1,a2 in pairings:
        total+=int(a1==a2)
    return total / len(pairings)

def y_Class(annotations):
    Ao = y_Ao(annotations)
    if Ao <= LOW:
        return "LOW"
    if Ao >= HIGH:
        return "HIGH"
    return "MID"


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
    parser.add_argument("idf_list",  metavar="FILE", help="")
    parser.add_argument("sense_entropy",  metavar="FILE", help="")


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
    printedheader=False
    for s in instances:
        feats = defaultdict(list)

        feats["a_targetfreq_n"] = f_targetFreq(s,sortedvocab)
        feats["a_headfreq_n"] = f_head_of_targetFreq(s,sortedvocab)
        feats["b_targetpos_s"] =  s.postags[s.headwordindex]
        feats["b_headpos_s"] = s.postags[head_of(s.parsetree,s.headwordindex)]
        feats["c_posbigram_left_s"] = f_posbigram(s)
        feats["c_posbigram_right_s"] = f_posbigram(s,left=False)
        feats["X_slength_n"] = len(s.postags[1:])
        feats["X_content_proportion_n"] = len([x for x in s.postags[1:] if x in CONTENTTAGS]) / len(s.postags[1:])
        feats["X_targetdeps_n"]=f_ndeps(s,s.headwordindex)
        feats["X_headsdeps_n"]=f_ndeps(s,head_of(s.parsetree,s.headwordindex))
        feats["X_targetdepsrels_b"]=f_bag_of_dependent_labels(s,head_of(s.parsetree,s.headwordindex))
        feats["X_headdeprels_b"]=f_bag_of_dependent_labels(s,head_of(s.parsetree,head_of(s.parsetree,s.headwordindex)))

        feats["X_context_b"]=f_contextbagofwords(s)
        feats["X_nlabels_n"]=f_nsenses(s)


        feats["y_Ao_n"]=y_Ao(s.annotations)
        feats["y_Class_s"]=y_Class(s.annotations)
        feats["i_id"]=s.id_
        if not printedheader:
            print("\t".join(header_in_order(feats)))
            printedheader=True
        print(outfeats(feats))



if __name__ == "__main__":
    main()