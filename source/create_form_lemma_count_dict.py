import argparse
from collections import Counter

valid = "abcdefghijklmnopqrstuvwzyz0123456789"

def isvalid(s):
    current = s.replace("@","A").replace("~","0").replace("-","1").replace("/","2").replace(".","3").replace("_","4").lower()
    current2=""
    for c in current:
        if c in valid:
            current2+=c
    return current2.isalpha() or current2.isdigit() or current2.isalnum()

def contentlist(s):
    v= [x.lower() for x in s.replace("\n","").split(" ") if isvalid(x)]
    if len(v)>0:
        if v[-1] in "?.!":
            v=v[:-1]
    return v

def main():
    parser = argparse.ArgumentParser(description="Rewrite Semafor input to annotation format")
    parser.add_argument("inform",  metavar="FILE", help="")
    parser.add_argument("instem",  metavar="FILE", help="")

    args = parser.parse_args()
    Ctuples = Counter()
    Cforms = Counter()
    Cstems = Counter()
    for lineform, linestem in zip(open(args.inform).readlines(),open(args.instem).readlines()):
        formlist=(contentlist(lineform))
        stemlist=(contentlist(linestem))
        print(len(contentlist(linestem)),len(contentlist(lineform)))
        for f,s in zip(formlist,stemlist):
            Ctuples[(f,s)]+=1
            Cforms[f]+=1
            Cstems[s]+=1

    for ((f,s),v) in Ctuples.most_common():
        print("\t".join([f,s,str(Cforms[f]),str(Cstems[s]) , str(Cforms[f] / Cstems[s])]))



if __name__ == "__main__":
    main()