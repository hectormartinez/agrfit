import argparse


def main():
    parser = argparse.ArgumentParser(description="Rewrite Semafor input to annotation format")
    parser.add_argument("inform",  metavar="FILE", help="")
    parser.add_argument("instem",  metavar="FILE", help="")
    parser.add_argument("outdict",  metavar="FILE", help="")
    args = parser.parse_args()
    for lineform, linestem in zip(open(args.inform).readlines(),open(args.instem).readlines())[:30]:
        print(lineform.split(" "))
        print(linestem.split(" "))
        print(len(lineform.split(" ")),len(linestem.split(" ")))



if __name__ == "__main__":
    main()