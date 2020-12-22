from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView as tv
from django.urls import path, re_path,include
from django.shortcuts import redirect
from gamehouse.sadm.views import juegos

urlpatterns = [
  ]

"""
    path('<administrador>/videojuegos',login_required(juegos.lista_videojuegos), name='lista_videojuegos'),####################################/sadm/<administrador>/videojuegos   mostrar lista de videojuegos
    path('g_videojuegos/editar_J/<int:id>/', views.editar_J, name='editar_J'),##################################/sadm/<administrador>/videojuegos/<Int: id_juego >    editar juego con id id_juego
    path('g_videojuegos/eliminar_J/<int:id>/', views.eliminar_J, name='eliminar_J'),############################/sadm/<administrador>/videojuegos/<Int: id_juego >/eliminar   Borrar juego con id_juego         modificar con un alert
    path('g_videojuegos/r_videojuegos/', views.registro_videojuegos, name='r_videojuegos'),#####################/sadm/<administrador>/videojuegos/nuevo         Agregar un juego nuevo
    path('g_videojuegos/agregar_vector/', views.agregar_vector, name='agregar_vector'),######################### Calcula los vectores Binarios de todos los videojuegos
    path('g_videojuegos/aceptado', views.aceptado, name='aceptado'),############################################Preview del juego aceptado       
    path('g_usuarios/', views.gestion_usuarios, name='g_usuarios'),#############################################/sadm/<administrador>/jugadores  mostrar lista de jugadores
    path('g_usuarios/r_usuarios/',views.registro_usuarios, name='r_usuarios'),##################################/sadm/<administrador>/jugadores/registro      Registrar un usuario
    path('g_usuarios/eliminar_usuarios/<int:id>/',views.eliminar_usuarios, name='eliminar_usuarios'),###########/sadm/<administrador>/jugadores/<Int: id_juego >/eliminar     Eliminar un usuario con id_jugador
    path('g_usuarios/e_usuarios/<int:id>/',views.editar_usuarios, name='e_usuarios'), ##########################/sadm/<administrador>/jugadores/<Int: id_juego >              Editar un usuario con id_jugador
    path('regresar_adm/',views.regresar_adm, name='regresar_adm'),##############################################Hay que borrarla
    path('g_GP/', views.gestion_GP, name='g_GP'),###############################################################/sadm/<administrador>/genero_plataforma   mostrar lista de generos y plataformas
    path('g_usuarios/r_GP/',views.registro_GP, name='r_GP'),####################################################/sadm/<administrador>/genero_plataforma/registro      registro de generos y plataformas
    path('perfil_adm',login_required(views.perfil_adm), name='perfil_adm'),#####################################/sadm/<administrador>     Mostrar el inicio del administrador
    path('g_usuarios/eliminar_P/<int:id>/', views.eliminar_P, name='eliminar_P'),###############################/sadm/<administrador>/plataforma/<Int: id_plataforma >/eliminar   Eliminar plataforma
    path('g_usuarios/e_P/<int:id>/', views.editar_P, name='e_P'),###############################################/sadm/<administrador>/plataforma/<Int: id_plataforma >          Editar plataforma
    path('g_usuarios/eliminar_G/<int:id>/', views.eliminar_G, name='eliminar_G'),###############################/sadm/<administrador>/genero/<Int: id_genero >/eliminar         Eliminar genero
    path('g_usuarios/e_G/<int:id>/', views.editar_G, name='e_G'),###############################################/sadm/<administrador>/genero/<Int: id_genero >                  Editar genero
    path('VCPU/', views.ViewcaracteristicasPU, name='ViewcaracteristicasPU'),################################### Ver las lista de vectores de los Usuario 
    path('VCDE/', views.ViewcaracteristicasDE, name='ViewcaracteristicasDE'),###################################Ver la lista de vectores de caracteristicas Descriptivas de cada usuario
    """
