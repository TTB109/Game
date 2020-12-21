'''
Created on 20/12/2020

@author: mimr
'''
from django.shortcuts import render, get_object_or_404, redirect
from gamehouse.sjug.models import Jugador,Usuario,Juego,Imagen
from django.http import Http404


def perfil(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        return render(request,'pruebas/perfil.html',{'jugador':solicitado})     
    except Jugador.DoesNotExist:
        raise Http404("El jugador que buscas no existe!")
            
    """
        {% if user.is_authenticated %}
        # only owner can view his page
        if self.request.user.username == object.username:
            return object
        else:
            # redirect to 404 page
            print("you are not the owner!!")
    """
     

def dashboard(request):
    contexto = {}
    contexto['juegos'] = juegos_random()
    
    """
    if request.user.is_authenticated:
    else:
    nickname = request.user.get_username()
    """
    print("QUedé xd")
    return render(request,'pruebas/dashboard.html',contexto)

def ver_juego(request,juego=0):
    print("Llegue")
    solicitado = get_object_or_404(Juego, id_juego = juego)
    print("VEr juego:",solicitado)
    return render(request,'pruebas/perfil.html',{'juego':solicitado})

def juegos_random():
    ##https://serpapi.com/images-results
    """ Esta funcion regresa pares juego, su imagen aleatorio """
    import random
    from django.core.exceptions import MultipleObjectsReturned
    disponibles = Juego.objects.all().count()  
    aleatorios = []
    for id_aleatorio in random.sample(range(0, disponibles), 12):
        juego = Juego.objects.get(id_juego = id_aleatorio)
        try:
            imagen = Imagen.objects.get(juego = id_aleatorio)
        except MultipleObjectsReturned:
            print("Excepcion generada:",MultipleObjectsReturned) 
            imagen = Imagen.objects.get(juego = id_aleatorio).first()[0]
        except Exception as e:
            print("Excepcion generada en inicio_jugador:",e)
            imagen = Imagen.objects.get(juego = 1)
        aleatorios.append((juego,imagen))
    return aleatorios
