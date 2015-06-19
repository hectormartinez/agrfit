import argparse
from utils import *

#The ritter data have Petrov tags, we kind of circumvent the issue

parser = argparse.ArgumentParser(description=")")
parser.add_argument("infile",   metavar="FILE", help="name of the input file")
args = parser.parse_args()




for lineidx,line in enumerate(args.open(args.infile).readlines()):
    idx, form, petrovpos, frame, args = line.split("\t")
    if idx == "1" and lineidx != 0:
        print(SENTENCEBOUNDARY)
    print(form)

