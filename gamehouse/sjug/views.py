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

def perfil(request):
    # if request.user.is_authenticated:
    #     return redirect('perfil_user')    
    if request.method == 'POST':        
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin':
          return render(request,'adm/perfil_adm.html')
        print(password)
        user = authenticate(request,username =username, password = password)
        if user is not None:
            login(request,user)
            #return render(request,'jugador/InicioUsuario.html')
            return redirect('iusuario')
        else:            
            return render(request,'inicio_sesion.html')
    else:        
        return render(request,'inicio_sesion.html')

def signout(request):
    logout(request)
    return redirect('/')

def perfil_user(request):
  return render(request,'jugador/perfil.html')

def registro(request):
  if request.method == 'POST':            
    user_form = UserForm(request.POST)  
    usuario_form = UsuarioForm(request.POST)
    jugador_form = JugadorForm(request.POST)
    if all([usuario_form.is_valid(),jugador_form.is_valid(),user_form.is_valid()]):          
      print('entre')
      usuario = usuario_form.save()
      jugador = jugador_form.save(commit = False)
      jugador.id_jugador = usuario
      jugador.save()
      user_form.save()
      username = user_form.cleaned_data['username']
      print(usuario.id)

      password = user_form.cleaned_data['password1']
      user = authenticate(username = username,password = password)
      login(request, user)
      print(user)
      return redirect('InicioCDE',id=usuario.id)
      #return render(request,'inicio_sesion.html')
  else:
    user_form=UserForm()
    usuario_form = UsuarioForm()
    jugador_form = JugadorForm()
  return render(request,'registro.html',{'fusuario':usuario_form, 'fuser':user_form,'fjugador':jugador_form})

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

def eliminar(request,id):
  try:
    usuario=get_object_or_404(Usuario,id=id)
    userio=get_object_or_404(User,id=id)
    jugador=get_object_or_404(Jugador,usuario=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method=="POST":
    jugador.delete()
    userio.delete()
    usuario.delete()
    return redirect('index')
  else:
    return render(request,'jugador/eliminar.html')

def regresar_user(request):
  return render(request,'jugador/perfil.html')

def iusuario(request):  
  # Generate 'n' unique random numbers within a range
  imagen =Imagen.objects.all()
  juego=Juego.objects.all()
  randomList = random.sample(range(0, len(imagen)), 12)
  LImagen=[]
  LJuego=[]
  for r in randomList:
    LImagen.append(imagen[r])
    LJuego.append(juego[r])
  VJuego=zip(LImagen,LJuego)
  #return render(request,'jugador/InicioUsuario.html')
  return render(request,'jugador/InicioUsuario.html',{'fvjuego':VJuego})
  # return render(request,'jugador/InicioUsuario.html',{'fImagen':LImagen,'fJuego':LJuego})


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


def salir(request):
  return render(request,'homepage.html')

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
  for i in range(18):
    if generos[i]==genes[i]:
      listgeneros[i]=1
    else:
      listgeneros[i]=0

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
  for i in range(29):
    if plataformas[i]==platas[i]:
      listplataformas[i]=1
    else:
      listplataformas[i]=0
  return listplataformas

def Comparate(list1,list0):
  lista=list(list0)
  #use CountPlat or CountGen return list2
  result = 1 - spatial.distance.cosine(list1, list2)
  if result >= 0.5:
    return 1
  return 0

def agregar_vector(request):
  platas=PlataformasAsociadas.objects.all()
  genes=GenerosAsociados.objects.all()
  listemp=[]
  for video in Juego.objects.all():
    new=[]
    newbi=[]
    gnr=GenerosAsociados.objects.all().filter(juego=video.id_juego)
    for gen in gnr:
      new.append(gen.genero)
    for i in range(len(new)):
      newbi.append(new[i].nombre)
    listemp.append(",".join(newbi))
  print(len(listemp))

  return render(request,'jugador/RecMiPalabra.html',{'RMPform':Recomendacion})


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
###############################################################################################
################################ADMINISTRADOR##################################################
###############################################################################################
def perfil_adm(request):
  platas=PlataformasAsociadas.objects.all()
  genes=GenerosAsociados.objects.all()

  # for gen in genes:
  #   print(gen.genero)

  return render(request,'adm/perfil_adm.html')

# def gestion_usuarios(request):
#   #TodoU=Usuario.objects.all()
#   return render(request,'adm/gestion_usuario.html')

def gestion_videojuegos(request):
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

# def changeVector(request):
#   VJuegos=Juego.objects.all()
#   for game in VJuegos:
#     print(game.genero)
#   return 


def registro_videojuegos(request):
  if request.method == 'POST':         
    juego_form = JuegoForm(request.POST)
    imagen_form = ImagenForm(request.POST)
    # compania_form = CompaniaForm(request.POST)
    if all([juego_form.is_valid(),imagen_form.is_valid()]):
      #photo = Juego()    # set any other fields, but don't commit to DB (ie. don't save())
      
      # imagen_form.imageurl=request.POST.get('imageurl')
      # img_url=request.POST.get('imageurl')
      # name = urlparse(img_url).path.split('/')[-1]
      # content =urllib.request.urlretrieve(img_url)
      # imagefile.save('imagen.jpg', File(open(content[0])), save=True)
      
      ######STRING DATA
      # juego_form.generos=request.POST.get('nombreG')
      # juego_form.plataformas=request.POST.get('nombreP')

      # See also: http://docs.djangoproject.com/en/dev/ref/files/file/
      imagen_form.save()
      juego_form.save()
      return redirect('g_videojuegos')
  else:
    juego_form=JuegoForm()
    imagen_form = ImagenForm()
  return render(request,'adm/registro_videojuego.html',{'VJuegos':juego_form,'fImagen':imagen_form})

def editar_J(request,id):
  try:    
    vjuego=get_object_or_404(Juego,id_juego=id)
    vimagen=get_object_or_404(Imagen,id_imagen=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':
    vjuego_form = JuegoForm(request.POST, instance=vjuego)
    imagen_form = ImagenForm(request.POST, instance=vimagen)
    if all([vjuego_form.is_valid(),imagen_form.is_valid()]):      
      ###STRING DATA
      # vjuego.plataformas=request.POST.get('nombreP')
      # vjuego.generos=request.POST.get('nombreG')
    
      imagen_form.save()
      vjuego_form.save()
      return redirect('g_videojuegos')
  else:
    imagen_form = ImagenForm(instance=vimagen)
    vjuego_form = JuegoForm(instance=vjuego)
    return render(request,'adm/editar_videojuego.html',{'VJuegos':vjuego_form,'fImagen':imagen_form})

def eliminar_J(request,id):
  try:
    vjuego=get_object_or_404(Juego,id_juego = id)
    vimagen=get_object_or_404(Imagen,id_imagen=id)
    # vgenero=get_object_or_404(  Genero,id = id)
    # vplataforma=get_object_or_404(Plataforma, id=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method=="POST":
    # vgenero.delete()
    # vplataforma.delete()
    vimagen.delete()
    vjuego.delete()
    return redirect('g_videojuegos')
  else:
    return render(request,'adm/eliminarJ.html')

def aceptado(request):
  return render(request,'adm/juego_aceptado.html')

def gestion_usuarios(request):
    dataset = Usuario.objects.all()
    paginator=Paginator(dataset,2)
    page=request.GET.get('page')
    try:
      posts=paginator.page(page)
    except PageNotAnInteger:
      posts=paginator.page(1)
    except EmptyPage:
      posts=paginator.page(paginator.num_pages)
    return render(request,'adm/gestion_usuario.html',{'dataset':posts,'page':page})

def gestion_GP(request):
    print('hola')
    plataforma=Plataforma.objects.all()
    genero=Genero.objects.all()
    return render(request,'adm/gestion_GP.html',{'fgenero':genero,'fplataforma':plataforma})

def registro_usuarios(request):
  if request.method == 'POST':
    user_form = UserForm(request.POST) 
    usuario_form = UsuarioForm(request.POST)
    jugador_form = JugadorForm(request.POST)

    if all([usuario_form.is_valid(),jugador_form.is_valid(),user_form.is_valid()]):
      usuario = usuario_form.save()
      jugador = jugador_form.save(commit = False)
      jugador.id_jugador = usuario
      jugador.save()
      user_form.save()
      username = user_form.cleaned_data['username']
      password = user_form.cleaned_data['password1']
      user = authenticate(username = username,password = password)
      login(request, user)
      return redirect('g_usuarios')
      #return HttpResponseRedirect(reverse('registro-exitoso'),mensaje = 'Felicidades te registraste')
  else:
    user_form=UserForm()
    usuario_form = UsuarioForm()
    jugador_form = JugadorForm()
  #  context={'fusuario':usuario_form, 'fjugador':jugador_form}
  return render(request,'adm/registro.html',{'fusuario':usuario_form, 'fuser':user_form, 'fjugador':jugador_form})

def editar_usuarios(request,id):
  try:    
    usuario=get_object_or_404(Usuario,id=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':
    usuario_form = UsuarioForm(request.POST, instance=usuario)
    if usuario_form.is_valid():
      usuario = usuario_form.save()
      return redirect('g_usuarios')
  else:
    usuario_form = UsuarioForm(instance=usuario)
  return render(request,'adm/Actualizar.html',{'fusuario':usuario_form})

def eliminar_usuarios(request,id):
  try:
    usuario=get_object_or_404(Usuario,id=id)
    userio=get_object_or_404(User,id=id)
    jugador=get_object_or_404(Jugador,usuario=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method=="POST":
    jugador.delete()
    userio.delete()
    usuario.delete()
    return redirect('g_usuarios')
  else:
    return render(request,'adm/eliminar.html')

def registro_GP(request):
  if request.method == 'POST':
    genero_form = GeneroForm(request.POST)
    plataforma_form = PlataformaForm(request.POST)
    if all([genero_form.is_valid(),plataforma_form.is_valid()]):
      genero_form.save()
      plataforma_form.save()
      return redirect('g_GP')
  else:
    genero_form = GeneroForm()
    plataforma_form = PlataformaForm()
  return render(request,'adm/registroGP.html',{'fgenero':genero_form, 'fplataforma':plataforma_form})

def editar_G(request,id):
  try:    
    genero=get_object_or_404(Genero,id_genero=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':
    genero_form = GeneroForm(request.POST, instance=genero)
    if genero_form.is_valid():
      genero_form.save()
      return redirect('g_GP')
  else:
    genero_form = GeneroForm(instance=genero)
  return render(request,'adm/ActualizarG.html',{'fgenero':genero_form})

def eliminar_G(request,id):
  try:
    usuario=get_object_or_404(Genero,id_genero=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method=="POST":
    usuario.delete()
    return redirect('g_GP')
  else:
    return render(request,'adm/eliminarG.html')

def editar_P(request,id):
  try:    
    usuario=get_object_or_404(Plataforma,id_plataforma=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method == 'POST':
    usuario_form = PlataformaForm(request.POST, instance=usuario)
    if usuario_form.is_valid():
      usuario_form.save()
      return redirect('g_GP')
  else:
    usuario_form = PlataformaForm(instance=usuario)
  return render(request,'adm/ActualizarP.html',{'fplataforma':usuario_form})

def eliminar_P(request,id):
  try:
    usuario=get_object_or_404(Plataforma,id_plataforma=id)
  except Exception:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  if request.method=="POST":
    usuario.delete()
    return redirect('g_GP')
  else:
    return render(request,'adm/eliminarP.html')

def editar_perfil(request):
  return render(request,'adm/editar_jugador.html')

def regresar_adm(request):
  platas=PlataformasAsociadas.objects.all()
  genes=GenerosAsociados.objects.all()

  # print(genes.genero)

  for gen in genes:
    print(gen.genero)
  return render(request,'adm/perfil_adm.html')

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

def prueba(request):
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
    
  # """
  # for number in randomList:
  #    aleatorios.append()
  # for aleatorio in aleatorios:
  #   print(aleatorio)
  # """  
  # print("Cadenas")
  return render(request,'prueba.html',{'generos':generos})

