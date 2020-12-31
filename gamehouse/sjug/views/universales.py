from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from gamehouse.sadm.models import Administrador,Tf_Idf
from django.shortcuts import redirect,render
from gamehouse.sjug.forms import UserForm,JugadorForm,UsuarioForm,OpinionForm
from gamehouse.sjug.models import Jugador, Usuario,Imagen,Juego
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
    """ Requisito haber limpiado las descripciones """
    #faltantes = Juego.objects.filter(tf_idf=None)
    faltantes = Juego.objects.filter(tf_idf=None)[:10] #Cien primeros juegos :100
    descripciones = faltantes.values_list('descripcion_limpia',flat=True)
    from gamehouse.algorithms.tf_idf import ex_tf_idf
    vectors = ex_tf_idf(descripciones)
    from pickle import dump
    from django.conf import settings
    i = 0
    for juego in faltantes:
        archivo = settings.ANALITYCS_DIR + str(juego.id_juego) +'.pkl' 
        output = open(archivo,'wb') #web -- write bytes
        dump(vectors[i],output, -1) #mete bytes en archivo nuestro diccionario de lemmas
        output.close()
        i = i + 1
        tf_idf = Tf_Idf(juego = juego, vector = archivo)
        tf_idf.save()    
    return redirect('/algoritmos/')

def tf_idf_sk(request):
    """ Requisito haber limpiado las descripciones """
    #faltantes = Juego.objects.filter(tf_idf=None)
    faltantes = Juego.objects.filter(tf_idf=None)[:10] #Cien primeros juegos :100
    descripciones = faltantes.values_list('descripcion_limpia',flat=True)
    from gamehouse.algorithms.tf_idf import im_tf_idf
    vectors = im_tf_idf(descripciones)
    from pickle import dump
    from django.conf import settings
    i = 0
    for juego in faltantes:
        archivo = settings.ANALITYCS_DIR + str(juego.id_juego) +'.pkl' 
        output = open(archivo,'wb') #web -- write bytes
        dump(vectors[i],output, -1) #mete bytes en archivo nuestro diccionario de lemmas
        output.close()
        i = i + 1
        tf_idf = Tf_Idf(juego = juego, vector = archivo)
        tf_idf.save()
    return redirect('/algoritmos/')

def limpiar_descripciones(request):
    """ Ejecutar antes de calcular vectores tf-idf """
    sucios = Juego.objects.filter(descripcion_limpia = None)[:25]
    print("Hay "+str(len(sucios))+" juegos sucios")
    for sucio in sucios:
        sucio.descripcion_limpia = None
        sucio.save()
    return redirect('/algoritmos')

def ee_tf_idf(juegos):
    """ Requisito haber limpiado las descripciones """
    from gamehouse.algorithms.tf_idf import get_vocabulary,implicit_tf_idf
    descripciones = juegos.values_list('descripcion',flat=True)
    vocabulario = get_vocabulary(descripciones)
    vectores = explicit_tf_idf(descripciones,vocabulario)
    for i in range(len(juegos)):
        juego = juegos[i]
        descripcion = descripciones[i]
        vector = vectores[i]
        print("Juego "+juego.titulo+" con id "+str(juego.id_juego)+" tiene descripcion limpia:")
        print(descripcion)
        print("Su vector:")
        print(vector)
    print(sorted(vocabulario))

