from datetime import datetime
from gamehouse.sadm.models import Tf_Idf
from apscheduler.schedulers.background import BackgroundScheduler


#https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata

def vect_desc():
    """ Esta funcion calcula el vector tf-idf de las 
        descripciones de todos los juegos que existen
    
    primero = Tf_Idf.objects.first()
    if primero: #Si existe algun vector
    else
    """
    return

def prueba():
    print("Ejecutada")
    return

""" Funciones para iniciar el segundo plano """



def start_vect_desc():
    scheduler = BackgroundScheduler(daemon = True)
    scheduler.add_job(vect_desc, 'interval', days=5) #days, weeks, hours, minutes, seconds
    scheduler.start()
    return

def start_prueba():
    scheduler = BackgroundScheduler(daemon = True)
    scheduler.add_job(prueba, 'interval', seconds=30) #days, weeks, hours, minutes, seconds
    scheduler.start()
    return