from datetime import datetime
from gamehouse.sadm.models import Tf_Idf
from gamehouse.sjug.models import Juego
from apscheduler.schedulers.background import BackgroundScheduler


#https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata
def auto_limpiar_descripciones():
    """ Ejecutar antes de calcular vectores tf-idf """
    sucios = Juego.objects.filter(descripcion_limpia = None)
    if len(sucios) > 0:
        print("Limpieza automatica de descripciones...")
        print("Se encontraron "+str(len(sucios))+" juegos sin descripcion limpia")
        for sucio in sucios:
            sucio.descripcion_limpia = None
            sucio.save()
    """ Version manual 
    from gamehouse.algorithms.tf_idf import clean_description
    for sucio in sucios:
        sucio.descripcion_limpia = clean_description(sucio.descripcion)
        sucion.save()
    """
    return


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