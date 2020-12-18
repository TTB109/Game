from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView as tv
from django.urls import path, re_path,include
from django.shortcuts import redirect
from gamehouse.sjug import views

urlpatterns = [
    path('mis_gustos/<int:id_gustos>/',login_required(views.mis_gustos), name='mis_gustos'),    
    path('mis_gustos/mis_gustos_2/<int:id>/',login_required(views.mis_gustos_2), name='mis_gustos_2'),
    path('mis_gustos/mis_gustos_2/eliminar_juego/<int:id>/<int:pk>/',login_required(views.eliminar_juego), name='eliminar_juego'),
    path('mis_gustos/mis_gustos_2/agregar_juego/<int:id>/<int:pk>/',login_required(views.agregar_juego), name='agregar_juego'),
    path('mis_opiniones/<int:id>/',login_required(views.mis_opiniones), name='mis_opiniones'),
    path('edit_perfil/<int:id>/',login_required(views.edit_perfil), name='edit_perfil'),
    path('eliminar/<int:id>/',login_required(views.eliminar), name='eliminar'),
    path('',login_required(views.perfil_user), name='perfil_user'),
    path('regresar_user/',login_required(views.regresar_user), name='regresar_user'),
    path('iusuario/',login_required(views.iusuario), name='iusuario'),
    path('VVJuego/<int:id_juego>/<int:pk>/',login_required(views.VVJuego), name='VVJuego'),
    path('MiLista/<int:id>/',login_required(views.MiLista), name='MiLista'),
    path('caracteristicasDE/<int:id>/',login_required(views.caracteristicasDE), name='caracteristicasDE'),
    path('InicioCDE/<int:id>/',login_required(views.InicioCDE), name='InicioCDE'),
    path('prueba/',views.prueba,name="prueba"),  
    ###########################################################
    ###########################################################
    path('e_perfil/', views.editar_perfil, name='e_perfil'),
    path('g_usuarios/', views.gestion_usuarios, name='g_usuarios'),
    path('g_GP/', views.gestion_GP, name='g_GP'),
    path('g_videojuegos/', views.gestion_videojuegos, name='g_videojuegos'),
    path('g_videojuegos/editar_J/<int:id>/', views.editar_J, name='editar_J'),
    path('g_videojuegos/eliminar_J/<int:id>/', views.eliminar_J, name='eliminar_J'),
    path('g_videojuegos/r_videojuegos/', views.registro_videojuegos, name='r_videojuegos'),
    path('g_videojuegos/agregar_vector/', views.agregar_vector, name='agregar_vector'),  
    path('g_videojuegos/aceptado', views.aceptado, name='aceptado'),
    path('g_usuarios/r_usuarios/',views.registro_usuarios, name='r_usuarios'),
    path('g_usuarios/eliminar_usuarios/<int:id>/',views.eliminar_usuarios, name='eliminar_usuarios'),
    path('g_usuarios/e_usuarios/<int:id>/',views.editar_usuarios, name='e_usuarios'),  
    path('regresar_adm/',views.regresar_adm, name='regresar_adm'),
    path('g_usuarios/r_GP/',views.registro_GP, name='r_GP'),
    path('perfil_adm',login_required(views.perfil_adm), name='perfil_adm'),
    path('g_usuarios/eliminar_P/<int:id>/', views.eliminar_P, name='eliminar_P'),
    path('g_usuarios/e_P/<int:id>/', views.editar_P, name='e_P'),
    path('g_usuarios/eliminar_G/<int:id>/', views.eliminar_G, name='eliminar_G'),
    path('g_usuarios/e_G/<int:id>/', views.editar_G, name='e_G'),
    path('VCPU/', views.ViewcaracteristicasPU, name='ViewcaracteristicasPU'),  
    path('VCDE/', views.ViewcaracteristicasDE, name='ViewcaracteristicasDE'),  
    ###########################################################
    ###########################################################
    path('signout/',views.signout, name = 'signout'),
    path('Busqueda/',views.Busqueda, name = 'Busqueda'),
  ]
