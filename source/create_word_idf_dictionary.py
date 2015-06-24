import argparse
from collections import Counter
from utils import *
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    parser = argparse.ArgumentParser(description="IDF from corpus")
    parser.add_argument("inform",  metavar="FILE", help="")
    args = parser.parse_args()

    textlist=[]
    for lineform in zip(open(args.inform).readlines()[:30]):
        formlist=(contentlist(lineform))
        textlist.append(formlist)

    tv=TfidfVectorizer(analyzer=lambda x:x)
    tv.fit(textlist)
    for name, idf in zip(tv.get_feature_names(), tv.idf_):
        print(name+"\t"+str(idf))



if __name__ == "__main__":
    main()