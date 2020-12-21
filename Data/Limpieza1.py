# Python program to read
import os
import re
import sqlite3 

if __name__ == "__main__":
    document_name = "mini.txt"
    document = open(document_name, encoding = "utf-8")
    games = document.read() #Take the document as a simple string
    document.close()
    while games != "":
        if(games == "\n"):
            break
        
