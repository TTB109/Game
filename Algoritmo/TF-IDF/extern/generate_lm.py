def get_lemmas_dictionary(file_name):
    file = open(file_name, encoding = "latin-1")
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    lemmas = {}
    for line in lines:
        if line != "":
            words = line.split() #List with splited line
            words = [w.strip() for w in words]
            wordform = words[0]
            wordform = wordform.replace("#","")
            lemmas[wordform] = words[-1]
    return lemmas


def save_lemmas_dictionary(lemmas): #mas rapido que guardar diccionario o en el tiempo de ejecucion
    from pickle import dump
    output = open('olemmas.pkl','wb') #web -- write bytes
    dump(lemmas,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
    output.close()
   
if __name__=='__main__':
    fname = "./generate.txt" #ruta archivo lemmas
    lemmas = get_lemmas_dictionary(fname)
    save_lemmas_dictionary(lemmas)
