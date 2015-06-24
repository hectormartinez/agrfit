__author__ = 'alonso'
import argparse
import numpy as np
from nltk.corpus import framenet as fn
from collections import Counter

def normalizeLemma(word):
    #lemmas have forms like export_((act)) or theater_((of_war))
    word = word.replace(" (","(").replace("_(","(").replace("((","(").replace("))",")").split("(")[0]
    return word

def frameCounter():
    #parser.add_argument("infile",  metavar="FILE", help="name of the framenet-parsed file file")
    Entries = Counter()

    #Add frames from the FN lexicon
    for d in fn.documents():
        for sentence in fn.annotated_document(d["ID"])["sentence"]:
            for annotation in sentence["annotationSet"]:
                if "frameID" in annotation.keys():
                    signature = annotation["luName"]
                    lemma, pos = annotation["luName"].split(".")
                    lemma = normalizeLemma(lemma)
                    frameID = str(annotation["frameID"])
                    framename = annotation["frameName"]
                    for x in annotation["layer"]:
                        if x["name"] == "Target":
                            for l in x["label"]:
                                start = int(l["start"])
                                end = int(l["end"])
                                form = sentence["text"][start:end+1].lower()
    Entries[framename]+=1
    return Entries
