from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length = 255)

class Posts(models.Model):
    username = models.CharField(max_length=255)
    lat = models.IntegerField(null=True)
    long = models.IntegerField(null=True)
    likes = models.IntegerField()
    parent = models.CharField(max_length=255,null=True)
    replies = models.IntegerField(null=True)