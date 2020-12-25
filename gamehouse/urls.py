"""gamehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.views.generic import TemplateView as tv
from django.urls import path, include, re_path,reverse

from gamehouse.sjug.views import universales


urls_universales = [
    path('', tv.as_view(template_name="homepage.html"), name='index'),  
    path('login/',universales.login, name='login'),
    path('registro/', universales.registro, name= 'registro'),
    path('logout/',universales.logout, name='logout'), 
    path('error/403',universales.solicitud_denegada,name='error_403'),
    path('error/404',universales.no_encontrado,name='error_404'),
    
    path('consolas/',tv.as_view(template_name="juegos/consolas.html"), name="consolas"),
    path('generos/',tv.as_view(template_name="juegos/generos.html"), name="generos"),
    path('InfConsolas/',tv.as_view(template_name="juegos/InfoConsolas.html"), name='InfConsolas'),
    path('InfGeneros/', tv.as_view(template_name="juegos/InfoGeneros.html"), name='InfGeneros'),
    
    #path('juegos/',universales.juegos,name = 'juegos'),
    #path('juegos/<int:id_juego>',universales.ver_juego,name='ver_juego')
]
urlpatterns = [
    path('',include(urls_universales)),
    path('sjug/',include('gamehouse.sjug.urls')),
    path('sadm/',include('gamehouse.sadm.urls')),
    #path('admin/', admin.site.urls)   
]

