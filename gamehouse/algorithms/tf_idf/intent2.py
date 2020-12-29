from gamehouse.sjug.models import Jugador

def imprime_usuarios():
    jugadores = Jugador.objects.all()
    print("Jugadores encontrados")
    for jugador in jugadores:
        print(jugador.nickname)
    