from gamehouse.sjug.models import Juego
from django.core.exceptions import PermissionDenied

## /sadm/adan/videojuegos
## /sadm/mimir/videojuegos
def lista_videojuegos(request,administrador):
    # administrador es igual a adan
    try:
        solicitado = Administrador.objects.get(nombre = administrador)
        if user.get_username() == solicitado.username: ## Tengo iniciada una sesión de adm
            juegos = Juegos.objects.all()    
            return render(request,'adm/juegos/videojuegos.html',{'juegos':juegos})    
        else:# Tengo iniciada sesión como jugador normal
            print("No tienes permisos!!")
            raise PermissionDenied # Error 403 forbidden
            
             
    except Jugador.DoesNotExist:
        raise Http404("Ese administrador no existe!")
            
    """
        {% if user.is_authenticated %}
        # only owner can view his page
        
    
  VJuegos=Juego.objects.all()
  # for game in VJuegos:
  #   print(game.generos)
  myFilter=JuegoFilter(request.GET,queryset=VJuegos)
  VJuegos=myFilter.qs

  paginator=Paginator(VJuegos,10)
  page=request.GET.get('page')
  try:
    posts=paginator.page(page)
  except PageNotAnInteger:
    posts=paginator.page(1)
  except EmptyPage:
    posts=paginator.page(paginator.num_pages)

  return render(request,'adm/gestion_videojuego.html',{'fVJuegos':posts,'myFilter':myFilter,'page':page})
  """