__author__ = 'alonso'
import argparse
from utils import *
from nltk.corpus import framenet as fn
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
#The ritter data have Petrov tags, we kind of circumvent the issue

# 1       and     _       CONJ    CONJ    _       4       cc
# 2       they    _       PRON    PRON    _       4       nsubj
# 3       'd      _       AUX     AUX     _       4       aux

#Nivre tags
# ADJ
# ADP
# ADV
# AUX
# CONJ
# DET
# INTJ
# NOUN
# NUM
# PART
# PRON
# PROPN
# PUNCT
# SCONJ
# SYM
# VERB
# X

#Petrov tags
# ADJ
# ADP
# ADV
# CONJ
# DET
# NOUN
# NUM
# PRON
# PRT
# VERB
# X



framenetpos = defaultdict(str)
framenetpos["NOUN"]=".n"
framenetpos["PROPN"]=".n"
framenetpos["SCONJ"]=".scon"
framenetpos["NUM"]=".num"
framenetpos["CONJ"]=".c"
framenetpos["INTJ"]=".intj"
framenetpos["VERB"]=".v"
framenetpos["AUX"]=".v"
framenetpos["ADJ"]=".a"
framenetpos["DET"]=".art"
framenetpos["ADP"]=".prep"
framenetpos["ADJ"]=".adv"



def choosePos(petrov_pos,nivre_pos):
    if petrov_pos not in NIVRETAGS:
        return PETROVTONIVREMAP[petrov_pos]
    if (petrov_pos,nivre_pos) in PREFERNIVRETAG:
        return nivre_pos
    return petrov_pos


def main():
    parser = argparse.ArgumentParser(description=")")
    parser.add_argument("infileparsed",   metavar="FILE", help="name of the input file")
    parser.add_argument("annofile",   metavar="FILE", help="name of the input file")
    args = parser.parse_args()


    fout = open(args.infileparsed+".common","w")
    outforms = []

    lmtzr = WordNetLemmatizer()

    sentenceounter=1
    for lineparse,lineanno in zip(open(args.infileparsed).readlines(), open(args.annofile)):
        lineparse=lineparse.strip()
        if lineparse:
            tokid, form, lemma, nivre_pos, pos2, feats, head, label = lineparse.split("\t")
            annoarray = lineanno.strip().split("\t")
            #print(annoarray)
            #petrov_pos, a1, a2, a3
            petrov_pos = annoarray[0]

            assignedpos = choosePos(petrov_pos,nivre_pos)
            lineout = [tokid,form,assignedpos,head,label]
            if len(annoarray) == 4 and annoarray[1] != "" and annoarray[2] != "" and annoarray[3] != "":
                labels = ",".join(annoarray[1:])
                xform = form.replace("*","-").lower()
                fnpos=framenetpos[assignedpos]
                if fnpos in ["n", ".v", ".a"]:
                    xform = lmtzr.lemmatize(xform,pos=assignedpos[0].lower())
                framesperlemma = fn.frames_by_lemma(xform+fnpos)
                instanceidentifier= "_".join([str(sentenceounter),tokid])
                nlabels = max(len(framesperlemma),len(set(annoarray[1:]))) #This is for the case of not giving a framelabel
                annotations = [instanceidentifier,labels,"nlabels:"+str(nlabels)]#[instanceidentifier+"\t"+",".join([a1,a2,a3])+"\t"+"nlabels:"+))]
            else:
                annotations = ["_"] * 3
            lineout.extend(annotations)
            fout.write("\t".join(lineout)+"\n")
        else:
            sentenceounter+=1
            fout.write("\n")

    fout.close()



if __name__ == "__main__":
    main()