'''
Created on 20/12/2020

@author: mimr
'''
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from gamehouse.sjug.models import Jugador,Usuario,Juego,Imagen
from gamehouse.sjug.forms import UserForm,UsuarioForm,JugadorForm
from django.http import Http404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import random


""" Vistas de perfil """
def perfil(request,jugador):
    try:
        solicitado = Jugador.objects.get(nickname = jugador)
        return render(request,'jugador/perfil.html',{'jugador':solicitado})     
    except Jugador.DoesNotExist:
        return redirect('error_404')

   
@login_required()
def editar_perfil(request,jugador):
    try:
        jugador = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')    
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance = request.user)
            usuario_form = UsuarioForm(request.POST, instance = jugador.usuario)
            jugador_form = JugadorForm(request.POST, instance = jugador)
            if user_form.is_valid():
                usuario_form.save() #Por el momento solo actualiza usuario
                return redirect('/sjug/'+jugador.nickname+'/')
            else:
                return render(request,'jugador/editar_jugador.html',{'fusuario':usuario_form, 'fuser':user_form, 'fjugador':jugador_form})
        else:
            user_form = UserForm(instance = request.user)
            usuario_form = UsuarioForm(instance = jugador.usuario)
            jugador_form = JugadorForm(instance = jugador)
            return render(request,'jugador/editar_jugador.html',{'fusuario':usuario_form, 'fuser':user_form, 'fjugador':jugador_form})
    except Jugador.DoesNotExist:
        return redirect('error_404')

#no hecha
@login_required()
def eliminar_perfil(request,jugador):
    try:
        jugador = Jugador.objects.get(nickname = jugador)
        if request.user.get_username() != jugador.nickname:
            return redirect('error_403')    
        if request.method == 'POST':
            usuario = jugador.usuario
            user = request.user
            auth_logout(request)
            jugador.delete()
            usuario.delete()
            user.delete()
            return redirect('index')
        else:
            return render(request,'jugador/eliminar_jugador.html')
    except Jugador.DoesNotExist:
        return redirect('error_404')

"""
def eliminar(request,id):
  try:
    usuario=get_object_or_404(Usuario,id=id)
    userio=get_object_or_404(User,id=id)
    jugador=get_object_or_404(Jugador,usuario=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method=="POST":
    jugador.delete()
    userio.delete()
    usuario.delete()
    return redirect('index')
  else:
    return render(request,'jugador/eliminar.html')


"""


#no hecha
@login_required()
def mis_gustos(request,jugador):
    if request.user.get_username() != jugador:
        return redirect('error_403')
    else:
        solicitado = get_object_or_404(Jugador, nickname = jugador)
    juegos = juegos_random()
    return render(request,'jugador/dashboard.html',{'juegos' : juegos})


@login_required(login_url='/login')
def dashboard(request,jugador):
    if request.user.get_username() != jugador:
        return redirect('error_403')
    else:
        solicitado = get_object_or_404(Jugador, nickname = jugador)
    juegos = juegos_random()
    return render(request,'jugador/dashboard.html',{'juegos' : juegos})


def ver_juego(request,juego=0):
    print("Llegue")
    solicitado = get_object_or_404(Juego, id_juego = juego)
    print("VEr juego:",solicitado)
    return render(request,'jugador/perfil.html',{'juego':solicitado})


""" Vistas para recomendacion """
@login_required(login_url='/')
def tf_idf(request,jugador):
    return render(request,'jugador/recomendacion/tf_idf.html')

    """
        {% if user.is_authenticated %}
        # only owner can view his page
        if self.request.user.get_username() == object.username:
            return object
        else:
            # redirect to 404 page
            print("you are not the owner!!")
    """
    """
    if request.user.is_authenticated:
    else:
    nickname = request.user.get_username()
    """     

""" Funciones que no son puntos de URL """

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
