# Python program to read
import os
import re
import sqlite3 

if __name__ == "__main__":
  queries = [ "INSERT INTO sjug_genero (nombre,descripcion) VALUES (?,?)",
              "INSERT INTO sjug_compania (nombre,descripcion) VALUES(?,?)",
	      "INSERT INTO sjug_plataforma (nombre,descripcion) VALUES(?,?)"]

  ####Conexion a base d datos
  conn = sqlite3.connect("gamehouse.db")
  ###Insercion
  data_folder = "Base/"
  for filename in os.listdir(data_folder): #Open each file
    conn = sqlite3.connect("gamehouse.db")
    document_name = data_folder + filename
    document = open(document_name, encoding = "utf-8")
    data_list = document.readlines() #Take the document as list
    document.close()
    ### [titulo,compania,anio,genero,plataforma,descripcion,imagen]
    cr = conn.cursor()
    for data in data_list: #For each line in the list
     data = data.strip() ##Remove blank spaces
     data = data.replace("\n","") ##Remove new line characters
     if(filename == "generos.txt"):
       t = (data,"Texto por defecto")
       cr.execute(queries[0],t)
     if(filename == "companias.txt"):
       t = (data,"Texto por defecto")
       cr.execute(queries[1],t)
     if(filename == "plataformas.txt"):
       t = (data,"Texto por defecto")
       cr.execute(queries[2],t)
    cr.close()
    conn.commit()
    conn.close()

  """
  cr = conn.cursor()
  for row in cr.execute("SELECT * FROM sjug_genero"):
    print(row)
  conn.commit()
  conn.close()
  """
