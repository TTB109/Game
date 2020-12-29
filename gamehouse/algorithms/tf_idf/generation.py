from pickle import dump

def generate_tagger(route):
	import nltk
	from nltk.corpus import cess_esp
	patterns = [ (r".*o$","NMS"),
               (r".*os$","NMP"),
               (r".*a$","NFS"),
               (r".*as$","NFP"),
             ]
	cesp_tsents = cess_esp.tagged_sents()
	td = nltk.DefaultTagger("s")
	tr = nltk.RegexpTagger(patterns, backoff = td )
	tu = nltk.UnigramTagger(cesp_tsents, backoff = tr )
	output = open(route+'tagger.pkl','wb')
	dump(tu,output,-1)
	output.close()


def generate_lemmas(route):
    source = route + 'source_lemmas.txt'
    doc = open(source, encoding = "latin-1")
    lines = doc.readlines()
    doc.close()
    lines = [line.strip() for line in lines]
    lemmas = {}
    for line in lines:
        if line != "":
            words = line.split() #List with splited line
            words = [w.strip() for w in words]
            wordform = words[0]
            wordform = wordform.replace("#","")
            lemmas[wordform] = words[-1]
    output = open(route+'lemmas.pkl','wb') #web -- write bytes
    dump(lemmas,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
    output.close()
