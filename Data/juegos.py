# Python program to read
import re
import sqlite3 
import os

if __name__ == "__main__":
  data_folder = "Data/"
  base_folder = "Salida/"
  ####Conexion a base d datos
  #conn = sqlite3.connect("gamehouse.db")

  queries = [ "INSERT INTO sjug_juego (titulo,descripcion,agnio) VALUES (?,?,?)",
  ###OBTENER ID DEL JUEGO
  "SELECT id_juego FROM sjug_juego WHERE titulo = ?",#Obtener id_juego

  ####### INSERTAR GENERO
  "SELECT id_genero FROM sjug_genero WHERE nombre LIKE ?",#Obtener id de cada genero que tiene el juego
  "INSERT INTO sjug_GenerosAsociados (juego,genero) VALUES (?,?)", #Mandar ids

  ####### INSERTAR PLATAFORMA
  "SELECT id_plataforma FROM sjug_plataforma WHERE nombre LIKE ?",
  "INSERT INTO sjug_PlataformasAsociadas (juego,plataforma) VALUES (?,?)",
  ########"INSERT INTO sjug_plataformas_asociadas (juego,plataforma) VALUES (?,?)",
  ####### INSERTAR COMPANIA
  "SELECT id_compania FROM sjug_compania WHERE nombre LIKE ?",
  "INSERT INTO sjug_CompaniasAsociadas (juego,compania) VALUES (?,?)",

  ####### INSERTAR IMAGEN
  "INSERT INTO sjug_imagen (referencia,alt,juego) VALUES (?,?,?)"
  ]
 
  for filename in os.listdir(data_folder): #Open each file
    conn = sqlite3.connect("gamehouse.db")
    document_name = data_folder + filename
    document = open(document_name, encoding = "utf-8")
    #document = open(document_name, encoding = "utf-8")    
    games = document.read() #Take the document as a simple string
    document.close()
    cr = conn.cursor()
    while games != "":
      if(games == "\n"):
        break
      ### [titulo,compañia,año,genero,plataforma,descripcion,imagen, resto_del_texto]
      splited = games.split("|",7)
      splited[0] = splited[0].strip()
      splited[1] = splited[1].strip()
      games = splited[7] ##Resto cadena
      ###LIMPIAR GENEROS 
      generos = list(set(splited[3].split(",")))
      generos = [genero.strip() for genero in generos] ##Remove whitespaces
      generos = [genero for genero in generos if genero] ## Remove empty elem.
      ###LIMPIAR PLATAFORMAS
      plataformas = list(set(splited[4].split(",")))
      plataformas = [plataforma.strip() for plataforma in plataformas]
      plataformas = [plataforma for plataforma in plataformas if plataforma]
      #### INSERCION DEL JUEGO
      t = (splited[0],splited[5],splited[2]) #tit.,descrip.,anio.
      cr.execute(queries[0],t)
      ### OBTENER ID JUEGO
      cr.execute(queries[1],(splited[0],))
      id_juego = cr.fetchone()[0] #Returns a row
      print("\n\n********INSERTANDO JUEGO********\n\n")
      print("Id del juego:",id_juego)
      print("Juego:"+splited[0])
      ### INSERCION DE LOS GENEROS
      print("\n----Insertando generos...")
      for genero in generos:
        cr.execute(queries[2],("%"+genero+"%",))
        id_genero = cr.fetchone()[0]
        t = (id_juego,id_genero)
        cr.execute(queries[3],t)
        print(genero+"("+str(id_genero)+") insertado!")
      ### INSERCION DE LAS PLATAFORMAS
      print("\n----Insertando plataformas...")
      for plataforma in plataformas:
        cr.execute(queries[4],("%"+plataforma+"%",))
        id_plataforma = cr.fetchone()[0]
        t = (id_juego,id_plataforma)
        cr.execute(queries[5],t)
        print(plataforma+"("+str(id_plataforma)+") insertada!")
      ### INSERCION DE LA COMPANIA
      print("\n----Insertando compania...")
      cr.execute(queries[6],("%"+splited[1]+"%",))
      id_compania = cr.fetchone()[0]
      t = (id_juego,id_compania)
      cr.execute(queries[7],t)
      print(splited[1]+"("+str(id_compania)+") insertada!")
      ### INSERCION DE LA IMAGEN
      print("\n----Insertando imagen...")
      t = (splited[6],"Alternativo por defecto",id_juego)
      cr.execute(queries[8],t)
      print("Imagen:"+splited[6]+"\nde id_juego:"+str(id_juego)+" insertada!")
      ### 
    cr.close()
    conn.commit()    
    conn.close()  
    
