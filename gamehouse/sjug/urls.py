from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView as tv
from django.urls import path, re_path,include
from django.shortcuts import redirect

from gamehouse.sjug.views import jugador as sjug_jugador


"""
CAMBIOS:
ACTUAL | CAMBIO | DESCRIPCION

mis_gustos/<int:id_gustos>/ | /sjug/<jugador>/gustos | Mostrar tres botones: Modificar mis generos, Modificar mis plataformas y Modificar mis juegos
mis_gustos/mis_gustos_2/<int:id>/ | indicado | Mostrar lista mis de juegos, un buscador de juegos y sus opciones añadir, ver y quitar
VVJuego/<int:id_juego>/<int:pk> 
juegos/<int:id_juego>


PENDIENTES:

/sjug/<jugador>/opinion/<int:id_opinion>  Muestra la opinion con id_opinion del jugador indicado
/sjug/<jugador>/opinion/<slug: juego_buscado> Buscar opiniones de la lista de opiniones del jugador indicado cuyo videojuego sea el del slug
                                              Por ejemplo /sjug/Mimir/opinion/grand-theft-auto busca opiniones que tengan que ver con GTA
/sjug/<jugador>/opinion/<int:id_opinion>/eliminar    

 path('',sjug_jugador.inicio ,name="inicio_jugador"), ## /sjug/  
    path('<jugador>/',sjug_jugador.perfil,name='perfil1'), ## /sjug/<jugador> Ver y modificar perfil del jugador
    path('<jugador>/dashboard/',sjug_jugador.dashboard,name="dashboard"), ### /sjug/<jugador>/dashboard  Presentación de recomendaciones
    path('<slug:juego_slug>/',sjug_views.juegotal,name="juego"),
"""

#/sjug/
urlpatterns = [
   
]
