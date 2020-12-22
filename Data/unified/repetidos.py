"""
https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
splited[0] --> titulo
splited[1] --> compañia
splited[2] --> año
splited[3] --> genero
splited[4] --> plataforma
splited[5] --> descripcion
splited[6] --> imagen
splited[7] --> resto_del_texto

"""

if __name__ == "__main__":
    document_name = "unified/plataformas.txt"
    document = open(document_name,encoding = "utf-8")
    lineas = document.readlines() #Ya es una lista de strings
    document.close()
    lineas_set = set(lineas)
    print("Longitud:",len(lineas))
    print("Longitud del set:",len(lineas_set))
    print("Diferencia:",len(lineas)-len(lineas_set))
    """
    #document_name = "unified/gameset.txt"
    document = open(document_name, encoding = "utf-8")
    games = document.read() #Take the document as a simple string
    document.close()
    while games != "":
        if(games == "\n"):
            break
        splited = games.split("|",7)
        games = splited [7]
        splited = splited[0:7]
        
        titulos.append(splited[0])
        companias.append(splited[1])
        anios.append(splited[2])
        generos.extend(splited[3].split(","))
        plataformas.extend(splited[4].split(","))

        
        splited = "|".join(splited) + "|"
        concentrado.write(splited)
    """