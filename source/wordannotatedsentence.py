import networkx as nx
from nltk.corpus import framenet as fn


#A class for a sentence with ONE annotated word, maps to one instance wrt to training or testing
#If a sentence has N words in the annotated data, it should yield N instances of this class

class WordAnnotatedSentence:
    def __init__(self, textlist=None, postags=None, heads=None, deprels=None, headwordindex=None, annotations=None, id_=None,extra=None):
            self.forms = [""]+textlist
            self.postags = ["ROOT"]+postags
            self.heads = [""]+heads
            self.deprels = [""]+deprels
            self.headwordindex = headwordindex
            self.id_ = id_
            self.annotations = annotations
            self.extra = extra
            self.parsetree = None

            assert len(self.forms) == len(self.postags)
            assert len(self.forms) == len(self.heads)
            assert len(self.forms) == len(self.deprels)

            self.dep_parse()

    def dep_parse(self):
        sent = nx.DiGraph()

        sent.add_node(0, {'form': 'ROOT', 'pos': 'ROOT'})
        for i in range(1, len(self.forms)):
            sent.add_node(i, {'form': self.forms[i],
                              'pos': self.postags[i]
                              })
            sent.add_edge(self.heads[i], i, deprel=self.deprels[i])

        self.parsetree = sent


def listOfWordAnnotatedSenteces(textlist,postags,heads,deprels,headwordindex,annotations,extra):
     #The list of words that have received an annotation
    s=[]
    for currentid,idvalue in enumerate(headwordindex):
        if idvalue != "_":
            extradict = dict([x.strip().split(":") for x in extra[currentid].split(",")])
            #print(extradict)

            s.append(WordAnnotatedSentence(textlist,postags,heads,deprels,headwordindex=currentid+1,annotations=annotations[currentid].split(","),id_=idvalue,extra=extradict))
    return s


def readsentences(infile):
    s = []
    textlist=[]
    postags=[]
    heads=[]
    deprels=[]
    headwordindex=[]
    annotations=[]
    extra=[]

    for line in open(infile).readlines()+[""]:
        line = line.strip()
        if line:
            wordindex, form,pos,head,deplabel,currentid,currentanno,currentextra = line.split("\t")
            textlist.append(form)
            postags.append(pos)
            heads.append(int(head))
            deprels.append(deplabel)
            annotations.append(currentanno)
            headwordindex.append(currentid) #This is for the zero offset
            extra.append(currentextra)

        else:
            s.extend(listOfWordAnnotatedSenteces(textlist,postags,heads,deprels,headwordindex,annotations,extra))
            textlist=[]
            postags=[]
            heads=[]
            deprels=[]
            headwordindex=[]
            annotations=[]
            extra=[]


    return s