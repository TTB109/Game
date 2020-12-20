from django.db.models import *
from django.db import models#, FloatField
from gamehouse.sjug.models import Juego,Usuario,JuegosFavoritos,Opinion

class MatrizJuegos(models.Model):
  juego = models.OneToOneField(Juego, 
    on_delete = models.CASCADE, 
    primary_key = True,
    db_column = "id_juego",
    verbose_name = "Identificador del juego"
  )
  vectorGENERO =models.CharField(max_length=256)
  vectorPLATAFORMA =models.CharField(max_length=256)
  agno = models.PositiveIntegerField(default = 2000)
  vectorCPU =models.CharField(max_length=256)
  vectorCDE =models.CharField(max_length=256)

  # caractpu0 = models.PositiveIntegerField(default = 0, blank = True)
  # caractpu1 = models.PositiveIntegerField(default = 0, blank = True)
  # caractpu2 = models.PositiveIntegerField(default = 0, blank = True)
  # caractpu3 = models.PositiveIntegerField(default = 0, blank = True)
  # caractpu4 = models.PositiveIntegerField(default = 0, blank = True)
  # caractpu5 = models.PositiveIntegerField(default = 0, blank = True)
  # caractpu6 = models.PositiveIntegerField(default = 0, blank = True)
  # caractpu7 = models.PositiveIntegerField(default = 0, blank = True)
  # caractpu8 = models.PositiveIntegerField(default = 0, blank = True)  
  # caractpu9 = models.PositiveIntegerField(default = 0, blank = True)

  # caractde0 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde1 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde2 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde3 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde4 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde5 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde6 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde7 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde8 = models.PositiveIntegerField(default = 0, blank = True)
  # caractde9 = models.PositiveIntegerField(default = 0, blank = True)

class TfIdf(models.Model):
  juego = models.OneToOneField(Juego, 
    on_delete = models.CASCADE, 
    primary_key = True,
    db_column = "id_juego",
    verbose_name = "Identificador del juego"
  )
  vector=models.CharField(max_length=256)
  #vector = models.FileField(upload_to='raw/tfidf')