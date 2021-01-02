from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from gamehouse.sadm.models import Administrador,Tf_Idf
from django.shortcuts import redirect,render
from gamehouse.sjug.forms import UserForm,JugadorForm,UsuarioForm,OpinionForm
from gamehouse.sjug.models import Jugador, Usuario,Imagen,Juego,CDE,CPU
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


### nltk FreqDist
#sudo pip install -U nltk
import nltk
def contar_caracteristicas(request):
    jugadores = Jugador.objects.all()
    for gamer in jugadores:
        generos_favoritos = gamer.generos.all()
        plataformas_favoritas = gamer.plataformas.all()
        carcde= CDE.objects.filter(jugador=gamer)
        carcpu= CPU.objects.filter(jugador=gamer)
        #como van a cambiar combiene hacerlos cada vez y no haccer la tabla
        caracteristicaDE=list(carcde.cde0+carcde.cde1+carcde.cde2+carcde.cde3+carcde.cde4+carcde.cde5+carcde.cde6+carcde.cde7+carcde.cde8+carcde.cde9)
        caracteristicaPU=list(carcpu.cpu0+carcpu.cpu1+carcpu.cpu2+carcpu.cpu3+carcpu.cpu4+carcpu.cpu5+carcpu.cpu6+carcpu.cpu7+carcpu.cpu8+carcpu.cpu9)
        
        for genero in generos_favoritos:
            print("Generos",genero)
            juegos_genero = Juego.objects.filter(generos = genero)
            if len(juegos_genero) > 20:#Elije los primeros 20
                juegos_genero = juegos_genero[:20]
            for juego in juegos_genero:                
                descripcion_limpia = juego.descripcion_limpia
                freGenCDE = FreqDist(len(caracteristicaDE) for caracteristicaDE in descripcion_limpia)
                freGenCPU = FreqDist(len(caracteristicaPU) for caracteristicaPU in descripcion_limpia)

        for plataforma in plataformas_favoritas:
            print("Plataformas",plataforma)
            juegos_genero = Juego.objects.filter(plataformas = plataforma)
            if len(juegos_genero) > 20:#Elije los primeros 20
                juegos_genero = juegos_genero[:20]
            for juego in juegos_genero:                
                descripcion_limpia = juego.descripcion_limpia
                frePlaCDE = FreqDist(len(caracteristicaDE) for caracteristicaDE in descripcion_limpia)
                frePlaCPU = FreqDist(len(caracteristicaPU) for caracteristicaPU in descripcion_limpia)
    return redirect('/algoritmos/')
                #----fdist1 = FreqDist(descripcion_limpia)
                #----listtemp=[]
                #descripcion_limpia = descripcion_limpia.split()
                #----for cde in caracteristicaDE:
                    #----listtemp.append(fdist1[cde])
    
    # a1 -> [1,2,20,10,15,1,..,0] -> "1,2,20,10,15"
    

