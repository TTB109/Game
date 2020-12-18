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

from gamehouse.sjug import views as sjug_views
from gamehouse.sadm import views as sadm_views

urls_juegos = [
    #path("",tv.as_view(template_name="juegos/juego.html"), name="juegos"),
    path("consolas/",tv.as_view(template_name="juegos/consolas.html"), name="consolas"),
    path("generos/",tv.as_view(template_name="juegos/generos.html"), name="generos"),
    path('InfConsolas/',tv.as_view(template_name="juegos/InfoConsolas.html"), name='InfConsolas'),
    path('InfGeneros/', tv.as_view(template_name="juegos/InfoGeneros.html"), name='InfGeneros'),  
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tv.as_view(template_name="homepage.html"), name='index'),
    path('login/',sjug_views.perfil, name='login'),
    path('registro/', sjug_views.registro, name= 'registro'),
    path('login/perfil/',include('gamehouse.sjug.urls')),
    path('login/perfil/',include('gamehouse.sadm.urls')),
    re_path(r'^juegos/',include(urls_juegos)),
    path('operacion/',tv.as_view(template_name="operacion.html"),name="operacion-exitosa"),      
]
