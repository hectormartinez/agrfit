import argparse
from utils import *

#The ritter data have Petrov tags, we kind of circumvent the issue


def main():
    parser = argparse.ArgumentParser(description=")")
    parser.add_argument("infile",   metavar="FILE", help="name of the input file")
    args = parser.parse_args()


    fout = open(args.infile+".topos","w")
    foutannotations = open(args.infile+".annotations","w")


    outforms = []
    outannotations = []


    for lineidx,line in enumerate(open(args.infile).readlines()):

        try:
            idx,form,pos,frame,args = line.strip().split("\t")
        except:
             idx,form,pos,args = line.strip().split("\t")

        if idx == "1" and lineidx != 0:
            outforms.append(SENTENCEBOUNDARY+"\n")
            outannotations.append(SENTENCEBOUNDARY+"\n")

            #print(SENTENCEBOUNDARY)
        outforms.append(form+"\n")
        outannotations.append("\t".join([pos,frame])+"\n")

    fout.writelines(outforms)
    fout.close()
    foutannotations.writelines(outannotations)
    foutannotations.close()


if __name__ == "__main__":
    main()