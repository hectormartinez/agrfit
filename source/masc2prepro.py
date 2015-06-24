__author__ = 'alonso'
import argparse
from collections import defaultdict
from utils import *

#The ritter data have Petrov tags, we kind of circumvent the issue


def main():
    parser = argparse.ArgumentParser(description=")")
    parser.add_argument("infilesentences",   metavar="FILE", help="name of the input file")
    parser.add_argument("infileannotations",   metavar="FILE", help="name of the input file")
    parser.add_argument("infilesenses",   metavar="FILE", help="name of the input file")

    args = parser.parse_args()


    fout = open(args.infilesentences+".topos","w")
    foutannotations = open(args.infilesentences+".annotations","w")


    outforms = []
    outannotations = []


    annotationlist = defaultdict(list)
    sensedict = defaultdict(dict)



    for line in open(args.infilesenses).readlines()[1:]:
        WordPos,	SenseId	,Definition,	Examples,	WordNetId,WordNetSynonyms = line.strip().split("\t")
        sensedict[WordPos][SenseId] = WordNetId

    print(sensedict)

    for line in open(args.infileannotations).readlines()[1:]:
        WordPos,FormId,SentenceId,AnnotatorId,SenseId = line.strip().split("\t")
        sentencekey = ":".join([WordPos,FormId,SentenceId])
        annotationlist[sentencekey].append(SenseId)

    #print(annotationlist)

    for line in open(args.infilesentences).readlines()[1:]:
        WordPos,FormId,SentenceId,Text,AncDocPath,SentenceStart,WordStart,WordEnd,WordForm = line.strip().split("\t")
        #print(WordPos,FormId,SentenceId,SentenceStart,WordStart,WordEnd,WordForm)
        #print(Text.split(" ").count(WordForm),Text,WordForm,WordStart,WordEnd,Text[int(WordStart):int(WordEnd)+1])
        SentenceStart = int(SentenceStart)
        WordStart=int(WordStart)
        WordEnd=int(WordEnd)
        if SentenceStart > -1:
            WordStart = WordStart  - SentenceStart
            WordEnd = WordEnd - SentenceStart

        preText=tokenizestring(Text[:WordStart])
        wordText=cleanheadword(Text[WordStart:(WordEnd)+1])
        posText=tokenizestring(Text[WordEnd+1:])

        if wordText: # cleanheadword() returns None upon tokenization errors or bad sentences and whatnot
            currentsentence = preText + [wordText] + posText + [SENTENCEBOUNDARY]

            sentencekey = ":".join([WordPos,FormId,SentenceId])
            preAnno = ["_\t_\t_"] * len(preText)
            postAnno = ["_\t_\t_"] * len(posText)
            instanceidentifier="_".join([WordPos,FormId,SentenceId])
            wordAnno = [instanceidentifier+"\t"+",".join(annotationlist[sentencekey])+"\t"+"nlabels:"+str(len(sensedict[WordPos].keys()))]

            currentanno = preAnno + wordAnno + postAnno + [""]

            #print(sentencekey,wordText,wordAnno,currentsentence,currentanno)
            #outforms.extend(padline(currentsentence))
            #outannotations.extend(padline(currentanno))
            outforms.append("\n".join(currentsentence)+"\n")
            outannotations.append("\n".join(currentanno)+"\n")

    fout.writelines(outforms)
    fout.close()
    foutannotations.writelines(outannotations)
    foutannotations.close()


if __name__ == "__main__":
    main()