from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView as tv
from django.urls import path, re_path,include
from django.shortcuts import redirect
from gamehouse.sadm.views import juegos

urlpatterns = [
    path('<administrador>/videojuegos',login_required(juegos.lista_videojuegos), name='lista_videojuegos'),####################################/sadm/<administrador>/videojuegos   mostrar lista de videojuegos
  ]
