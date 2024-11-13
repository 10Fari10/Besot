from django.db import models

# Create your models here.

class UserData(models.Model):
    username = models.CharField(max_length=255)
    lobby = models.CharField(max_length=255)
    time = models.IntegerField()

class MapData(models.Model):
    lobbyID = models.CharField(max_length=255)
    pinLocations= models.CharField(max_length=255)
    solution = models.CharField(max_length=255)