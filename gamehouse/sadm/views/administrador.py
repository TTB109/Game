from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect,render,get_object_or_404
from gamehouse.sjug.models import *
#from .forms import Administrador
from gamehouse.sjug.filters import JuegoFilter

def perfil_adm(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        if user.get_username() == solicitado.username: ## Tengo iniciada una sesión de adm
            return render(request,'adm/perfil_adm.html')       
                
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")

def signout(request,administrador):
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        if user.get_username() == solicitado.username: ## Tengo iniciada una sesión de adm
            logout(request)
            return redirect('/')            
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")