from django.shortcuts import render
import json
import bcrypt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from reviews.models import Users
from reviews.models import Posts
import hashlib
from django.views.decorators.csrf import csrf_protect

def main_homepage(request):
    return render(request, 'reviews/homepage.html') 

@csrf_protect
def postHandle(request):
  #handle authtoken
  #use autoincrement id for post username
  #increment reply and like number
  #remember to migrate and add urls
  #handle no auth
  #check hash method
  #escape special characters
  auth = request.COOKIES.get('auth_token')
  if not(auth is None):
    sha = hashlib.sha256()
    sha.update(auth.encode())
    auth = sha.hexdigest()
    if(Users.objects.filter(auth_token=auth).count() ==1):
      user = Users.objects.get(auth_token=auth)
      post = Posts(username=user.username,lat= 0,long=0,parent=request.parent,likes=0,replies=0)
      post.save()
    if(request.parent != -1):
      parent = request.parent
      post = Posts.objects.get(id=parent)
      post.replies = post.replies+1
      post.save()
  else:
    return HttpResponse('Unauthorized', status=401)
  next = request.POST.get('next','/')
  return HttpResponseRedirect(next)

@csrf_protect
def likeHandle(request):
  #handle authtoken
  #use autoincrement id for post username
  #increment reply and like number
  #ask about like functionality
  parent = request.parent
  post = Posts.objects.get(id=parent)
  if(Posts.objects.filter(id=parent).count() ==1):
    post.likes = post.likes+1
    post.save()
  next = request.POST.get('next','/')
  return HttpResponseRedirect(next)

@csrf_protect
def sendPost(request):
  template= loader.get_template("homepage.html")
  lat = request.lat
  long = request.long
  post = Posts.objects.filter(lat=lat,long=long).order_by("id").values()
  allPosts = []
  for p in post:
     parent_content = {}
     parent_content.username = p.username
     parent_content.body = p.body
     parent_content.likes = p.likes
     parent_content.parent = p.parent
     parent_content.reply_num = p.replies
     replies = []
     reply = Posts.objects.filter(parent=p.postID).order_by("id").values()
     for r in reply:
       reply_content = {}
       reply_content.username = r.username
       reply_content.body = r.body
       reply_content.likes = r.likes
       reply_content.parent = r.parent
       reply_content.replies = r.replies
       replies.append(reply_content)
     parent_content.replies =  replies
     allPosts.append(parent_content)
  context = {
    'allposts':allPosts
  }
  return HttpResponse(template.render(context,request))