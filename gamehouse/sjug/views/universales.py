from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from gamehouse.sadm.models import Administrador,Tf_Idf
from django.shortcuts import redirect,render
from gamehouse.sjug.forms import UserForm,JugadorForm,UsuarioForm,OpinionForm
from gamehouse.sjug.models import Jugador, Usuario,Imagen,Juego,Opinion,CPU,CDE,Vector_Caracteristicas
from django.http import Http404
from pickle import NONE

"""
PENDIENTES:
1.- Hacer vista para punto /juegos
2.- Corregir UserForm, UsuarioForm,JugadorForm


"""

def login(request):
    # if request.user.is_authenticated:
    #     return redirect('juegos')    
    if request.method == 'POST':     
        username = request.POST['username']
        password = request.POST['password']
        print("El admin tiene:",username)
        try:
            admin = Administrador.objects.get(nombre = username)
            print("El admin tiene:",admin.nombre)            
            if admin:
                jugador = Jugador.objects.get(usuario = admin.usuario)
                print("El admin tiene:",jugador.nickname)
                usuario = authenticate(request, username = jugador.nickname, password = password)
                # usuario = authenticate(request, username = username, password = password)
                if usuario:
                    auth_login(request,usuario)
                    return redirect('/sadm/'+admin.nombre)
                else:
                    return redirect("/login/")
        except Administrador.DoesNotExist:
            try:
                jugador = Jugador.objects.get(nickname = username)
                usuario = authenticate(request, username = username, password = password)
                if usuario:
                    auth_login(request,usuario)
                    return redirect('/sjug/'+jugador.nickname+'/dashboard/')
                else:
                    return redirect("/login/")
            except Jugador.DoesNotExist:
                raise Http404("El usuario con el que intentas iniciar sesión no existe!")
    else:        
        return render(request,'inicio_sesion.html')

@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect('index')

## Falta guardar datos de genero consolas    
## Falta la página de 10 palabras
def registro(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        usuario_form = UsuarioForm(request.POST)
        jugador_form = JugadorForm(request.POST)
        if all([usuario_form.is_valid(),jugador_form.is_valid(),user_form.is_valid()]):          
            usuario = usuario_form.save()
            jugador = jugador_form.save(commit = False)
            jugador.id_jugador = usuario.id_usuario
            jugador.save()
            user_form.save()
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            usuario = authenticate(request, username =username, password = password)
            auth_login(request,usuario)        
            return redirect('registro_palabras',jugador=username)
        else: # Renderizar de nuevo con errores
            return render(request,'registro.html',{'fusuario':usuario_form, 'fuser':user_form,'fjugador':jugador_form}) 
    else:
        user_form = UserForm()
        usuario_form = UsuarioForm()
        jugador_form = JugadorForm()
        return render(request,'registro.html',{'fusuario':usuario_form, 'fuser':user_form,'fjugador':jugador_form})
    
    
""" Vistas de error """
def bad_request(request):
    context = {}
    return render(request, '400.html', context, status=400)

def solicitud_denegada(request):
    context = {}
    return render(request, 'error/403.html', context, status=403)

def no_encontrado(request):
    context = {}
    return render(request, 'error/404.html', context, status=404)

def server_error(request):
    context = {}
    return render(request, '500.html', context, status=500)


""" Prueba """
def algoritmos(request):
    return render(request, 'algoritmos.html')

def tf_idf_propio(request):
    """ ESTA FUNCION CREA LOS VECTORES USANDO METODO PROPIO
        DE TODOS LOS JUEGOS, TENGAN O NO YA DESCRIPCION
        TOMARA TIEMPO EN TERMINAR
     Requisito haber limpiado las descripciones """
    juegos = Juego.objects.all()
    descripciones = juegos.values_list('descripcion_limpia',flat=True)
    from gamehouse.algorithms.tf_idf import ex_tf_idf
    vectors = ex_tf_idf(descripciones)
    from pickle import dump
    from django.conf import settings
    i = 0
    for juego in juegos:
        archivo = settings.ANALITYCS_DIR + str(juego.id_juego) +'.pkl' 
        output = open(archivo,'wb') #web -- write bytes
        dump(vectors[i],output, -1) #mete bytes en archivo nuestro diccionario de lemmas
        output.close()
        i = i + 1
        tf_idf = Tf_Idf(juego = juego, vector = archivo)
        tf_idf.save()    
    return redirect('/algoritmos/')

def tf_idf_sk(request):
    """ ESTA FUNCION CREA LOS VECTORES USANDO SKLEARN
        DE TODOS LOS JUEGOS, TENGAN O NO YA DESCRIPCION
        TOMA BASTANTE TIEMPO EN EJECUTARSE
     Requisito haber limpiado las descripciones """
    juegos = Juego.objects.all() 
    descripciones = juegos.values_list('descripcion_limpia',flat=True)
    from gamehouse.algorithms.tf_idf import im_tf_idf
    vectors = im_tf_idf(descripciones)
    from pickle import dump
    from django.conf import settings
    i = 0
    for juego in juegos:
        archivo = settings.ANALITYCS_DIR + str(juego.id_juego) +'.pkl' 
        output = open(archivo,'wb') #web -- write bytes
        dump(vectors[i],output, -1) #mete bytes en archivo nuestro diccionario de lemmas
        output.close()
        i = i + 1
        tf_idf = Tf_Idf(juego = juego, vector = archivo)
        tf_idf.save()
    return redirect('/algoritmos/')


def obtener_cpus(request):
    from gamehouse.algorithms.caracteristicas import calcular_cpus
    # Obtener todos los jugadores que han hecho una opiniones
    jugadores = Jugador.objects.exclude(opiniones=None)
    for jugador in jugadores:
        #Obtener las opiniones del jugador distintas y con calificacion mayor a seis, ordenar de acuerdo al total
        #juegos = jugador.opiniones.distinct().values_list('juego',flat=True)
        juegos = jugador.opiniones.filter(gusto__gte=6).order_by('puntaje_total').values_list('juego',flat=True).distinct()
        juegos = juegos.reverse() ## De mayor a menor
        seccion = len(juegos) // 5 
        if seccion: #Si hay al menos cinco
            #juegos = jugador.opiniones.all().values_list('juego',flat=True).distinct()
            cpus = calcular_cpus(juegos) 
            tabla_cpu = CPU()
            tabla_cpu.jugador = jugador
            tabla_cpu.cpu0=cpus[0]
            tabla_cpu.cpu1=cpus[1]
            tabla_cpu.cpu2=cpus[2]
            tabla_cpu.cpu3=cpus[3]
            tabla_cpu.cpu4=cpus[4]
            tabla_cpu.cpu5=cpus[5]
            tabla_cpu.cpu6=cpus[6]
            tabla_cpu.cpu7=cpus[7]
            tabla_cpu.cpu8=cpus[8]
            tabla_cpu.cpu9=cpus[9]
            tabla_cpu.save()
            print("El jugador "+jugador.nickname+" tiene las cpus:")
            print(cpus)
    return redirect('/algoritmos/')


def generar_tf_idf(request):
    from gamehouse.algorithms.tf_idf import recomendar_tf_idf
    from gamehouse.sadm.models import Tf_Idf
    jugadores = Jugador.objects.exclude(juegos_favoritos=None)
    for jugador in jugadores:
        favoritos = jugador.juegos_favoritos.all() #.values_list('uego',flat=True) #.distinct()
        print(jugador)
        print("Tiene los siguientes juegos favoritos:")
        generos = set()
        for favorito in favoritos:
            generos.update(favorito.juego.generos.all())
        generos = list(generos)
        for favorito in favoritos:
            pos = Tf_Idf.objects.get(juego = favorito.juego)
            recomendar_tf_idf(pos,generos)
    return redirect('/algoritmos/')

import nltk
from nltk.probability import FreqDist
def contar_caracteristicas(request):
  from gamehouse.algorithms.caracteristicas import calcular_caracteristicas
  jugadores = Jugador.objects.all()
  listJuegosCDE=[]
  listJuegosCPU=[]
  caracteristicaDE=[]
  caracteristicaPU=[]
  for gamer in jugadores:
    print("GAMER",gamer)
    generos_favoritos = gamer.generos.all()
    plataformas_favoritas = gamer.plataformas.all()
    print("GENES",generos_favoritos)
    print("PLATAS",plataformas_favoritas)
    carcde= CDE.objects.get(jugador=gamer)
    #carcpu= CPU.objects.get(jugador=gamer)
    carcpu= CPU.objects.get(jugador=4)
    #como van a cambiar combiene hacerlos cada vez y no haccer la tabla
    caracteristicaDE.extend([carcde.cde0,carcde.cde1,carcde.cde2,carcde.cde3,carcde.cde4,carcde.cde5,carcde.cde6,carcde.cde7,carcde.cde8,carcde.cde9])
    caracteristicaPU.extend([carcpu.cpu0,carcpu.cpu1,carcpu.cpu2,carcpu.cpu3,carcpu.cpu4,carcpu.cpu5,carcpu.cpu6,carcpu.cpu7,carcpu.cpu8,carcpu.cpu9])
    for genero in generos_favoritos:
      juegos_genero = Juego.objects.filter(generos = genero)      
      if len(juegos_genero) > 20:#Elije los primeros 20
        juegos_genero = juegos_genero[:20]
      for juego in juegos_genero:
        print("El jugador",gamer)
        # cpus=""
        # cdes=""
        # descripcion_limpia = juego.descripcion_limpia
        # listDescripcion = list(descripcion_limpia.split(" "))     
        # freGen = FreqDist(listDescripcion)
        # cdes=calcular_caracteristicas(caracteristicaDE,freGen)
        # cpus=calcular_caracteristicas(caracteristicaPU,freGen)
        # tabla_gen = Vector_Caracteristicas()
        # tabla_gen.jugador = gamer
        # tabla_gen.juego=juego
        # tabla_gen.cpus=cpus
        # tabla_gen.cdes=cdes
        # tabla_gen.save()                                  
    for plataforma in plataformas_favoritas:
      juegos_genero = Juego.objects.filter(plataformas = plataforma)
      if len(juegos_genero) > 20:#Elije los primeros 20
        juegos_genero = juegos_genero[:20]
      for juego in juegos_genero:
        pass
        # cpus=""
        # cdes=""
        # descripcion_limpia = juego.descripcion_limpia
        # listDescripcion = list(descripcion_limpia.split(" "))     
        # frePla = FreqDist(listDescripcion)
        # cdes=calcular_caracteristicas(caracteristicaDE,frePla)
        # cpus=calcular_caracteristicas(caracteristicaPU,frePla)
        # tabla_pla = Vector_Caracteristicas()
        # tabla_pla.jugador = gamer
        # tabla_pla.juego=juego
        # tabla_pla.cpus=cpus
        # tabla_pla.cdes=cdes
        # tabla_pla.save()            
  return redirect('/algoritmos/')

"""
    listdesc=[]
    listgames=[]
    listidf=[]
    list7=[]
    list8=[]
    list9=[]
    list10=[]

    ############    FILTER LIST
    usuario=Usuario.objects.get(id=id)
    jugador=Jugador.objects.get(usuario=usuario)
    setGames=Opinion.objects.all().filter(jugador=jugador.nickname,gusto__gte=6)

    ############    SEPARATE LIST
    for game in setGames:
      print("El juego es:",game)
      temp=[]
      suma=game.guion+game.artes+game.jugabilidad+game.tecnico
      print("La suma es:",suma)
      if game.gusto == 10:
        temp.append(game.juego)
        temp.append(suma)
        list10.append(temp)
      elif game.gusto == 9:
        temp.append(game.juego)
        temp.append(suma)
        list9.append(temp)
      elif game.gusto == 8:
        temp.append(game.juego)
        temp.append(suma)
        list8.append(temp)
      elif game.gusto == 7 or game.gusto == 6:
        temp.append(game.juego)
        temp.append(suma)
        list7.append(temp)

    ############    SORT LIST
    list10.sort(key=lambda x: x[1], reverse=True)
    list9.sort(key=lambda x: x[1], reverse=True)
    list8.sort(key=lambda x: x[1], reverse=True)
    list7.sort(key=lambda x: x[1], reverse=True)

    # for ele in list10:
    #   print("lista 10:",ele[0])

    ############    CHANGE LISTS IN LIST OF 10
    if len(list10)>0:
      if len(list10) >= 5:
        #listtemp=list(split(list10, 5)) #seccionar la lista
        listtemp = np.array_split(list10, 5)
        for evry in listtemp:
          listgames=random.sample(range(0, len(evry)), 1)
      else:#si no cumple con el ancho
        for elemento in list10:
          listgames.append(elemento)

    if len(list9)>0:
      limit=8-len(listgames)#Se resta 8 para saber los que faltan    
      if len(listgames)<5 and len(list9) >=3:#Agrega si en la lista no hay 5
        listtemp=np.array_split(list9,limit)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      elif len(list9) >=3:#Agrega 3
        listtemp=np.array_split(list9, 3)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      else:
        for elemento in list9:
          listgames.append(elemento)
    
    if len(list8)>0:
      limit=10-len(listgames)#Se resta 10 para saber los que faltan
      if len(listgames)<8 and len(list8) >=2:#Agrega si en la lista no hay 5
        listtemp=np.array_split(list8,limit)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      elif len(list8) >=2:
        listtemp=np.array_split(list8, 2)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      else:
        for elemento in list8:
          listgames.append(elemento)

    if len(list7)>0:
      limit=10-len(listgames)#Se resta 10 para saber los que faltan
      if len(listgames)<10 and len(list7) >=limit:
        listtemp=np.array_split(list7, limit)#seccionar la lista
        for evry in listtemp:#de cada seccion obtiene un elemento
          listgames=random.sample(range(0, len(evry)), 1)
      else:
        for elemento in list7:
          listgames.append(elemento)

    ############    CREATE LIST OF DESCRIPTION
    for ele in listgames:
      description=Juego.objects.filter(titulo=ele[0])
      for desc in description:
        listdesc.append(desc.descripcion)
    print("lista :",listdesc)
    
    for listtext in listdesc:
      listidf.append(idf(listtext))
    
    listidf.sort(reverse=True)
"""


def limpiar_descripciones(request):
    """ ESTA FUNCION LIMPIA LAS DESCRIPCIONES DE
        TODOS LOS JUEGOS
        TARDA BASTANTE 
        LO IDEAL ES HACER LA LIMPIEZA POR FUERA
        Ejecutar antes de calcular vectores tf-idf """
    sucios = Juego.objects.filter(descripcion_limpia = None)
    print("Hay "+str(len(sucios))+" juegos sucios")
    for sucio in sucios:
        sucio.descripcion_limpia = None
        sucio.save()
    return redirect('/algoritmos')
