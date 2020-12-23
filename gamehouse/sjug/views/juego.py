'''
Created on 20/12/2020

@author: mimr
'''
from django.shortcuts import render, get_object_or_404
from gamehouse.sjug.models import Jugador,Usuario,Juego,Imagen
from django.http import Http404


def default(request):
    return render(request,'jugador/sjug.html')

"""  Vistas de interaccion jugador-juego """
#no hecha
def opiniones(request,jugador):
    return render(request,'pruebas/dashboard.html',{})

