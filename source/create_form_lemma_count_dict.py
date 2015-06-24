import argparse


def isvalid(s):
    current = s.replace("@","A").replace("~","0").replace("-","1").replace("/","2").replace(".","3").replace("_","4")
    return current.isalpha() or current.isnum() or current.isalnum()

def contentlist(s):
    return [x for x in s.replace("\n","").split(" ") if x.isvalid()]

def main():
    parser = argparse.ArgumentParser(description="Rewrite Semafor input to annotation format")
    parser.add_argument("inform",  metavar="FILE", help="")
    parser.add_argument("instem",  metavar="FILE", help="")
    parser.add_argument("outdict",  metavar="FILE", help="")
    args = parser.parse_args()
    for lineform, linestem in zip(open(args.inform).readlines()[:30],open(args.instem).readlines()):
        print(contentlist(lineform))
        print(contentlist(linestem))
        print(len(contentlist(linestem)),len(contentlist(lineform)))



if __name__ == "__main__":
    main()