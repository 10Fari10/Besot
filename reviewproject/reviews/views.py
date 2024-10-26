from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from reviews.models import Users
from reviews.models import Posts
from reviews.models import Pins
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

@csrf_protect
#Receives post requests from users posting and replying
def postHandle(request):
  if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

  if request.method == "POST":

        req_body = request.body.decode()
        req_body = json.loads(req_body)
        lat = float(req_body.get("latVal", 0))  
        long = float(req_body.get("longVal", 0))
        body = html.escape(req_body.get("review", ""))
        parent = req_body.get("parent", -1)
        likes = req_body.get("likes", 0)
        replies = req_body.get("replies", 0)

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
  req_body = request.body.decode()
  req_body = json.loads(req_body)
  id = req_body["id"]
  post = Posts.objects.get(id=id)
  if(Posts.objects.filter(id=id).count() ==1):
    post.likes = post.likes+1
    post.save()
  next = request.POST.get('next','/')
  return HttpResponseRedirect(next)

@csrf_protect
#Receives get requests and sends posts from specified location to front end
#Make a post on front end. Send post data to backend. Backend saves to pins database. Sends list of pin back. Front end renders all pins. When pin is clicked, sends request to backed. Backends sends all post data.
def sendPost(request):
  lat = int(float(request.GET.get("lat")))
  long= int(float(request.GET.get("long")))
  post = Posts.objects.filter(lat=lat,long=long).order_by("id").values()
  allPosts = []
  if(Posts.objects.filter(lat=lat,long=long).count()>0):
    for p in post:
      parent_content = {}
      parent_content["username"] = p["username"]
      parent_content["body"] = p["body"]
      parent_content["likes"] = p["likes"]
      parent_content["parent"] = p["parent"]
      parent_content["reply_num"] = p["replies"]
      parent_content['id'] = p["id"]
      replies = []
      reply = Posts.objects.filter(parent=p["id"]).order_by("id").values()
      for r in reply:
        reply_content = {}
        reply_content["username"] = r["username"]
        reply_content["body"] = r["body"]
        reply_content["likes"]= r["likes"]
        reply_content["parent"]= r["parent"]
        reply_content["reply_num"]= r["replies"]
        reply_content['id'] = r["id"]
        replies.append(reply_content)
      parent_content["replies"] =  replies
      allPosts.append(parent_content)
  return JsonResponse(allPosts,safe=False)

@csrf_protect
def sendPins():
  allPins = []
  pins = Pins.objects.all().values
  if(Posts.objects.all().count()>0):
    for pin in pins:
      allPins.append([pin["lat"],pin["long"]])
  return JsonResponse(allPins,safe=False)
