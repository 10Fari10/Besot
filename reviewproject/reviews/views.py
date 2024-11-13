from django.shortcuts import render
import json
from reviews.models import Posts
from reviews.models import Pins
from reviews.models import Likes
from reviews.models import ProfilePics
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect
import html

import logging
from django.conf import settings

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))

def main_homepage(request):
    return render(request, 'reviews/homepage.html') 


#Gets Profile pic
@csrf_protect
def loadpfp(request):
    if request.method=='GET':
       username = request.user.get_username()
       pass
    

#Post Profile pic
@csrf_protect 
def postpfp(request):
   if request.method=='POST':
       username = request.user.get_username()
       pass

@csrf_protect
#Receives post requests from users posting and replying
def postHandle(request):
  if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please Login First'}, status=401)

  if request.method == "POST":

        req_body = request.body.decode()
        req_body = json.loads(req_body)
        lat = float(req_body["latVal"])  
        print(lat)
        long = float(req_body["longVal"])
        print(long)
        body = req_body.get("review", "")
        parent = req_body.get("parent", -1)
        likes = req_body.get("likes", 0)
        replies = req_body.get("replies", 0)
        
        print(f"Creating pin at Latitude: {lat}, Longitude: {long}")
        pin = Pins(lat = lat, long = long)
        pin.save()
        username = request.user.get_username()
        post = Posts(username=username, lat=lat, long=long, parent=parent,likes=likes, replies=replies, body=body)
        post.save()
       

        if parent != -1:
          parent_post = Posts.objects.get(id=parent)
          parent_post.replies += 1
          parent_post.save()
             

        SendPins = list(Pins.objects.values("lat", "long"))
       
        return JsonResponse({"message": "Post created successfully!", "pins": SendPins}, status=201)

  return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_protect
#Receives post requests from users liking
def likeHandle(request):
  if request.method == "POST":
   req_body = request.body.decode()
   req_body = json.loads(req_body)
   id = req_body["id"]
   post = Posts.objects.get(id=id)
   if(Posts.objects.filter(id=id).count() ==1):
    if request.user.is_authenticated:
     user = request.user.get_username()
     if(Likes.objects.filter(username=user,postID=id).count()>0):
        post.likes = post.likes-1
        post.save()
        Likes.objects.filter(username=user,postID=id).delete()
     else:
        post.likes = post.likes+1
        post.save()
        like = Likes(username=user,postID=id)
        like.save()
   return JsonResponse({"likes": post.likes}, status=200)
   
  return JsonResponse({"error": "Post not found"}, status=404)

@csrf_protect
#Receives get requests and sends posts from specified location to front end
#Make a post on front end. Send post data to backend. Backend saves to pins database. Sends list of pin back. Front end renders all pins. When pin is clicked, sends request to backed. Backends sends all post data.
def sendPost(request):
  lat = float(request.GET.get("lat"))
  long= float(request.GET.get("long"))
  post = Posts.objects.filter(lat=lat,long=long).order_by("id").values()
  allPosts = []
  if post.exists():
    for p in post:
      parent_content = {}
      parent_content["username"] = html.escape(p["username"])
      parent_content["body"] = html.escape(p["body"])
      parent_content["likes"] = p["likes"]
      parent_content["parent"] = p["parent"]
      parent_content["reply_num"] = p["replies"]
      parent_content['id'] = p["id"]
      replies = []
      reply = Posts.objects.filter(parent=p["id"]).order_by("id").values()
      for r in reply:
        reply_content = {}
        reply_content["username"] = html.escape(r["username"])
        reply_content["body"] = html.escape(r["body"])
        reply_content["likes"]= r["likes"]
        reply_content["parent"]= r["parent"]
        reply_content["reply_num"]= r["replies"]
        reply_content['id'] = r["id"]
        replies.append(reply_content)
      parent_content["replies"] =  replies
      allPosts.append(parent_content)
  
 
  return JsonResponse(allPosts,safe=False)

@csrf_protect
def sendPins(request):
   if request.method == "GET":
        pins = list(Pins.objects.values("lat", "long"))  
        return JsonResponse({"pins": pins}, status=200)
   return JsonResponse({'error': 'Invalid request method'}, status=405)



