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

def juegos(request):
    
    return render()

def ver_juego(request,juego):
  #Juego = Juego.objects.get(id_juego = juego)
  #imagen = Imagen.objects.get(id_imagen = juego)
  """
  if request.method == 'POST':
    opinion_form = OpinionForm(request.POST)
    if opinion_form.is_valid():
      rOpinion=opinion_form.save(commit = False)
      rOpinion.juego=Juego.objects.get(id_juego=id_juego)##############corregir con Jugador
      rOpinion.jugador=Jugador.objects.get(usuario=pk)##################corregir con Jugador
      rOpinion.gusto=request.POST.get('gusto')
      rOpinion.guion=request.POST.get('guion')
      rOpinion.artes=request.POST.get('artes')
      rOpinion.jugabilidad=request.POST.get('jugabilidad')
      rOpinion.tecnico=request.POST.get('tecnico')
      rOpinion.save()
      return redirect('VVJuego',id_juego=id_juego,pk=pk)
      #return redirect('regresar_user')
  else:
  """
  opinion_form = OpinionForm()
  VJuego = Juego.objects.get(id_juego=juego)
  imagen = Imagen.objects.get(id_imagen=juego)    
  return render(request,'juegos/juego.html',{'fopinion':opinion_form,'VJuego':VJuego,'fimagen':imagen})
  
