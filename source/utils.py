__author__ = 'alonso'

SENTENCEBOUNDARY="<SENTENCEBOUNDARY>"
apostrophelist = "'s n't 'm 'll 've 're 'd".split(" ")
NIVRETAGS=["ADJ","ADP","ADV","AUX","CONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","PUNCT","SCONJ","SYM","VERB","X"]
PETROVTAGS=["ADJ","ADP","ADV","CONJ","DET","NOUN","NUM","PRON","PRT","VERB","X"]

PETROVTONIVREMAP = {}
PETROVTONIVREMAP["PRT"]="PART"
PETROVTONIVREMAP["."] = "PUNCT"
PREFERNIVRETAG=[("NOUN","PROPN"),("VERB","AUX"),("X","INTJ")]



def cleanheadword(s,key=None):
    s = s.strip()
    if len(s.split(" ")) != 1:
            return None
    outs=""
    for c in s:
        if c.isalpha():
            outs+=c
    if len(outs)==0:
        return None
    return outs

def tokenizestring(s):
    s=s.replace("’","'").replace("“","\"").replace("”","\"").replace(" "," ").replace("."," . ").replace("."," . ").replace("“","\"").replace("`","\"").replace("/"," / ")
    s=s.replace("["," [").replace("("," ( ").replace("]"," ] ").replace(")"," ) ")
    s=s.replace(","," , ").replace("-"," - ").replace(":"," : ").replace(";"," ; ").replace("!"," ! ").replace("?"," ? ").replace("\""," \" ").replace("  "," ")
    s=s.replace("'s"," 's ").replace("n't"," n't ").replace("'m"," 'm ").replace("'ll"," 'll ").replace("'ve"," 've ").replace("'re"," 're ").replace("'d "," 'd ").replace("  "," ")
    tokenized = [x for x in s.strip().split(" ") if x]
    o = []
    for t in tokenized:
        if "'" in t and t not in apostrophelist:
            t = t.replace("'","")
        o.append(t)
    return o


def padline(stringlist):
    return [x+"\n" for x in stringlist if x]