from django.db import models

# Create your models here.

class UserData(models.Model):
    username = models.CharField(max_length=255)
    lobby = models.CharField(max_length=255)
    time = models.IntegerField(null=True)
    start = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)

class MapData(models.Model):
    lobbyID = models.CharField(max_length=255)
    pinLocations = models.TextField()  
    solution = models.TextField()