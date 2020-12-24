import nltk
from nltk.corpus import cess_esp
from pickle import dump

patterns = [ (r".*o$","NMS"),
               (r".*os$","NMP"),
               (r".*a$","NFS"),
               (r".*as$","NFP"),
             ]
cesp_tsents = cess_esp.tagged_sents()
td = nltk.DefaultTagger("s")
tr = nltk.RegexpTagger(patterns, backoff = td )
tu = nltk.UnigramTagger(cesp_tsents, backoff = tr )
output = open("tagger.pkl","wb")
dump(tu,output,-1)
output.close()
