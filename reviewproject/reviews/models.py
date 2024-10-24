from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    auth_token = models.CharField(max_length=255,null=True)

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    body = models.CharField(max_length=255,default='')
    lat = models.IntegerField(null=True)
    long = models.IntegerField(null=True)
    likes = models.IntegerField()
    parent = models.CharField(max_length=255,null=True)
    replies = models.IntegerField(null=True)