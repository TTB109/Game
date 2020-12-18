from django.db.models import *
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .juego import Juego, Genero, Plataforma
import datetime
from django.utils import timezone

""" Entidades del jugador """
class Usuario(models.Model):
  nombre = models.CharField(max_length=100)
  apellido = models.CharField(max_length=256)
  correo = models.EmailField()
  fec_nac = models.DateField(help_text = "Use el formato:DD-MM-AAAA")
  def __str__(self):
   return '%s, %s' % (self.nombre, self.correo)

class Jugador(models.Model):
  usuario = models.OneToOneField(Usuario, 
    on_delete = models.CASCADE, 
    primary_key = True,
    db_column = "id_jugador",
    verbose_name = "Identificador del jugador"
  )
  juegos = models.ManyToManyField(Juego,
    through = 'JuegosFavoritos',
    verbose_name = "Juegos favoritos del usuario"
  )
  generos = models.ManyToManyField(Genero,
    through = 'GenerosFavoritos',
    through_fields=('jugador','genero')
  )
  plataformas = models.ManyToManyField(Plataforma,
    through = 'PlataformasFavoritas',
    through_fields=('jugador','plataforma')
  )
  #null indica que pueden almacenarse datos NULL en la tabla
  #blank indica que en los formularios se permite que el campo este en blanco
  nickname = models.CharField(unique=True, null=False, max_length=20, verbose_name="Nickname del usuario")
  def __str__(self):
   return self.nickname

class Opinion(models.Model):
  jugador = models.ForeignKey(Jugador,
     on_delete = models.SET_NULL, #AL Borrar el creador se pone en nulo y no mueren comentarios
     to_field = 'nickname',
     related_name = 'opiniones',
     db_column = 'jugador',
     verbose_name = 'Creador de la opinion',
     null = True # Activar para conservar la opinion SET_NULL CAMBIAR SI NECESARIO
  ) #PONER EN NULL si jugador muere
  juego = models.ForeignKey(Juego, 
     on_delete = models.CASCADE, #AL Borrar el juego se borran los comentarios relacionados
     related_name = 'opiniones',
     db_column = 'juego',
     verbose_name = 'Juego al que pertenece la opinion',
  )
  comentario = models.TextField(blank = True)
  gusto = models.PositiveIntegerField(default = 1, blank = True,
  validators=[MinValueValidator(1), MaxValueValidator(10)]
  )
  guion = models.PositiveIntegerField(default = 1, blank = True,
  validators=[MinValueValidator(1), MaxValueValidator(10)]
  )
  artes = models.PositiveIntegerField(default = 1, blank = True,
  validators=[MinValueValidator(1), MaxValueValidator(10)]
  )
  jugabilidad = models.PositiveIntegerField(default=1, blank = True,
  validators=[MinValueValidator(1), MaxValueValidator(10)]
  )
  tecnico = models.PositiveIntegerField(default=1, blank = True,
  validators=[MinValueValidator(1), MaxValueValidator(10)]
  )
  def __str__(self):
   return '%s, %s' % (self.jugador.id, self.juego.titulo)

""" Entidades de relacion """
class JuegosFavoritos(models.Model):
  # id_jfavoritos = models.AutoField(primary_key = True)
  jugador = models.ForeignKey(Jugador,
    on_delete=models.CASCADE,
    null = True,
    to_field = 'nickname',
    db_column = 'jugador',
    related_name = 'juegos_favoritos',
    verbose_name = 'Jugador al que le gusta el juego',
  )
  juego = models.ForeignKey(Juego, 
    on_delete=models.CASCADE,
    null = True,
    db_column = 'juego',
    related_name = 'jugadores',
    verbose_name = 'Juego que le gusta al jugador',
  )
  def __str__(self):
   return '%s, %s' % (self.jugador.id, self.juego.titulo)
  #Dejando este campo opcional como comentario por el momento
  """
  fecha_adicion = models.DateField(blank = TRUE, 
  null = TRUE,
  verbose="En que fecha el usuario indico que le gustaba"
  )
  """

class GenerosFavoritos(models.Model):
  # id_gfavoritos = models.AutoField(primary_key = True)
  jugador = models.ForeignKey(Jugador,
    on_delete=models.CASCADE,
    null = True,
    to_field = 'nickname',
    db_column = 'jugador',
    related_name = 'generos_favoritos',
    verbose_name = 'Jugador al que le gusta el genero',
  )
  genero = models.ForeignKey(Genero, 
    on_delete=models.CASCADE,
    null = True,
    db_column = 'genero',
    related_name = 'jugadores',
    verbose_name = 'Genero que le gusta al jugador',
  )

class PlataformasFavoritas(models.Model):
  # id_pfavoritos = models.AutoField(primary_key = True)
  jugador = models.ForeignKey(Jugador, 
    on_delete=models.CASCADE,
    null = True,
    to_field = 'nickname',
    db_column = 'jugador',
    related_name = 'plataformas_favoritas',
    verbose_name = 'Jugador que tiene la plataforma',
  )
  plataforma = models.ForeignKey(Plataforma,
    on_delete=models.CASCADE,
    null = True,
    db_column = 'plataforma',
    related_name = 'jugadores',
    verbose_name = 'Plataforma que tiene el jugador',
  )


class CDE(models.Model):
  jugador = models.OneToOneField(Usuario, 
    on_delete = models.CASCADE, 
    primary_key = True,
    db_column = "id_jugador",
    verbose_name = "Jugador a quien pertenecen las CDE")

  cde0 = models.CharField(max_length=256)
  cde1 = models.CharField(max_length=256)
  cde2 = models.CharField(max_length=256)
  cde3 = models.CharField(max_length=256)
  cde4 = models.CharField(max_length=256)
  cde5 = models.CharField(max_length=256)
  cde6 = models.CharField(max_length=256)
  cde7 = models.CharField(max_length=256)
  cde8 = models.CharField(max_length=256)
  cde9 = models.CharField(max_length=256)


class Cpu(models.Model):
  cpu = models.OneToOneField(Usuario, 
    on_delete = models.CASCADE, 
    primary_key = True,
    db_column = "id_cpu",
    verbose_name = "Identificador de CPU")
  carusu1 = models.CharField(max_length=256)
  carusu2 = models.CharField(max_length=256)
  carusu3 = models.CharField(max_length=256)
  carusu4 = models.CharField(max_length=256)
  carusu5 = models.CharField(max_length=256)
  carusu6 = models.CharField(max_length=256)
  carusu7 = models.CharField(max_length=256)
  carusu8 = models.CharField(max_length=256)
  carusu9 = models.CharField(max_length=256)
  carusu10 = models.CharField(max_length=256)


