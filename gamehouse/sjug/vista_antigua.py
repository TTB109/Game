
"""
path('login/perfil/',include('gamehouse.sjug.urls')),
path('login/perfil/',include('gamehouse.sadm.urls')),

urlpatterns = [
    path('mis_gustos/<int:id_gustos>/',login_required(views.mis_gustos), name='mis_gustos'),  ### /sjug/<jugador>/gustos Ver y modificar generos y plataformas
    path('mis_gustos/mis_gustos_2/<int:id>/',login_required(views.mis_gustos_2), name='mis_gustos_2'), ### /sjug/<jugador>/gustos/juegos Ver, añadir, o modificar mis juegos preferidos  
    path('mis_gustos/mis_gustos_2/eliminar_juego/<int:id>/<int:pk>/',login_required(views.eliminar_juego), name='eliminar_juego'),  ### /sjug/<jugador>/gustos/juegos/<int:id_juego>/eliminar  
    path('mis_gustos/mis_gustos_2/agregar_juego/<int:id>/<int:pk>/',login_required(views.agregar_juego), name='agregar_juego'),  ### /sjug/<jugador>/gustos/juegos/<int:id_juego>/agregar 
    path('mis_opiniones/<int:id>/',login_required(views.mis_opiniones), name='mis_opiniones'),  ### /sjug/<jugador>/opinion  Muestra lista de opiniones hechas por el jugador indicado
    path('eliminar/<int:id>/',login_required(views.eliminar), name='eliminar'), ### /sjug/<jugador>/eliminar
    path('',login_required(views.perfil_user), name='perfil_user'),  ### /sjug/<jugador> Ver perfil con opciones
    path('regresar_user/',login_required(views.regresar_user), name='regresar_user'), ### Borrar después mand inicio
    path('VVJuego/<int:id_juego>/<int:pk>/',login_required(views.VVJuego), name='VVJuego'), ### juegos/
    path('MiLista/<int:id>/',login_required(views.MiLista), name='MiLista'), ## Mis opniones cambiar a anterior
    path('caracteristicasDE/<int:id>/',login_required(views.caracteristicasDE), name='caracteristicasDE'),  ###   /sjug/<jugador>/gustos/CDE    
    path('InicioCDE/<int:id>/',login_required(views.InicioCDE), name='InicioCDE'), ### registro/CDE
    #path('prueba/',views.prueba,name="prueba"),  
    ###########################################################
    ###########################################################
    
    ###########################################################
    ###########################################################
    path('signout/',views.signout, name = 'signout'),
    path('Busqueda/',views.Busqueda, name = 'Busqueda'),
  ]

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.urls import reverse, reverse_lazy
from .models import *
from gamehouse.sadm.models import *
from .forms import UsuarioForm,JugadorForm,UserForm,GeneroForm,PlataformaForm,JuegoForm,OpinionForm,JuegosFavoritosForm,ImagenForm,CompaniaForm,MisGustosForm,CdeForm,CpuForm
from .filters import JuegoFilter

import random
from scipy import spatial
from django.core.exceptions import MultipleObjectsReturned
from _testcapi import exception_print

# Create your views here.
@csrf_exempt
def signin(request):
  context = { 
          'username': request.POST['usuario'] , 
          'password': request.POST['pass']
  }
  if request.POST['usuario'] == 'admin':
    return render(request,'adm/perfil_adm.html',context)
  return render(request,'jugador/perfil.html',context)

def perfil_user(request):
  return render(request,'jugador/perfil.html')



###############################################################################################
######################################USUARIO##################################################
###############################################################################################

#Modificar las listas Genero y Plataforma
def mis_gustos(request,id_gustos):
  try:    
    MGustos=get_object_or_404(Jugador,usuario=id_gustos)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':
    ILike_form = MisGustosForm(request.POST, instance=MGustos)
    if ILike_form.is_valid():
      ILike_form.save()
      #return redirect('mis_gustos_2',id=id_gustos)
      return redirect('prueba')
  else:
    ILike_form = MisGustosForm(instance=MGustos)
    return render(request,'jugador/gustos/mis_gustos.html',{'fgustos':ILike_form})

def mis_gustos_2(request, id ):
  List_juegos=Juego.objects.all()
  #########Pizza.objects.all().prefetch_related('toppings')###############################################################
  #########b = Book.objects.select_related('author__hometown').get(id=4)
  ########from django.db.models import Q
  ########Model.objects.filter(Q(x=1) | Q(y=2))
  ########Model.objects.filter(Q(x=1) & Q(y=2))


  ############SEARCH
  ############Entry.objects.filter(headline__in='abc')
  List_Agregar=JuegosFavoritos.objects.filter(jugador=id)
  return render(request,'jugador/gustos/mis_gustos_2.html',{'fVJuegos':List_juegos,'fAgregar':List_Agregar})

def eliminar_juego(request,id,pk):
  try:
    usuario=get_object_or_404(JuegosFavoritos,id=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method=="POST":
    usuario.delete()
    return redirect('mis_gustos_2',id=pk)
  else:
    return render(request,'jugador/gustos/eliminar.html')

def agregar_juego(request,id,pk):
  try:
    vjuego=get_object_or_404(Juego,id_juego=id)
    vjugador=get_object_or_404(Jugador,usuario=pk)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')
  if request.method=="POST":
    vjugador.juegos = vjuego
    vjugador.save()
    return redirect('mis_gustos_2',id=pk)
  else:
    return render(request,'jugador/gustos/agregar.html')

def mis_opiniones(request,id):
    jugador=Jugador.objects.filter(usuario=id).first()
    print(jugador.nickname)
    miOpinion=Opinion.objects.filter(jugador=jugador.nickname)
    paginator=Paginator(miOpinion,5)
    page=request.GET.get('page')
    try:
      posts=paginator.page(page)
    except PageNotAnInteger:
      posts=paginator.page(1)
    except EmptyPage:
      posts=paginator.page(paginator.num_pages)
    return render(request,'jugador/opiniones.html',{'fOpinion':posts,'page':page})
    # return render(request,'jugador/opiniones.html',{'fOpinion':miOpinion,'page':page})

def edit_perfil(request,id):
  try:    
    usuario=get_object_or_404(Usuario,id=id)
    userio=get_object_or_404(User,id=id)
    jugador=get_object_or_404(Jugador,usuario=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':
    user_form = UserForm(request.POST, instance=userio)
    usuario_form = UsuarioForm(request.POST, instance=usuario)
    jugador_form = JugadorForm(request.POST, instance=jugador)
    if all([usuario_form.is_valid(),jugador_form.is_valid(),user_form.is_valid()]):
      usuario = usuario_form.save()
      jugador = jugador_form.save(commit = False)
      jugador.id_jugador = usuario
      jugador_form.save()
      user_form.save()
      return redirect('perfil_user')
      #return HttpResponseRedirect(reverse('registro-exitoso'),mensaje = 'Felicidades te registraste')
  else:
    usuario_form = UsuarioForm(instance=usuario)
    user_form = UserForm(instance=userio)
    jugador_form = JugadorForm(instance=jugador)
  return render(request,'jugador/editar_jugador.html',{'fusuario':usuario_form, 'fuser':user_form, 'fjugador':jugador_form})


def regresar_user(request):
  return render(request,'jugador/perfil.html')


def VVJuego(request,id_juego,pk):
  VJuego=Juego.objects.get(id_juego=id_juego)
  imagen =Imagen.objects.get(id_imagen=id_juego)
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
    opinion_form=OpinionForm()
    VJuego=Juego.objects.get(id_juego=id_juego)
    imagen =Imagen.objects.get(id_imagen=id_juego)    
    return render(request,'juegos/juego.html',{'fopinion':opinion_form,'VJuego':VJuego,'fimagen':imagen})

  
def consolas(request):
  imagen =Imagen.objects.all()
  juego=Juego.objects.all()
  return render(request,'juegos/consolas.html',{'fImagen':imagen,'fJuego':juego})

def generos(request):
  imagen =Imagen.objects.all()
  juego=Juego.objects.all()
  return render(request,'juegos/generos.html',{'fImagen':imagen,'fJuego':juego})

def MiLista(request,id):
  MLista=JuegosFavoritos.objects.filter(jugador=id)
  myFilter=JuegoFilter(request.GET,queryset=MLista)
  MLista=myFilter.qs

  paginator=Paginator(MLista,10)
  page=request.GET.get('page')
  try:
    posts=paginator.page(page)
  except PageNotAnInteger:
    posts=paginator.page(1)
  except EmptyPage:
    posts=paginator.page(paginator.num_pages)
  return render(request,'jugador/milista.html',{'fMLista':posts,'page':page})

def CountGen(generos):
  genes=['Acción','Arcade','Aventura','Bélico','Carreras','Deporte','Disparo',
  'Educacional','Estrategia','Juegos de mesa','Música','Peleas','Plataforma',
  'Rol (RPG)','Rompecabezas','Simulación','Survival horror','Trivia']
  generos.sort()
  genes.sort()
  listgeneros=[]
  cero=0
  uno=1
  for i in range(18): 
    if genes[i] not in generos:
      listgeneros.append(cero)
    else:
      listgeneros.append(uno)
  #print("Esta son los generos",listgeneros)
  return listgeneros

def CountPlat(plataformas):
  platas=['Android','Arcade','Dreamcast','Gameboy',
  'Gameboy Advance','Gameboy Color','J2ME','Linux',
  'NES','Neo Geo','Nintendo 3DS','Nintendo 64','Nintendo DS',
  'Nintendo GameCube','Nintendo Switch','PS Vita','PSP',
  'PlayStation 1','PlayStation 2','PlayStation 3','PlayStation 4',
  'SNES','Wii','Wii U','Windows',
  'Xbox','Xbox 360','Xbox One','iOS']
  platas.sort()
  plataformas.sort()
  listplataformas=[]
  cero=0
  uno=1
  for i in range(29): 
    if platas[i] not in plataformas:
      listplataformas.append(cero)
    else:
      listplataformas.append(uno)
  return listplataformas

def Comparate(list1,list0):
  list2=list(list0)
  #use CountPlat or CountGen return list2
  result = 1 - spatial.distance.cosine(list1, list2)
  if result >= 0.5:
    return 1
  return 0

def agregar_vector(request):
  for video in Juego.objects.all():
    new=[]
    newps=[]
    genres=""
    platforms=""
    print(video.titulo)
    for gen in video.generos.all():
      new.append(gen.nombre)
    new=list(dict.fromkeys(new))#Delete duplicates
    new.sort()#Sort list
    new=CountGen(new)
    #genres=(",".join(new))
    genres=(','.join(str(x) for x in new))

    for pat in video.plataformas.all():
      newps.append(pat.nombre)
    newps=list(dict.fromkeys(newps))#Delete duplicates
    newps.sort()#Sort list
    newps=CountPlat(newps)
    platforms=(','.join(str(x) for x in newps))

    listbinario=ListGeneros()
    listbinario.juego=video
    listbinario.listgenero=genres
    listbinario.listplataforma=platforms
    listbinario.save()

  return render(request,'jugador/RecMiPalabra.html')


def RecMisPalabras(request,id):
  try:
    usuario=Usuario.objects.get(id=id)
    carCDE=get_object_or_404(Cde,cde=usuario)
    jugador=get_object_or_404(Jugador,cde=usuario)
    generos=GenerosFavoritos.objects.all().filter(jugador=usuario)
    plataforma=PlataformasFavoritas.objects.all().filter(jugador=usuario)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')
  
  if Recomendacion(obj):
    return render(request,'jugador/RecMiPalabra.html',{'RMPform':Recomendacion})
  else:
    print (generos.length())
    print (plataforma.length())
    #litgenes=CountGen(generos)
    #listplatas=CountPlat(plataformas)
    return render(request,'jugador/RecMiPalabra.html',{'RMPform':Recomendacion})


def Busqueda(request):
  search=""
  if request.method == 'GET':
    search=request.GET.get('search')
    VJuego=Juego.objects.all().filter(titulo__icontains=search)
    return render(request,'juegos/busqueda.html',{'fVJuego':VJuego})

def info_consolas(request):
  return render(request,'juegos/InfoConsolas.html')

def info_generos(request):
  return render(request,'juegos/InfoGeneros.html')


######################################################################
######################################################################
                        #CARACTERISTICAS#
######################################################################
######################################################################
def InicioCDE(request,id):
  usuario=Usuario.objects.get(id=id)
  if request.method == 'POST':            
    cde_form = CdeForm(request.POST)
    if cde_form.is_valid():
      caracteristicas = cde_form.save(commit = False)
      caracteristicas.cde = usuario
      caracteristicas.save()
      return redirect('iusuario')
  else:
    cde_form = CdeForm()
    return render(request,'jugador/CDE.html',{'fcde':cde_form})


def caracteristicasDE(request,id):
  try:
    usuario=Usuario.objects.get(id=id)
    carDE=get_object_or_404(Cde,cde=usuario)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':            
    cde_form = CdeForm(request.POST,instance=carDE)
    if cde_form.is_valid():
      caracteristicas = cde_form.save(commit = False)
      caracteristicas.cde = usuario
      caracteristicas.save()      
      return redirect('caracteristicasDE',id=id)    
  else:
    cde_form = CdeForm(instance=carDE)
    return render(request,'jugador/CDE.html',{'fcde':cde_form})


def ViewcaracteristicasPU(request):
  vcpu=Cpu.objects.all()
  paginator=Paginator(vcpu,5)
  page=request.GET.get('page')
  try:
    posts=paginator.page(page)
  except PageNotAnInteger:
    posts=paginator.page(1)
  except EmptyPage:
    posts=paginator.page(paginator.num_pages)
  return render(request,'adm/CaractPU.html',{'fvcpu':vcpu,'page':page})

def ViewcaracteristicasDE(request):
  vcde=Cde.objects.all()
  paginator=Paginator(vcde,5)
  page=request.GET.get('page')
  try:
    posts=paginator.page(page)
  except PageNotAnInteger:
    posts=paginator.page(1)
  except EmptyPage:
    posts=paginator.page(paginator.num_pages)
  return render(request,'adm/CaractDE.html',{'fvcde':vcde,'page':page})

def prueba(request,username):
  jugador = get_object_or_404(Jugador,nickname=username)
  print(jugador)
  return render(request,'prueba.html')

def juegos101(request):
  juegos = Juego.objects.all()
  slugs = [juego.slug() for juego in juegos]
  for slug in slugs:
      print(slug)
  return render(request,'prueba.html')

def juegotal(request,juego_slug):
  print("SOlicitado:"+juego_slug)
  juego = get_object_or_404(Juego,slug=juego_slug)
  print(juego)
  return render(request,'prueba.html')

lg = [] #Lista de generos  
  aleatorios = []
  generos = []
  for favorito in GenerosFavoritos.objects.all():
    generos.append(favorito.genero)
    lg.append((Genero.objects.all().filter(nombre=favorito.genero))[0].id_genero)
  for id_genero in lg:
    print("Juegos para id_genero",id_genero)
    rs = GenerosAsociados.objects.all().filter(genero=id_genero)
    print("Que son ",len(rs))
    max_lim = 0
    if len(rs) < 20:
       max_lim = len(rs)
    else:
       max_lim = 20
    print("El maximo ",max_lim)
    randomList = random.sample(range(0, len(rs)), max_lim)
    print("La lista aleatoria:",randomList)
  
  # listjuegos=[]
  # for i in randomList:
    
  # for number in randomList:
  #    aleatorios.append()
  # for aleatorio in aleatorios:
  #   print(aleatorio)
  
  # print("Cadenas")

"""
