from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from gamehouse.sadm.models import Administrador
from django.shortcuts import redirect,render
from gamehouse.sjug.forms import UserForm,JugadorForm,UsuarioForm,OpinionForm
from gamehouse.sjug.models import Jugador, Usuario,Imagen,Juego
from django.http import Http404

"""
PENDIENTES:
1.- Hacer vista para punto /juegos
2.- Corregir UserForm, UsuarioForm,JugadorForm


"""

def login(request):
    if request.user.is_authenticated:
        return redirect('/juegos/')    
    if request.method == 'POST':     
        username = request.POST['username']
        password = request.POST['password']
        try:
            jugador = Jugador.objects.get(nickname = username)
            usuario = authenticate(request, username = username, password = password)
            if usuario:
                auth_login(request,usuario)
                return redirect('/sjug/'+jugador.nickname+'/dashboard/')
            else:
                return redirect("/login/")
        except Jugador.DoesNotExist:
            try:
                admin = Administrador.objects.get(nombre = username)
                # usuario = Usuario.objects.get(id_usuario = admin.usuario.id_usuario)
                # jugador = Jugador.objects.get(usuario_id = usuario.id_usuario)
                #usuario = authenticate(request, username = jugador.nickname, password = password)
                usuario = authenticate(request, username = username, password = password)
                if usuario:
                    auth_login(request,usuario)
                    return redirect('/sadm/'+admin.nombre)
                else:
                    return redirect("/login/")
            except Administrador.DoesNotExist:
                raise Http404("El usuario con el que intentas iniciar sesión no existe!")
    else:        
        return render(request,'inicio_sesion.html')

@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect('index')
    
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
            return redirect('/login')
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
