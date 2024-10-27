from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    auth_token = models.CharField(max_length=255,null=True)

class Pins(models.Model):
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)


class Posts(models.Model):
    username = models.CharField(max_length=255)
    body = models.CharField(max_length=255,default='')
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    likes = models.IntegerField()
    parent = models.CharField(max_length=255,null=True)
    replies = models.IntegerField(null=True)

class Likes(models.Model):
    username = models.CharField(max_length=255)
    postID = models.IntegerField(null=True)
    
    