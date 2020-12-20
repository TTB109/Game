from django.db.models import *
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
#from multiselectfield import MultiSelectField
import datetime
import os
from django.utils import timezone

class Generacion(models.Model):
  # id_generacion = models.AutoField(primary_key=True)
  #Introducir las generaciones como primera, septima y asi
  generacion = models.CharField(unique=True,
  null=False, max_length=20, verbose_name="Numero de generacion")
  #Numero de bits de esta generacion
  #https://www.tecnobreak.com/generaciones-videoconsolas/
  #https://gamedev.stackexchange.com/questions/114381/8-16-32-bits-consoles-what-does-it-mean
  bits = models.PositiveIntegerField(default = 4, blank = True,
    validators=[MinValueValidator(1), MaxValueValidator(2056)]
  )
  #Periodos
  inicio = models.DateField()
  fin = models.DateField()


class Plataforma(models.Model):
  # descripcion = models.TextField()
  # PCHOICES=(
  #           ('XboxOne','XboxOne'),
  #           ('Ps4','Ps4'),
  #           ('Nintendo Switch','Nintendo Switch'),
  #           ('Wii U','Wii U'),
  #           ('PS Vita','PS Vita'),
  #           ('3ds','3ds'),
  #           ('Android','Android'),
  #           ('Xbox360','Xbox360'),
  #           ('Ps3','Ps3'),
  #           ('Wii','Wii'),
  #           ('Psp','Psp'),
  #           ('Ds','Ds'),
  #           ('Windows','Windows'),
  #           ('Ipad','Ipad'),
  #           ('Xbox','Xbox'),
  #           ('Ps2','Ps2'),
  #           ('GameCube','GameCube'),
  #           ('GameboyAdvance','GameboyAdvance'),
  #           ('Dreamcast','Dreamcast'),
  #           ('J2me','J2me'),
  #           ('Ps1','Ps1'),
  #           ('Nintendo64','Nintendo64'),
  #           ('GameboyColor','GameboyColor'),
  #           ('Snes','Snes'),
  #           ('NeoGeo','NeoGeo'),
  #           ('Arcade','Arcade'),
  #           ('Nes','Nes'),
  #           ('Gameboy','Gameboy')
  # )
  # nombreP = MultiSelectField(choices=PCHOICES)
  #nombreP = models.CharField(max_length=100)
  id_plataforma = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=100)
  descripcion = models.TextField()

  class Meta:
    ordering = ['nombre']

  def __str__(self):
    return self.nombre

class Genero(models.Model):
  # GCHOICES=(
  #           ('Accion','Accion'),
  #           ('Aventura','Aventura'),
  #           ('Educativo','Educativo'),
  #           ('Rompecabezas','Rompecabezas'),
  #           ('Carreras','Carreras'),
  #           ('Rol','Rol'),
  #           ('Simulacion','Simulacion'),
  #           ('Deporte','Deporte'),
  #           ('Estrategia','Estrategia'),
  #           ('Arcade','Arcade'),
  #           ('Belico','Belico'),
  #           ('Peleas','Peleas'),
  #           ('JuegodeMesa','JuegodeMesa'),
  #           ('Musica','Musica'),
  #           ('Plataforma','Plataforma'),
  #           ('Disparos','Disparos'),
  #           ('Survivalhorror','Survivalhorror'),
  #           ('Trivia','Trivia')
  # )
  # nombreG = MultiSelectField(choices=GCHOICES)
  # nombreG = models.CharField(max_length=100)
  id_genero = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=100)
  descripcion = models.TextField()
  class Meta:
    ordering = ['nombre']
  def __str__(self):
   return self.nombre


class Compania(models.Model):
  id_compania = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=100)
  descripcion = models.TextField(max_length=300)
  def __str__(self):
   return self.nombre



class Juego(models.Model):
  id_juego = models.AutoField(primary_key=True)
  titulo = models.CharField(max_length=100)
  agnio=models.PositiveIntegerField(default = 2020)
  descripcion = models.CharField(max_length=5000)
  generos = models.ManyToManyField(Genero,
    through = 'GenerosAsociados',
    through_fields=('juego','genero')
  )
  plataformas = models.ManyToManyField(Plataforma,
    through = 'PlataformasAsociadas',
    through_fields=('juego','plataforma')
  )
  companias = models.ManyToManyField(Compania,
    through = 'CompaniasAsociadas',
    through_fields=('juego','compania')
  )
  # generos = models.CharField(max_length=100)
  # plataformas = models.CharField(max_length=100)    
  def __str__(self):
    #return '%s, %s, %s' % (self.titulo, self.jgeneros, self.jplataformas)
    return self.titulo

  # def Obt_Gen(self):
  #   OGeneros=str([ogenero for generos in self.generos.all().values_list('nombreG',flat=True)]).replace("[","").replace("]","").replace("'","")
  #   return OGeneros
  
  # def Obt_Plat(self):
  #   OPlataforma=str([oplataforma for plataformas in self.plataformas.all().values_list('nombreP',flat=True)]).replace("[","").replace("]","").replace("'","")
  #   return OPlataforma

class Imagen(models.Model):
  id_imagen = models.AutoField(primary_key=True)
  #tipo = models.IntegerField()
  #imagefile = models.ImageField(upload_to='static/', default = 'static/img/no-img.jpg')
  referencia=models.URLField(max_length=255)
  alt= models.CharField(max_length=100)
  juego = models.ForeignKey(Juego, 
  on_delete=models.CASCADE,
  db_column = 'juego',
  related_name = 'imagenes',
  verbose_name = 'Imagenes que representan el juego',
  )

  # def get_remote_image(self):
  #   if self.imageurl and not self.imagefile:
  #       result = urllib.urlretrieve(self.imageurl)
  #       self.imagefile.save(
  #               os.path.basename(self.imageurl),
  #               File(open(result[0]))
  #               )
  #        self.save()
  # def __str__(self):
  #  return self.imageurl

""" Entidades de relacion """
class GenerosAsociados(models.Model):
  # id_gAsociados = models.AutoField(primary_key = True)
  genero = models.ForeignKey(Genero, 
  on_delete=models.CASCADE,
  db_column = 'genero',
  related_name = 'juegos_asociados',
  verbose_name = 'Generos que conforman el juego',
  )
  juego = models.ForeignKey(Juego, 
  on_delete=models.CASCADE,
  null = True,
  db_column = 'juego',
  related_name = 'generos_asociados',
  verbose_name = 'Juegos que pertenecen al genero',
  )
  def __str__(self):
    return self.genero

class ListGeneros(models.Model):
  juego = models.ForeignKey(Juego, 
  on_delete=models.CASCADE,
  db_column = 'juego',
  null = True,
  related_name = 'generos_boolean',
  verbose_name = 'generos en boolean',
  )
  listgenero=models.CharField(max_length=100)
  listplataforma=models.CharField(max_length=100)
  def __str__(self):
    return self.juego

class PlataformasAsociadas(models.Model):
  # id_pAsociadas = models.AutoField(primary_key = True)
  plataforma = models.ForeignKey(Plataforma, 
  on_delete = models.CASCADE,
  db_column = 'plataforma',
  related_name = 'juegos_asociados',
  verbose_name = 'Plataforma a las que pertenece el juego',
  )
  juego = models.ForeignKey(Juego, 
  on_delete=models.CASCADE,
  null = True,
  db_column = 'juego',
  related_name = 'plataformas_asociadas',
  verbose_name = 'Juegos que pertenecen a la plataforma',
  )
  def __str__(self):
    return self.plataforma

  
class CompaniasAsociadas(models.Model):
  # id_pAsociadas = models.AutoField(primary_key = True)
  compania = models.ForeignKey(Compania, 
  on_delete = models.CASCADE,
  db_column = 'compania',
  related_name = 'juegos_asociados',
  verbose_name = 'Compañias que hicieron el juego',
  )
  juego = models.ForeignKey(Juego, 
  on_delete=models.CASCADE,
  null = True,
  db_column = 'juego',
  related_name = 'companias_asociadas',
  verbose_name = 'Juegos que pertenecen a la plataforma',
  )
  def __str__(self):
    return self.compania

# """ Entidades de relacion """
# class GenerosAsociados(models.Model):
#   # id_gAsociados = models.AutoField(primary_key = True)
#   genero = models.ForeignKey(Genero, 
#   on_delete=models.CASCADE,
#   db_column = 'genero',
#   related_name = 'juegos_asociados',
#   verbose_name = 'Generos que conforman el juego',
#   )
#   juego = models.ForeignKey(Juego, 
#   on_delete=models.CASCADE,
#   null = True,
#   db_column = 'juego',
#   related_name = 'generos_asociados',
#   verbose_name = 'Juegos que pertenecen al genero',
#   )

# class PlataformasAsociadas(models.Model):
#   # id_pAsociadas = models.AutoField(primary_key = True)
#   plataforma = models.ForeignKey(Plataforma, 
#   on_delete = models.CASCADE,
#   db_column = 'plataforma',
#   related_name = 'juegos_asociados',
#   verbose_name = 'Plataforma a las que pertenece el juego',
#   )
#   juego = models.ForeignKey(Juego, 
#   on_delete=models.CASCADE,
#   null = True,
#   db_column = 'juego',
#   related_name = 'plataformas_asociadas',
#   verbose_name = 'Juegos que pertenecen a la plataforma',
#   )
